import Foundation

// MARK: - Match
struct Match: Codable, Identifiable, Hashable {
    let matchId: String
    let isMutual: Bool?
    let matchedAt: String?
    let canSendText: Bool?
    let messagesCount: Int?
    let voiceMessagesCount: Int?
    let otherUser: DiscoveryProfile?

    var id: String { matchId }

    var matchedDate: Date? {
        guard let dateString = matchedAt else { return nil }
        let formatter = ISO8601DateFormatter()
        return formatter.date(from: dateString)
    }

    var formattedMatchDate: String {
        guard let date = matchedDate else { return "" }
        let formatter = RelativeDateTimeFormatter()
        formatter.unitsStyle = .abbreviated
        return formatter.localizedString(for: date, relativeTo: Date())
    }

    func hash(into hasher: inout Hasher) {
        hasher.combine(matchId)
    }

    static func == (lhs: Match, rhs: Match) -> Bool {
        lhs.matchId == rhs.matchId
    }
}

// MARK: - Matches Response
struct MatchesResponse: Codable {
    let matches: [Match]
    let total: Int?
}

// MARK: - Like Response
struct LikeResponse: Codable {
    let success: Bool
    let isMutual: Bool?
    let matchId: String?
    let message: String?
    let matchedAt: String?
}

// MARK: - Pass Response
struct PassResponse: Codable {
    let success: Bool
}

// MARK: - Chat Message
struct ChatMessage: Codable, Identifiable, Hashable {
    let id: String
    let matchId: String
    let senderId: Int
    let type: MessageType
    let content: String
    let voiceUrl: String?
    let voiceDuration: Int?
    let createdAt: String
    let isRead: Bool?

    var sentDate: Date {
        let formatter = ISO8601DateFormatter()
        return formatter.date(from: createdAt) ?? Date()
    }

    var formattedTime: String {
        let formatter = DateFormatter()
        formatter.timeStyle = .short
        return formatter.string(from: sentDate)
    }

    var isFromCurrentUser: Bool {
        guard let currentUserId = KeychainManager.shared.getUserId() else { return false }
        return senderId == currentUserId
    }

    func hash(into hasher: inout Hasher) {
        hasher.combine(id)
    }

    static func == (lhs: ChatMessage, rhs: ChatMessage) -> Bool {
        lhs.id == rhs.id
    }
}

// MARK: - Message Type
enum MessageType: String, Codable {
    case text
    case voice
    case image
    case typing
    case readReceipt = "read_receipt"
}

// MARK: - WebSocket Message
struct WebSocketMessage: Codable {
    let type: String
    let content: String?
    let matchId: String?
    let messageId: String?
    let senderId: Int?
    let voiceUrl: String?
    let voiceDuration: Int?
    let timestamp: String?

    // Outgoing message
    init(type: MessageType, content: String, matchId: String) {
        self.type = type.rawValue
        self.content = content
        self.matchId = matchId
        self.messageId = nil
        self.senderId = nil
        self.voiceUrl = nil
        self.voiceDuration = nil
        self.timestamp = nil
    }

    // For voice messages
    init(matchId: String, voiceUrl: String, duration: Int) {
        self.type = MessageType.voice.rawValue
        self.content = nil
        self.matchId = matchId
        self.messageId = nil
        self.senderId = nil
        self.voiceUrl = voiceUrl
        self.voiceDuration = duration
        self.timestamp = nil
    }
}

// MARK: - Call
struct Call: Codable, Identifiable {
    let callId: String
    let callToken: String?
    let expiresIn: Int?

    var id: String { callId }
}

// MARK: - Call Request
struct CallRequest: Codable {
    let matchId: String
    let callType: CallType
}

// MARK: - Call Type
enum CallType: String, Codable {
    case voice
    case video
}
