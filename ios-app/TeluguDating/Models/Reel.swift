import Foundation

// MARK: - Reel
struct Reel: Codable, Identifiable, Hashable {
    let reelId: String
    let userId: Int?
    let title: String?
    let contentUrl: String?
    let createdAt: String?
    let likesCount: Int?
    let messagesCount: Int?
    let isLiked: Bool?
    let tags: [String]?

    var id: String { reelId }

    var videoURL: URL? {
        guard let urlString = contentUrl else { return nil }
        return URL(string: urlString)
    }

    var createdDate: Date? {
        guard let dateString = createdAt else { return nil }
        let formatter = ISO8601DateFormatter()
        return formatter.date(from: dateString)
    }

    func hash(into hasher: inout Hasher) {
        hasher.combine(reelId)
    }

    static func == (lhs: Reel, rhs: Reel) -> Bool {
        lhs.reelId == rhs.reelId
    }
}

// MARK: - Reels Feed Response
struct ReelsFeedResponse: Codable {
    let reels: [Reel]
}

// MARK: - Create Reel Request
struct CreateReelRequest: Codable {
    let title: String
    let contentUrl: String
    let isGlobal: Bool
    let tags: [String]?
}

// MARK: - Create Reel Response
struct CreateReelResponse: Codable {
    let reelId: String
    let success: Bool
}

// MARK: - Reel Message Request
struct ReelMessageRequest: Codable {
    let reelId: String
    let content: String
}

// MARK: - Reel Message Response
struct ReelMessageResponse: Codable {
    let messageId: String
    let success: Bool
}

// MARK: - Reel Conversation
struct ReelConversation: Codable, Identifiable {
    let userId: Int
    let name: String?
    let photo: String?
    let lastMessage: String?
    let unreadCount: Int?
    let lastMessageAt: String?

    var id: Int { userId }

    var photoURL: URL? {
        guard let urlString = photo else { return nil }
        return URL(string: APIConfig.baseURL + urlString)
    }
}

// MARK: - Reels Inbox Response
struct ReelsInboxResponse: Codable {
    let conversations: [ReelConversation]
}

// MARK: - Like Reel Request
struct LikeReelRequest: Codable {
    let reelId: String
}

// MARK: - Unlike Reel Request
struct UnlikeReelRequest: Codable {
    let reelId: String
}
