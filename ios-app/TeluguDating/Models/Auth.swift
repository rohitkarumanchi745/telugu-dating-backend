import Foundation

// MARK: - Send OTP Request
struct SendOTPRequest: Codable {
    let phoneNumber: String
}

// MARK: - Send OTP Response
struct SendOTPResponse: Codable {
    let message: String
    let otp: String? // Only returned in dev mode
}

// MARK: - Verify OTP Request
struct VerifyOTPRequest: Codable {
    let phoneNumber: String
    let otp: String
}

// MARK: - Verify OTP Response
struct VerifyOTPResponse: Codable {
    let accessToken: String
    let tokenType: String?
    let userId: Int
    let isNewUser: Bool?
    let isProfileComplete: Bool?
}

// MARK: - Token Claims (for JWT decoding if needed)
struct TokenClaims: Codable {
    let sub: String
    let exp: Int
    let scope: String?
    let matchId: String?
    let callId: String?
    let isAdmin: Bool?
}
