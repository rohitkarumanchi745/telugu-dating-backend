import Foundation
import Combine

// MARK: - Auth Service
@MainActor
final class AuthService: ObservableObject {
    static let shared = AuthService()

    @Published var isAuthenticated = false
    @Published var currentUser: UserProfile?
    @Published var isLoading = false
    @Published var error: String?

    private var cancellables = Set<AnyCancellable>()

    private init() {
        checkAuthStatus()
        setupLogoutObserver()
    }

    // MARK: - Check Auth Status
    func checkAuthStatus() {
        isAuthenticated = KeychainManager.shared.getAccessToken() != nil
            && !KeychainManager.shared.isTokenExpired()

        if isAuthenticated {
            Task {
                await fetchCurrentUser()
            }
        }
    }

    private func setupLogoutObserver() {
        NotificationCenter.default.publisher(for: .userDidLogout)
            .receive(on: DispatchQueue.main)
            .sink { [weak self] _ in
                self?.isAuthenticated = false
                self?.currentUser = nil
            }
            .store(in: &cancellables)
    }

    // MARK: - Send OTP
    func sendOTP(phoneNumber: String) async throws -> SendOTPResponse {
        isLoading = true
        error = nil
        defer { isLoading = false }

        let request = SendOTPRequest(phoneNumber: phoneNumber)
        let response: SendOTPResponse = try await APIClient.shared.request(
            endpoint: .sendOTP,
            body: request
        )
        return response
    }

    // MARK: - Verify OTP
    func verifyOTP(phoneNumber: String, otp: String) async throws -> VerifyOTPResponse {
        isLoading = true
        error = nil
        defer { isLoading = false }

        let request = VerifyOTPRequest(phoneNumber: phoneNumber, otp: otp)
        let response: VerifyOTPResponse = try await APIClient.shared.request(
            endpoint: .verifyOTP,
            body: request
        )

        // Save tokens
        KeychainManager.shared.saveAccessToken(response.accessToken)
        KeychainManager.shared.saveUserId(response.userId)

        // Calculate expiry (default 24 hours if not specified)
        let expiryDate = Date().addingTimeInterval(24 * 60 * 60)
        KeychainManager.shared.saveTokenExpiry(expiryDate)

        isAuthenticated = true
        NotificationCenter.default.post(name: .userDidLogin, object: nil)

        // Fetch user profile
        await fetchCurrentUser()

        return response
    }

    // MARK: - Fetch Current User
    func fetchCurrentUser() async {
        do {
            let profile: UserProfile = try await APIClient.shared.request(endpoint: .profileMe)
            currentUser = profile
        } catch {
            print("Failed to fetch user profile: \(error)")
        }
    }

    // MARK: - Logout
    func logout() {
        KeychainManager.shared.clearTokens()
        isAuthenticated = false
        currentUser = nil
        NotificationCenter.default.post(name: .userDidLogout, object: nil)
    }

    // MARK: - Check Profile Completion
    func getProfileStatus() async throws -> ProfileStatus {
        return try await APIClient.shared.request(endpoint: .profileStatus)
    }
}
