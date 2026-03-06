import Foundation

// MARK: - API Configuration
enum APIConfig {
    static let baseURL = "https://your-api-domain.com" // Replace with your actual API URL
    static let wsBaseURL = "wss://your-api-domain.com" // WebSocket URL

    // For local development
    static let localBaseURL = "http://localhost:3000"
    static let localWSBaseURL = "ws://localhost:3000"
}

// MARK: - API Endpoints
enum APIEndpoint {
    // Authentication
    case sendOTP
    case verifyOTP

    // Profile
    case profileMe
    case profileStatus
    case updateProfile
    case updateBio
    case preferences

    // Discovery & Matching
    case discover
    case like
    case pass
    case matches
    case matchDetail(String)

    // Voice Intro
    case uploadVoiceIntro
    case trackVoicePlay

    // Location
    case updateLocation
    case searchLocation
    case nearbyUsers
    case myLocation

    // Calls
    case initializeCall

    // Payments
    case createOrder
    case verifyPayment
    case products
    case subscriptions
    case cancelSubscription

    // Reels
    case createReel
    case reelsFeed
    case likeReel
    case messageReel
    case reelsInbox

    // Student Verification
    case verifyStudent
    case verifyStudentOTP
    case studentStatus

    // Selfie Verification
    case verifySelfie

    // WebSocket
    case chatWebSocket(matchId: String)
    case callWebSocket(callId: String)

    var path: String {
        switch self {
        case .sendOTP: return "/send-otp"
        case .verifyOTP: return "/verify-otp"
        case .profileMe: return "/profile/me"
        case .profileStatus: return "/profile/status"
        case .updateProfile: return "/update-profile"
        case .updateBio: return "/update-bio"
        case .preferences: return "/preferences"
        case .discover: return "/discover"
        case .like: return "/match/like"
        case .pass: return "/match/pass"
        case .matches: return "/matches"
        case .matchDetail(let id): return "/match/\(id)"
        case .uploadVoiceIntro: return "/voice-intro"
        case .trackVoicePlay: return "/voice-intro/track"
        case .updateLocation: return "/location/update"
        case .searchLocation: return "/location/search"
        case .nearbyUsers: return "/location/nearby"
        case .myLocation: return "/me/location"
        case .initializeCall: return "/calls"
        case .createOrder: return "/api/payments/create-order"
        case .verifyPayment: return "/api/payments/verify"
        case .products: return "/api/payments/products"
        case .subscriptions: return "/api/payments/subscriptions"
        case .cancelSubscription: return "/api/payments/subscriptions/cancel"
        case .createReel: return "/reels"
        case .reelsFeed: return "/reels/feed"
        case .likeReel: return "/reels/like"
        case .messageReel: return "/reels/message"
        case .reelsInbox: return "/reels/inbox"
        case .verifyStudent: return "/student/verify"
        case .verifyStudentOTP: return "/student/verify-otp"
        case .studentStatus: return "/student/status"
        case .verifySelfie: return "/verify/selfie"
        case .chatWebSocket(let matchId): return "/ws/chat?match_id=\(matchId)"
        case .callWebSocket(let callId): return "/ws/call?call_id=\(callId)"
        }
    }

    var method: HTTPMethod {
        switch self {
        case .sendOTP, .verifyOTP, .updateProfile, .updateBio, .preferences,
             .like, .pass, .uploadVoiceIntro, .trackVoicePlay, .updateLocation,
             .initializeCall, .createOrder, .verifyPayment, .cancelSubscription,
             .createReel, .likeReel, .messageReel, .verifyStudent, .verifyStudentOTP,
             .verifySelfie:
            return .POST
        case .profileMe, .profileStatus, .discover, .matches, .matchDetail,
             .searchLocation, .nearbyUsers, .myLocation, .products, .subscriptions,
             .reelsFeed, .reelsInbox, .studentStatus, .chatWebSocket, .callWebSocket:
            return .GET
        }
    }
}

enum HTTPMethod: String {
    case GET, POST, PUT, DELETE, PATCH
}

// MARK: - API Error
enum APIError: Error, LocalizedError {
    case invalidURL
    case noData
    case decodingError(Error)
    case networkError(Error)
    case serverError(Int, String)
    case unauthorized
    case rateLimited(retryAfter: Int)
    case unknown

    var errorDescription: String? {
        switch self {
        case .invalidURL:
            return "Invalid URL"
        case .noData:
            return "No data received"
        case .decodingError(let error):
            return "Decoding error: \(error.localizedDescription)"
        case .networkError(let error):
            return "Network error: \(error.localizedDescription)"
        case .serverError(let code, let message):
            return "Server error (\(code)): \(message)"
        case .unauthorized:
            return "Unauthorized - Please login again"
        case .rateLimited(let retryAfter):
            return "Rate limited. Retry after \(retryAfter) seconds"
        case .unknown:
            return "Unknown error occurred"
        }
    }
}

// MARK: - API Response
struct APIResponse<T: Decodable>: Decodable {
    let data: T?
    let detail: String?
}

// MARK: - API Client
actor APIClient {
    static let shared = APIClient()

    private let session: URLSession
    private let decoder: JSONDecoder
    private let encoder: JSONEncoder

    private init() {
        let config = URLSessionConfiguration.default
        config.timeoutIntervalForRequest = 30
        config.timeoutIntervalForResource = 60
        self.session = URLSession(configuration: config)

        self.decoder = JSONDecoder()
        decoder.keyDecodingStrategy = .convertFromSnakeCase
        decoder.dateDecodingStrategy = .iso8601

        self.encoder = JSONEncoder()
        encoder.keyEncodingStrategy = .convertToSnakeCase
        encoder.dateEncodingStrategy = .iso8601
    }

    // MARK: - Request Building
    private func buildRequest(
        endpoint: APIEndpoint,
        body: Encodable? = nil,
        queryItems: [URLQueryItem]? = nil
    ) throws -> URLRequest {
        var urlString = APIConfig.baseURL + endpoint.path

        if let queryItems = queryItems, !queryItems.isEmpty {
            var components = URLComponents(string: urlString)
            components?.queryItems = queryItems
            urlString = components?.url?.absoluteString ?? urlString
        }

        guard let url = URL(string: urlString) else {
            throw APIError.invalidURL
        }

        var request = URLRequest(url: url)
        request.httpMethod = endpoint.method.rawValue
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        request.setValue("application/json", forHTTPHeaderField: "Accept")

        // Add auth token if available
        if let token = KeychainManager.shared.getAccessToken() {
            request.setValue("Bearer \(token)", forHTTPHeaderField: "Authorization")
        }

        if let body = body {
            request.httpBody = try encoder.encode(body)
        }

        return request
    }

    // MARK: - Generic Request
    func request<T: Decodable>(
        endpoint: APIEndpoint,
        body: Encodable? = nil,
        queryItems: [URLQueryItem]? = nil
    ) async throws -> T {
        let request = try buildRequest(endpoint: endpoint, body: body, queryItems: queryItems)

        let (data, response) = try await session.data(for: request)

        guard let httpResponse = response as? HTTPURLResponse else {
            throw APIError.unknown
        }

        // Handle rate limiting
        if httpResponse.statusCode == 429 {
            let retryAfter = Int(httpResponse.value(forHTTPHeaderField: "Retry-After") ?? "60") ?? 60
            throw APIError.rateLimited(retryAfter: retryAfter)
        }

        // Handle unauthorized
        if httpResponse.statusCode == 401 {
            // Clear tokens and notify app
            KeychainManager.shared.clearTokens()
            NotificationCenter.default.post(name: .userDidLogout, object: nil)
            throw APIError.unauthorized
        }

        // Handle server errors
        if httpResponse.statusCode >= 400 {
            if let errorResponse = try? decoder.decode(ErrorResponse.self, from: data) {
                throw APIError.serverError(httpResponse.statusCode, errorResponse.detail)
            }
            throw APIError.serverError(httpResponse.statusCode, "Unknown error")
        }

        do {
            return try decoder.decode(T.self, from: data)
        } catch {
            throw APIError.decodingError(error)
        }
    }

    // MARK: - Multipart Upload
    func uploadMultipart<T: Decodable>(
        endpoint: APIEndpoint,
        files: [(name: String, data: Data, filename: String, mimeType: String)],
        fields: [String: String] = [:],
        progressHandler: ((Double) -> Void)? = nil
    ) async throws -> T {
        let boundary = UUID().uuidString
        var urlString = APIConfig.baseURL + endpoint.path

        guard let url = URL(string: urlString) else {
            throw APIError.invalidURL
        }

        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("multipart/form-data; boundary=\(boundary)", forHTTPHeaderField: "Content-Type")

        if let token = KeychainManager.shared.getAccessToken() {
            request.setValue("Bearer \(token)", forHTTPHeaderField: "Authorization")
        }

        var body = Data()

        // Add text fields
        for (key, value) in fields {
            body.append("--\(boundary)\r\n".data(using: .utf8)!)
            body.append("Content-Disposition: form-data; name=\"\(key)\"\r\n\r\n".data(using: .utf8)!)
            body.append("\(value)\r\n".data(using: .utf8)!)
        }

        // Add files
        for file in files {
            body.append("--\(boundary)\r\n".data(using: .utf8)!)
            body.append("Content-Disposition: form-data; name=\"\(file.name)\"; filename=\"\(file.filename)\"\r\n".data(using: .utf8)!)
            body.append("Content-Type: \(file.mimeType)\r\n\r\n".data(using: .utf8)!)
            body.append(file.data)
            body.append("\r\n".data(using: .utf8)!)
        }

        body.append("--\(boundary)--\r\n".data(using: .utf8)!)
        request.httpBody = body

        let (data, response) = try await session.data(for: request)

        guard let httpResponse = response as? HTTPURLResponse else {
            throw APIError.unknown
        }

        if httpResponse.statusCode >= 400 {
            if let errorResponse = try? decoder.decode(ErrorResponse.self, from: data) {
                throw APIError.serverError(httpResponse.statusCode, errorResponse.detail)
            }
            throw APIError.serverError(httpResponse.statusCode, "Upload failed")
        }

        return try decoder.decode(T.self, from: data)
    }
}

// MARK: - Error Response
struct ErrorResponse: Decodable {
    let detail: String
}

// MARK: - Notification Names
extension Notification.Name {
    static let userDidLogout = Notification.Name("userDidLogout")
    static let userDidLogin = Notification.Name("userDidLogin")
    static let newMatchReceived = Notification.Name("newMatchReceived")
    static let newMessageReceived = Notification.Name("newMessageReceived")
}
