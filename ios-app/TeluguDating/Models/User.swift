import Foundation

// MARK: - User Profile
struct UserProfile: Codable, Identifiable, Hashable {
    let id: Int
    let phoneNumber: String?
    let email: String?
    let name: String?
    let dob: String?
    let age: Int?
    let gender: String?
    let bio: String?
    let location: String?
    let interests: [String]?
    let languages: [String]?
    let lookingFor: String?
    let professionCategory: String?
    let professionTitle: String?
    let heightCm: Int?
    let photos: [String]?
    let isProfileComplete: Bool?
    let profileCompletion: Int?
    let attractivenessScore: Double?
    let isVerified: Bool?
    let isStudentVerified: Bool?
    let preferences: UserPreferences?
    let locationData: UserLocation?
    let subscriptions: [Subscription]?
    let spots: [Spot]?

    // Computed properties
    var displayName: String {
        name ?? "User"
    }

    var primaryPhoto: URL? {
        guard let firstPhoto = photos?.first else { return nil }
        return URL(string: APIConfig.baseURL + firstPhoto)
    }

    var allPhotoURLs: [URL] {
        photos?.compactMap { URL(string: APIConfig.baseURL + $0) } ?? []
    }

    var formattedHeight: String? {
        guard let height = heightCm else { return nil }
        let feet = height / 30
        let inches = (height % 30) / 2
        return "\(feet)'\(inches)\""
    }

    var hasActiveSubscription: Bool {
        subscriptions?.contains { $0.isActive == true } ?? false
    }

    func hash(into hasher: inout Hasher) {
        hasher.combine(id)
    }

    static func == (lhs: UserProfile, rhs: UserProfile) -> Bool {
        lhs.id == rhs.id
    }
}

// MARK: - User Preferences
struct UserPreferences: Codable {
    var minAge: Int?
    var maxAge: Int?
    var preferredGenders: [String]?
    var maxDistanceKm: Int?
    var onlyVerified: Bool?
    var onlyStudents: Bool?
    var preferredLocations: [String]?
    var intent: String?
}

// MARK: - User Location
struct UserLocation: Codable {
    let latitude: Double?
    let longitude: Double?
    let city: String?
    let state: String?
    let country: String?
    let neighborhood: String?
    let isFuzzy: Bool?
    let showExactDistance: Bool?
    let lastUpdated: String?
}

// MARK: - Subscription
struct Subscription: Codable, Identifiable {
    let id: String
    let subscriptionType: String?
    let passType: String?
    let startDate: String?
    let endDate: String?
    let status: String?
    let isActive: Bool?
}

// MARK: - Spot (Short Videos)
struct Spot: Codable, Identifiable {
    let id: Int
    let title: String?
    let posterUrl: String?
    let renditions: [String]?
    let expiresAt: String?
    let createdAt: String?
    let isGlobal: Bool?
    let city: String?
    let tags: [String]?
}

// MARK: - Discovery Profile (Lightweight for swiping)
struct DiscoveryProfile: Codable, Identifiable, Hashable {
    let id: Int
    let name: String?
    let age: Int?
    let gender: String?
    let bio: String?
    let photos: [String]?
    let isVerified: Bool?
    let lookingFor: String?
    let professionTitle: String?
    let heightCm: Int?
    let distanceKm: Double?
    let distanceText: String?
    let city: String?
    let compatibilityScore: Double?
    let voiceIntroUrl: String?
    let voiceIntroDuration: Int?
    let hasVoiceIntro: Bool?
    let languages: [String]?

    var displayName: String {
        name ?? "User"
    }

    var primaryPhoto: URL? {
        guard let firstPhoto = photos?.first else { return nil }
        return URL(string: APIConfig.baseURL + firstPhoto)
    }

    var allPhotoURLs: [URL] {
        photos?.compactMap { URL(string: APIConfig.baseURL + $0) } ?? []
    }

    var voiceIntroURL: URL? {
        guard let urlString = voiceIntroUrl else { return nil }
        return URL(string: APIConfig.baseURL + urlString)
    }

    func hash(into hasher: inout Hasher) {
        hasher.combine(id)
    }

    static func == (lhs: DiscoveryProfile, rhs: DiscoveryProfile) -> Bool {
        lhs.id == rhs.id
    }
}

// MARK: - Discovery Response
struct DiscoveryResponse: Codable {
    let profiles: [DiscoveryProfile]
    let total: Int?
    let slateId: String?
}

// MARK: - Profile Status
struct ProfileStatus: Codable {
    let isComplete: Bool
    let completion: Int
    let missingFields: [String]?
}

// MARK: - Update Profile Request
struct UpdateProfileRequest: Codable {
    var name: String?
    var dob: String?
    var gender: String?
    var bio: String?
    var interests: [String]?
    var languages: [String]?
    var lookingFor: String?
    var professionCategory: String?
    var professionTitle: String?
    var heightCm: Int?
}

// MARK: - Gender Enum
enum Gender: String, CaseIterable, Codable {
    case male
    case female
    case nonBinary = "non_binary"
    case other

    var displayName: String {
        switch self {
        case .male: return "Male"
        case .female: return "Female"
        case .nonBinary: return "Non-binary"
        case .other: return "Other"
        }
    }
}

// MARK: - Intent Enum
enum DatingIntent: String, CaseIterable, Codable {
    case relationship
    case casual
    case friendship

    var displayName: String {
        switch self {
        case .relationship: return "Relationship"
        case .casual: return "Casual"
        case .friendship: return "Friendship"
        }
    }
}
