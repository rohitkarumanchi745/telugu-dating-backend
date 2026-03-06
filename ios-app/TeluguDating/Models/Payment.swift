import Foundation

// MARK: - Payment Order Request
struct CreateOrderRequest: Codable {
    let productId: String
    let currency: String
    let regionCode: String
    let platform: String
    let idempotencyKey: String
}

// MARK: - Payment Order Response
struct PaymentOrder: Codable {
    let orderId: String
    let gateway: String
    let amountCents: Int64
    let currency: String
    let gatewayOrderId: String?
    let razorpayKeyId: String?
    let clientSecret: String? // For Stripe
}

// MARK: - Verify Payment Request
struct VerifyPaymentRequest: Codable {
    let orderId: String
    let razorpayPaymentId: String?
    let razorpaySignature: String?
    let stripePaymentIntentId: String?
}

// MARK: - Verify Payment Response
struct VerifyPaymentResponse: Codable {
    let success: Bool
    let transactionId: String?
    let message: String?
}

// MARK: - Product
struct Product: Codable, Identifiable {
    let id: String
    let name: String
    let description: String?
    let productType: String
    let prices: [ProductPrice]

    var localizedPrice: String {
        // Default to INR, you can implement locale-based selection
        prices.first(where: { $0.currency == "INR" })?.formattedPrice
            ?? prices.first?.formattedPrice
            ?? "N/A"
    }
}

// MARK: - Product Price
struct ProductPrice: Codable {
    let currency: String
    let amountCents: Int64
    let formattedPrice: String
}

// MARK: - Products Response
struct ProductsResponse: Codable {
    let products: [Product]
}

// MARK: - Subscriptions Response
struct SubscriptionsResponse: Codable {
    let subscriptions: [UserSubscription]
}

// MARK: - User Subscription
struct UserSubscription: Codable, Identifiable {
    let id: String
    let productName: String
    let status: String
    let currentPeriodEnd: String?
    let cancelAtPeriodEnd: Bool?

    var isActive: Bool {
        status == "active"
    }

    var expiryDate: Date? {
        guard let dateString = currentPeriodEnd else { return nil }
        let formatter = ISO8601DateFormatter()
        return formatter.date(from: dateString)
    }
}

// MARK: - Pass Type
enum PassType: String, CaseIterable, Codable {
    case free
    case hourly
    case daily
    case weekly
    case monthly
    case ultra

    var displayName: String {
        switch self {
        case .free: return "Free"
        case .hourly: return "1 Hour"
        case .daily: return "24 Hours"
        case .weekly: return "7 Days"
        case .monthly: return "30 Days"
        case .ultra: return "Unlimited"
        }
    }

    var radiusKm: Double {
        switch self {
        case .free: return 0
        case .hourly: return 2
        case .daily: return 5
        case .weekly: return 10
        case .monthly: return 25
        case .ultra: return Double.infinity
        }
    }
}
