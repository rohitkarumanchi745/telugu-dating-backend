import Foundation
import Security

// MARK: - Keychain Manager
final class KeychainManager {
    static let shared = KeychainManager()

    private let serviceName = "com.telugudating.app"

    private enum Keys {
        static let accessToken = "access_token"
        static let refreshToken = "refresh_token"
        static let userId = "user_id"
        static let tokenExpiry = "token_expiry"
    }

    private init() {}

    // MARK: - Access Token
    func saveAccessToken(_ token: String) {
        save(key: Keys.accessToken, value: token)
    }

    func getAccessToken() -> String? {
        return get(key: Keys.accessToken)
    }

    // MARK: - Refresh Token
    func saveRefreshToken(_ token: String) {
        save(key: Keys.refreshToken, value: token)
    }

    func getRefreshToken() -> String? {
        return get(key: Keys.refreshToken)
    }

    // MARK: - User ID
    func saveUserId(_ userId: Int) {
        save(key: Keys.userId, value: String(userId))
    }

    func getUserId() -> Int? {
        guard let idString = get(key: Keys.userId) else { return nil }
        return Int(idString)
    }

    // MARK: - Token Expiry
    func saveTokenExpiry(_ date: Date) {
        let timestamp = String(date.timeIntervalSince1970)
        save(key: Keys.tokenExpiry, value: timestamp)
    }

    func getTokenExpiry() -> Date? {
        guard let timestamp = get(key: Keys.tokenExpiry),
              let interval = Double(timestamp) else { return nil }
        return Date(timeIntervalSince1970: interval)
    }

    func isTokenExpired() -> Bool {
        guard let expiry = getTokenExpiry() else { return true }
        return Date() >= expiry
    }

    // MARK: - Clear All
    func clearTokens() {
        delete(key: Keys.accessToken)
        delete(key: Keys.refreshToken)
        delete(key: Keys.userId)
        delete(key: Keys.tokenExpiry)
    }

    // MARK: - Generic Keychain Operations
    private func save(key: String, value: String) {
        guard let data = value.data(using: .utf8) else { return }

        let query: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrService as String: serviceName,
            kSecAttrAccount as String: key,
            kSecValueData as String: data,
            kSecAttrAccessible as String: kSecAttrAccessibleAfterFirstUnlockThisDeviceOnly
        ]

        // Delete existing item first
        SecItemDelete(query as CFDictionary)

        // Add new item
        let status = SecItemAdd(query as CFDictionary, nil)
        if status != errSecSuccess {
            print("Keychain save error: \(status)")
        }
    }

    private func get(key: String) -> String? {
        let query: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrService as String: serviceName,
            kSecAttrAccount as String: key,
            kSecReturnData as String: true,
            kSecMatchLimit as String: kSecMatchLimitOne
        ]

        var result: AnyObject?
        let status = SecItemCopyMatching(query as CFDictionary, &result)

        guard status == errSecSuccess,
              let data = result as? Data,
              let string = String(data: data, encoding: .utf8) else {
            return nil
        }

        return string
    }

    private func delete(key: String) {
        let query: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrService as String: serviceName,
            kSecAttrAccount as String: key
        ]

        SecItemDelete(query as CFDictionary)
    }
}
