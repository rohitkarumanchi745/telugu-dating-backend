import Foundation
import UIKit

// MARK: - Profile Service
actor ProfileService {
    static let shared = ProfileService()

    private init() {}

    // MARK: - Get Profile
    func getMyProfile() async throws -> UserProfile {
        return try await APIClient.shared.request(endpoint: .profileMe)
    }

    // MARK: - Get Profile Status
    func getProfileStatus() async throws -> ProfileStatus {
        return try await APIClient.shared.request(endpoint: .profileStatus)
    }

    // MARK: - Update Profile with Photos
    func updateProfile(
        name: String?,
        dob: String?,
        gender: String?,
        photos: [UIImage]
    ) async throws -> UserProfile {
        var fields: [String: String] = [:]

        if let name = name { fields["name"] = name }
        if let dob = dob { fields["dob"] = dob }
        if let gender = gender { fields["gender"] = gender }

        var files: [(name: String, data: Data, filename: String, mimeType: String)] = []

        for (index, image) in photos.enumerated() {
            if let imageData = compressImage(image) {
                files.append((
                    name: "profile_photo_\(index + 1)",
                    data: imageData,
                    filename: "photo_\(index + 1).jpg",
                    mimeType: "image/jpeg"
                ))
            }
        }

        return try await APIClient.shared.uploadMultipart(
            endpoint: .updateProfile,
            files: files,
            fields: fields
        )
    }

    // MARK: - Update Bio
    func updateBio(_ bio: String) async throws -> UserProfile {
        struct BioRequest: Codable {
            let bio: String
        }
        return try await APIClient.shared.request(
            endpoint: .updateBio,
            body: BioRequest(bio: bio)
        )
    }

    // MARK: - Update Preferences
    func updatePreferences(_ preferences: UserPreferences) async throws -> UserProfile {
        return try await APIClient.shared.request(
            endpoint: .preferences,
            body: preferences
        )
    }

    // MARK: - Upload Voice Intro
    func uploadVoiceIntro(audioData: Data, duration: Int) async throws -> VoiceIntroResponse {
        let files: [(name: String, data: Data, filename: String, mimeType: String)] = [
            (name: "voice_file", data: audioData, filename: "voice_intro.m4a", mimeType: "audio/mp4")
        ]

        let fields = ["duration_seconds": String(duration)]

        return try await APIClient.shared.uploadMultipart(
            endpoint: .uploadVoiceIntro,
            files: files,
            fields: fields
        )
    }

    // MARK: - Image Compression
    private func compressImage(_ image: UIImage, maxSizeKB: Int = 100) -> Data? {
        var compression: CGFloat = 1.0
        let maxBytes = maxSizeKB * 1024

        guard var imageData = image.jpegData(compressionQuality: compression) else {
            return nil
        }

        while imageData.count > maxBytes && compression > 0.1 {
            compression -= 0.1
            if let newData = image.jpegData(compressionQuality: compression) {
                imageData = newData
            }
        }

        return imageData
    }
}

// MARK: - Voice Intro Response
struct VoiceIntroResponse: Codable {
    let success: Bool
    let voiceIntroUrl: String?
    let durationSeconds: Int?
    let message: String?
}
