#!/usr/bin/env python3
"""Generate Telugu Dating Backend Architecture PDF"""

from fpdf import FPDF
import os

class ArchPDF(FPDF):
    def header(self):
        if self.page_no() > 1:
            self.set_font("Helvetica", "I", 8)
            self.set_text_color(120, 120, 120)
            self.cell(0, 8, "Telugu Dating Platform - Architecture Document", align="R")
            self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(120, 120, 120)
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="C")

    def section_title(self, title):
        self.set_font("Helvetica", "B", 16)
        self.set_text_color(26, 26, 80)
        self.cell(0, 12, title, new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(26, 26, 80)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(4)

    def sub_title(self, title):
        self.set_font("Helvetica", "B", 13)
        self.set_text_color(50, 50, 120)
        self.cell(0, 10, title, new_x="LMARGIN", new_y="NEXT")
        self.ln(1)

    def body_text(self, text):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(40, 40, 40)
        self.multi_cell(0, 5.5, text)
        self.ln(2)

    def code_block(self, text):
        self.set_fill_color(240, 240, 245)
        self.set_font("Courier", "", 8)
        self.set_text_color(30, 30, 30)
        x = self.get_x()
        y = self.get_y()
        lines = text.strip().split("\n")
        block_h = len(lines) * 4.5 + 4
        if y + block_h > 270:
            self.add_page()
            y = self.get_y()
        self.rect(10, y, 190, block_h, "F")
        self.set_xy(12, y + 2)
        for line in lines:
            self.cell(0, 4.5, line[:110], new_x="LMARGIN", new_y="NEXT")
            self.set_x(12)
        self.ln(4)

    def bullet(self, text, indent=0):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(40, 40, 40)
        x = 14 + indent
        self.set_x(x)
        self.cell(4, 5.5, "-", new_x="END")
        self.multi_cell(190 - indent - 4, 5.5, f"  {text}")
        self.ln(1)

    def table_row(self, cols, widths, bold=False, fill=False):
        style = "B" if bold else ""
        self.set_font("Helvetica", style, 9)
        if fill:
            self.set_fill_color(230, 230, 245)
        self.set_text_color(30, 30, 30)
        h = 7
        for i, col in enumerate(cols):
            self.cell(widths[i], h, str(col)[:50], border=1, fill=fill)
        self.ln(h)


def generate():
    pdf = ArchPDF()
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=20)

    # ===================== COVER PAGE =====================
    pdf.add_page()
    pdf.ln(50)
    pdf.set_font("Helvetica", "B", 32)
    pdf.set_text_color(26, 26, 80)
    pdf.cell(0, 15, "Telugu Dating Platform", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(5)
    pdf.set_font("Helvetica", "", 20)
    pdf.set_text_color(80, 80, 140)
    pdf.cell(0, 12, "Backend Architecture Document", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(15)
    pdf.set_draw_color(26, 26, 80)
    pdf.line(60, pdf.get_y(), 150, pdf.get_y())
    pdf.ln(15)
    pdf.set_font("Helvetica", "", 12)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 8, "Rust Backend (Axum Framework)", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 8, "Version 1.0", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 8, "February 2026", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(30)
    pdf.set_font("Helvetica", "I", 10)
    pdf.set_text_color(130, 130, 130)
    pdf.cell(0, 8, "Production-grade system designed for 10,000+ concurrent users", align="C", new_x="LMARGIN", new_y="NEXT")

    # ===================== TABLE OF CONTENTS =====================
    pdf.add_page()
    pdf.section_title("Table of Contents")
    pdf.ln(5)
    toc = [
        ("1.", "Technology Stack"),
        ("2.", "High-Level Architecture"),
        ("3.", "Directory Structure"),
        ("4.", "Bootstrap & Startup Flow"),
        ("5.", "Application State"),
        ("6.", "API Endpoints (100+ routes)"),
        ("7.", "Middleware Stack"),
        ("8.", "Database Architecture"),
        ("9.", "Authentication & Security"),
        ("10.", "WebSocket (Real-time)"),
        ("11.", "ML / Vision Pipeline"),
        ("12.", "Payment System"),
        ("13.", "Background Jobs"),
        ("14.", "Configuration"),
        ("15.", "Deployment (Docker + K8s)"),
        ("16.", "Testing Infrastructure"),
    ]
    for num, title in toc:
        pdf.set_font("Helvetica", "", 12)
        pdf.set_text_color(40, 40, 40)
        pdf.cell(12, 8, num)
        pdf.set_text_color(26, 26, 80)
        pdf.cell(0, 8, title, new_x="LMARGIN", new_y="NEXT")

    # ===================== 1. TECH STACK =====================
    pdf.add_page()
    pdf.section_title("1. Technology Stack")
    pdf.ln(2)

    widths = [50, 70, 70]
    pdf.table_row(["Category", "Technology", "Purpose"], widths, bold=True, fill=True)
    rows = [
        ["Web Framework", "Axum 0.8", "HTTP routing & middleware"],
        ["Language", "Rust", "Performance & safety"],
        ["Async Runtime", "Tokio 1", "Async I/O"],
        ["Primary DB", "PostgreSQL + SQLx", "Relational data"],
        ["Graph DB", "Neo4j (HTTP API)", "Social graph & recommendations"],
        ["Cache", "Redis 0.24", "Sessions, rate limiting, pub/sub"],
        ["Auth", "JWT (jsonwebtoken 9)", "Stateless authentication"],
        ["GraphQL", "async-graphql 7.0", "Flexible API queries"],
        ["ML Runtime", "tract-onnx 0.21", "On-device vision models"],
        ["Payments", "Razorpay + Stripe", "India + Global payments"],
        ["Container", "Docker", "Multi-stage builds"],
        ["Orchestration", "Kubernetes", "Scaling & deployment"],
        ["Monitoring", "Prometheus + OpenTelemetry", "Metrics & tracing"],
        ["HTTP Client", "reqwest 0.12", "External API calls"],
    ]
    for r in rows:
        pdf.table_row(r, widths)

    # ===================== 2. HIGH-LEVEL ARCHITECTURE =====================
    pdf.add_page()
    pdf.section_title("2. High-Level Architecture")
    pdf.ln(2)

    arch_diagram = """
+-------------------------------------------------------------------+
|                          CLIENTS                                   |
|    iOS App (Swift)  .  Web App  .  Ambassador Dashboard            |
+----------+----------------+------------------+--------------------+
           |  REST / GraphQL |     WebSocket    |
           v                v                   v
+-------------------------------------------------------------------+
|                   MIDDLEWARE STACK (Axum)                           |
|   CORS > Compression > Tracing > Timeout > Security > Rate Limit   |
+-------------------------------------------------------------------+
                              |
+-------------------------------------------------------------------+
|                       ROUTE HANDLERS                               |
|  Auth  | Profile | Discovery | Chat/Call | Payments | Reels | ML   |
+-------------------------------------------------------------------+
                              |
+-------------------------------------------------------------------+
|                      SERVICE LAYER                                 |
|  AuthService . ProfileService . MatchService . PaymentService      |
|  GraphService . AdsService . AmbassadorService . VisionAnalyzer    |
|  DualWriteManager (Circuit Breaker) . RedisService                 |
+---+----------+------------+----------+----------------------------+
    |          |            |          |
    v          v            v          v
+--------+ +-------+ +---------+ +------------+
|Postgres| | Redis | |  Neo4j  | | ONNX Models|
|  (SQL) | |(Cache)| | (Graph) | |  (Vision)  |
+--------+ +-------+ +---------+ +------------+
                          |
              +-----------+-----------+
              |  External Services    |
              |  Razorpay . Stripe    |
              |  AdMob . RevenueCat   |
              +-----------------------+"""

    pdf.code_block(arch_diagram)

    pdf.body_text(
        "The system follows a layered architecture pattern: "
        "Clients connect via REST, GraphQL, or WebSocket. "
        "Requests pass through the middleware stack (CORS, rate limiting, security headers, tracing). "
        "Route handlers delegate to the service layer, which manages business logic and talks to "
        "PostgreSQL (primary), Redis (cache), Neo4j (graph), and ONNX ML models."
    )

    # ===================== 3. DIRECTORY STRUCTURE =====================
    pdf.add_page()
    pdf.section_title("3. Directory Structure")
    pdf.ln(2)

    dir_struct = """
rust-backend/
  src/
    main.rs                  # Entry point, routing, middleware
    state.rs                 # Shared AppState
    config.rs                # Environment-based configuration
    auth.rs                  # JWT authentication
    error.rs                 # Error handling
    models.rs                # Database row models
    websocket.rs             # WebSocket chat & call handlers
    redis_service.rs         # Redis caching & rate limiting
    storage.rs               # File storage (local / S3 + CloudFront)
    graphql.rs               # GraphQL schema & resolvers
    telemetry.rs             # OpenTelemetry tracing
    vision/
      mod.rs                 # ONNX ML models (NSFW, NIMA, FER+, ArcFace)
    handlers/
      mod.rs                 # Handler exports
      auth.rs                # OTP / phone verification
      common.rs              # Profile, discovery, matching, location, reels
      health.rs              # Health checks & metrics
      payments.rs            # Razorpay + Stripe payment processing
      ads.rs                 # Ad serving & monetization
      ambassador.rs          # Referral program
      graph_handlers.rs      # Neo4j-powered recommendations
    middleware/
      mod.rs                 # Middleware exports
      security.rs            # Security headers & input sanitization
      dual_write.rs          # Circuit breaker for dual-DB writes
    services/
      mod.rs                 # Service exports
      graph_service.rs       # Neo4j + PostgreSQL operations
      neo4j_http.rs          # Neo4j HTTP API client
      ads.rs                 # Ad service logic
      ambassador.rs          # Ambassador service logic
      payments/
        mod.rs               # Payment gateway abstraction
        razorpay.rs          # Razorpay integration (India)
        stripe.rs            # Stripe integration (Global)
        retry.rs             # Exponential backoff & DLQ
    jobs/
      mod.rs                 # Background jobs
      sync_job.rs            # Neo4j <-> PostgreSQL sync
      dlq_processor.rs       # Dead letter queue processor
  migrations/                # 9 SQL migration files
  k8s/                       # Kubernetes deployment configs
  monitoring/                # Prometheus & observability
  Cargo.toml                 # Rust dependencies
  Dockerfile                 # Multi-stage Docker build
  docker-compose.yml         # Local development stack"""

    pdf.code_block(dir_struct)

    # ===================== 4. BOOTSTRAP FLOW =====================
    pdf.add_page()
    pdf.section_title("4. Bootstrap & Startup Flow")
    pdf.ln(2)
    pdf.body_text("The application boots in main.rs with the following sequence:")
    steps = [
        "Load .env configuration via dotenvy",
        "Initialize telemetry / structured logging",
        "Validate config (DB URL, secrets required in production)",
        "Initialize PostgreSQL pool (300 max connections in prod)",
        "Initialize optional read replica pool",
        "Connect to Redis for caching & rate limiting",
        "Load ONNX vision models (NSFW, NIMA, FER+, ArcFace, Liveness)",
        "Connect to Neo4j via HTTP API",
        "Initialize DualWriteManager (circuit breaker)",
        "Create WebSocket chat rooms & call session managers",
        "Initialize payment service (Razorpay + Stripe)",
        "Initialize ads service (AdMob, Facebook, Unity)",
        "Start background jobs: Sync, DLQ Processor, Heartbeat",
        "Build GraphQL schema with dataloaders",
        "Build Axum router with all routes & middleware",
        "Start HTTP server with graceful shutdown support",
    ]
    for i, step in enumerate(steps, 1):
        pdf.set_font("Helvetica", "B", 10)
        pdf.set_text_color(26, 26, 80)
        pdf.cell(10, 6, f"{i}.")
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(40, 40, 40)
        pdf.cell(0, 6, step, new_x="LMARGIN", new_y="NEXT")

    # ===================== 5. APPLICATION STATE =====================
    pdf.ln(6)
    pdf.section_title("5. Application State (AppState)")
    pdf.ln(2)
    pdf.body_text(
        "All shared resources are held in AppState, passed to every handler via Axum's "
        "state extraction. This enables zero-cost dependency injection."
    )
    state_code = """
pub struct AppState {
    pub db: PgPool,                                // PostgreSQL connection pool
    pub redis: Option<ConnectionManager>,           // Redis cache
    pub neo4j: Option<Arc<Graph>>,                  // Neo4j Bolt (optional)
    pub graph_service: Option<Arc<GraphService>>,   // Neo4j HTTP service
    pub dual_write: Arc<DualWriteManager>,          // Fault-tolerant dual writes
    pub config: Config,                             // Runtime configuration
    pub vision: Option<Arc<Mutex<VisionAnalyzer>>>, // ML vision models
    pub chat_rooms: Arc<RwLock<ChatRooms>>,         // WebSocket chat rooms
    pub call_sessions: Arc<RwLock<CallSessions>>,   // WebSocket call sessions
    pub metrics: Arc<AppMetrics>,                   // Atomic metrics counters
    pub payment_service: Option<Arc<PaymentService>>,
    pub ads_service: Option<Arc<AdsService>>,
}"""
    pdf.code_block(state_code)

    # ===================== 6. API ENDPOINTS =====================
    pdf.add_page()
    pdf.section_title("6. API Endpoints (100+ routes)")
    pdf.ln(2)

    # Auth
    pdf.sub_title("Authentication")
    widths = [25, 55, 20, 90]
    pdf.table_row(["Method", "Endpoint", "Auth", "Description"], widths, bold=True, fill=True)
    pdf.table_row(["POST", "/send-otp", "No", "Send OTP to phone number"], widths)
    pdf.table_row(["POST", "/verify-otp", "No", "Verify OTP, returns JWT token"], widths)
    pdf.ln(3)

    # Profile
    pdf.sub_title("User Profile")
    pdf.table_row(["Method", "Endpoint", "Auth", "Description"], widths, bold=True, fill=True)
    pdf.table_row(["GET", "/profile/me", "Yes", "Get current user full profile"], widths)
    pdf.table_row(["GET", "/profile/status", "Yes", "Profile completion (0-100%)"], widths)
    pdf.table_row(["POST", "/update-profile", "Yes", "Update profile + photos (multipart)"], widths)
    pdf.table_row(["POST", "/update-bio", "Yes", "Update user bio"], widths)
    pdf.table_row(["POST", "/preferences", "Yes", "Update matching preferences"], widths)
    pdf.ln(3)

    # Discovery
    pdf.sub_title("Discovery & Matching")
    pdf.table_row(["Method", "Endpoint", "Auth", "Description"], widths, bold=True, fill=True)
    pdf.table_row(["GET", "/discover", "Yes", "Get discovery feed (10 profiles)"], widths)
    pdf.table_row(["POST", "/match/like", "Yes", "Like user (creates match if mutual)"], widths)
    pdf.table_row(["POST", "/match/pass", "Yes", "Pass/skip a user"], widths)
    pdf.table_row(["GET", "/matches", "Yes", "Get all mutual matches"], widths)
    pdf.table_row(["GET", "/match/{id}", "Yes", "Get match details"], widths)
    pdf.ln(3)

    # Location
    pdf.sub_title("Location")
    pdf.table_row(["Method", "Endpoint", "Auth", "Description"], widths, bold=True, fill=True)
    pdf.table_row(["POST", "/location/update", "Yes", "Update user location (GPS)"], widths)
    pdf.table_row(["GET", "/location/search", "Yes", "Search locations by name"], widths)
    pdf.table_row(["GET", "/location/nearby", "Yes", "Get nearby users with distance"], widths)
    pdf.table_row(["POST", "/location/purchase-pass", "Yes", "Buy location discovery pass"], widths)
    pdf.ln(3)

    # Reels
    pdf.add_page()
    pdf.sub_title("Reels (Private Message Dating)")
    pdf.table_row(["Method", "Endpoint", "Auth", "Description"], widths, bold=True, fill=True)
    pdf.table_row(["POST", "/reels", "Yes", "Create a reel"], widths)
    pdf.table_row(["GET", "/reels/feed", "Yes", "Get reel feed"], widths)
    pdf.table_row(["POST", "/reels/like", "Yes", "Like a reel"], widths)
    pdf.table_row(["POST", "/reels/message", "Yes", "Send message on a reel"], widths)
    pdf.table_row(["GET", "/reels/inbox", "Yes", "Get reel conversations"], widths)
    pdf.table_row(["GET", "/reels/conversation", "Yes", "Get conversation thread"], widths)
    pdf.ln(3)

    # Payments
    pdf.sub_title("Payments (Razorpay + Stripe)")
    pdf.table_row(["Method", "Endpoint", "Auth", "Description"], widths, bold=True, fill=True)
    pdf.table_row(["POST", "/api/payments/create-order", "Yes", "Create payment order"], widths)
    pdf.table_row(["POST", "/api/payments/verify", "Yes", "Verify payment"], widths)
    pdf.table_row(["GET", "/api/payments/products", "Yes", "List products & pricing"], widths)
    pdf.table_row(["GET", "/api/payments/subscriptions", "Yes", "Get user subscriptions"], widths)
    pdf.table_row(["POST", "/webhook/razorpay", "No", "Razorpay webhook"], widths)
    pdf.table_row(["POST", "/webhook/stripe", "No", "Stripe webhook"], widths)
    pdf.ln(3)

    # Voice & Calls
    pdf.sub_title("Voice Intro & Calls")
    pdf.table_row(["Method", "Endpoint", "Auth", "Description"], widths, bold=True, fill=True)
    pdf.table_row(["POST", "/voice-intro", "Yes", "Upload voice intro (multipart)"], widths)
    pdf.table_row(["POST", "/calls", "Yes", "Initialize voice/video call"], widths)
    pdf.table_row(["WS", "/ws/chat", "Yes", "Real-time messaging"], widths)
    pdf.table_row(["WS", "/ws/call", "Yes", "WebRTC call signaling"], widths)
    pdf.ln(3)

    # ML
    pdf.sub_title("ML / Federated Learning")
    pdf.table_row(["Method", "Endpoint", "Auth", "Description"], widths, bold=True, fill=True)
    pdf.table_row(["POST", "/ml/embeddings", "Yes", "Update user embedding"], widths)
    pdf.table_row(["POST", "/ml/reward", "Yes", "Log reward signal"], widths)
    pdf.table_row(["POST", "/fl/register", "Yes", "Register FL client"], widths)
    pdf.table_row(["POST", "/fl/update", "Yes", "Submit FL model update"], widths)
    pdf.table_row(["GET", "/fl/model", "Yes", "Get active FL model"], widths)
    pdf.table_row(["POST", "/verify/selfie", "Yes", "Liveness selfie verification"], widths)
    pdf.ln(3)

    # Ambassador
    pdf.sub_title("Ambassador Program")
    pdf.table_row(["Method", "Endpoint", "Auth", "Description"], widths, bold=True, fill=True)
    pdf.table_row(["POST", "/api/ambassador/login", "No", "Ambassador login"], widths)
    pdf.table_row(["GET", "/api/ambassador/me", "Yes", "Ambassador profile"], widths)
    pdf.table_row(["GET", "/api/ambassador/performance", "Yes", "Performance metrics"], widths)
    pdf.table_row(["GET", "/api/ambassador/leaderboard", "Yes", "Top ambassadors"], widths)
    pdf.table_row(["POST", "/api/referral/record", "Yes", "Record referral"], widths)
    pdf.ln(3)

    # Health
    pdf.sub_title("Health & Monitoring")
    pdf.table_row(["Method", "Endpoint", "Auth", "Description"], widths, bold=True, fill=True)
    pdf.table_row(["GET", "/health", "No", "Basic health check"], widths)
    pdf.table_row(["GET", "/health/detailed", "No", "Extended health metrics"], widths)
    pdf.table_row(["GET", "/ready", "No", "Kubernetes readiness probe"], widths)
    pdf.table_row(["GET", "/metrics", "No", "Prometheus metrics"], widths)
    pdf.table_row(["POST", "/graphql", "Yes", "GraphQL endpoint"], widths)

    # ===================== 7. MIDDLEWARE =====================
    pdf.add_page()
    pdf.section_title("7. Middleware Stack")
    pdf.ln(2)
    pdf.body_text("Requests pass through middleware in this order (bottom layer first):")

    mw = [
        ("1. Security Headers", "X-Frame-Options: DENY, HSTS, CSP, X-Content-Type-Options, "
         "Referrer-Policy, Permissions-Policy, Cache-Control"),
        ("2. Rate Limiting", "Redis-based sliding window: 120 req/min (prod), "
         "60 req/min (dev). Premium users get 2x. Returns 429 + Retry-After header."),
        ("3. Metrics", "Track total/active requests, error counts, WebSocket connections."),
        ("4. Request ID", "Generate X-Request-ID (UUID) for distributed tracing."),
        ("5. Compression", "Gzip response compression."),
        ("6. Request Timeout", "Global 30-second timeout per request."),
        ("7. Tracing", "Tower HTTP structured logging with latency tracking."),
        ("8. CORS", "Dev: allow all origins. Prod: configurable whitelist with credentials."),
        ("9. Dual-Write", "Circuit breaker state injection for database availability."),
    ]
    for title, desc in mw:
        pdf.set_font("Helvetica", "B", 10)
        pdf.set_text_color(26, 26, 80)
        pdf.cell(0, 6, title, new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(60, 60, 60)
        pdf.set_x(14)
        pdf.multi_cell(180, 5, desc)
        pdf.ln(2)

    # ===================== 8. DATABASE =====================
    pdf.add_page()
    pdf.section_title("8. Database Architecture")
    pdf.ln(2)

    pdf.sub_title("PostgreSQL (Primary)")
    pdf.body_text(
        "300 max connections in production (50 min). PgBouncer-compatible transaction pooling. "
        "Optional read replica for read-heavy queries. 9 migration files."
    )

    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(26, 26, 80)
    pdf.cell(0, 7, "Core Tables:", new_x="LMARGIN", new_y="NEXT")
    core_tables = [
        "users - User profiles with embeddings & scores",
        "user_preferences - Discovery filters & preferences",
        "user_locations - Geolocation with fuzzy/exact modes",
        "matches - Mutual matches between users",
        "messages - Text messages in matches",
        "voice_messages - Voice messages with sentiment",
        "voice_intros - User voice introductions",
        "reels - Short-form video profiles",
        "reel_messages - Private messages on reels",
        "spots - Location-based date spots",
        "calls - Video/voice call records",
        "user_swipes - Like/Pass/Block interactions",
    ]
    for t in core_tables:
        pdf.bullet(t)

    pdf.ln(2)
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(26, 26, 80)
    pdf.cell(0, 7, "Payment Tables:", new_x="LMARGIN", new_y="NEXT")
    pay_tables = [
        "payment_gateways - Multi-gateway config (Razorpay, Stripe)",
        "products / product_prices - Catalog with regional pricing",
        "payment_orders / payment_transactions - Order & transaction records",
        "subscriptions - Subscription management",
        "dead_letter_queue - Failed payment retry queue",
    ]
    for t in pay_tables:
        pdf.bullet(t)

    pdf.ln(2)
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(26, 26, 80)
    pdf.cell(0, 7, "University & Student Tables:", new_x="LMARGIN", new_y="NEXT")
    uni_tables = [
        "universities - University directory",
        "student_verification - Verification status by tier",
        "university_passes - Location-based discovery passes",
    ]
    for t in uni_tables:
        pdf.bullet(t)

    pdf.ln(4)
    pdf.sub_title("Redis (Cache & Sessions)")
    redis_items = [
        "Session caching (7-day TTL)",
        "OTP storage (5-minute TTL)",
        "User profile caching (1-hour TTL)",
        "Rate limiting (sliding window sorted sets)",
        "Online status (5-minute TTL)",
        "Distributed locking (30-second locks)",
        "WebSocket instance routing (user -> server mapping)",
        "Pub/Sub for cross-instance events",
    ]
    for item in redis_items:
        pdf.bullet(item)

    pdf.ln(4)
    pdf.sub_title("Neo4j (Graph Database)")
    pdf.body_text(
        "Connected via HTTP API (Neo4j 5.x compatible). Used for social graph "
        "analysis, friend-of-friend matching, shared interest discovery, and "
        "university relationship graphs. Dual-write with circuit breaker ensures "
        "fault tolerance."
    )
    graph_schema = """
Nodes: User, University, Location, Interest
Relationships: LIKED, MATCHED_WITH, BLOCKED_BY, ATTENDS_UNIVERSITY,
               LIVES_IN, SHARED_INTEREST, MUTUAL_FRIEND"""
    pdf.code_block(graph_schema)

    # ===================== 9. AUTH & SECURITY =====================
    pdf.add_page()
    pdf.section_title("9. Authentication & Security")
    pdf.ln(2)

    pdf.sub_title("Authentication Flow")
    pdf.body_text(
        "Phone-based OTP authentication. User sends phone number, receives OTP, "
        "verifies it, and receives a JWT access token."
    )
    jwt_code = """
JWT Claims {
    sub: String,              // user_id
    exp: usize,               // expiration (7 days default)
    scope: Option<String>,    // "call", "refresh", or None
    match_id: Option<String>, // for call tokens
    call_id: Option<String>,  // for call tokens
    is_admin: bool,           // admin flag
}

Header: Authorization: Bearer <access_token>"""
    pdf.code_block(jwt_code)

    pdf.sub_title("Input Validation & Sanitization")
    validations = [
        "validate_phone(): +prefix, 10-15 digits",
        "validate_email(): Basic RFC format check",
        "sanitize_input(): Remove control chars, limit to 10k chars",
        "sanitize_for_display(): HTML entity encoding (XSS prevention)",
        "IP extraction: X-Forwarded-For, X-Real-IP, CF-Connecting-IP",
        "Data redaction: Phone/email masking in logs",
    ]
    for v in validations:
        pdf.bullet(v)

    # ===================== 10. WEBSOCKET =====================
    pdf.ln(4)
    pdf.section_title("10. WebSocket (Real-time)")
    pdf.ln(2)

    pdf.sub_title("Chat WebSocket (/ws/chat)")
    chat_items = [
        "JWT authenticated via query parameter",
        "Per-match broadcast channels (HashMap<match_id, Sender>)",
        "Message types: text, voice, typing, read_receipt, system",
        "Auto-cleanup of empty rooms",
        "Buffer size: 500 messages (production)",
    ]
    for item in chat_items:
        pdf.bullet(item)

    pdf.ln(2)
    pdf.sub_title("Call WebSocket (/ws/call)")
    call_items = [
        "WebRTC signaling channel",
        "Signal types: offer, answer, ice, join, leave, end",
        "JSON payload for SDP/ICE candidates",
        "Buffer size: 200 signals (production)",
        "Max 5 WebSocket connections per user",
    ]
    for item in call_items:
        pdf.bullet(item)

    # ===================== 11. VISION/ML =====================
    pdf.add_page()
    pdf.section_title("11. ML / Vision Pipeline")
    pdf.ln(2)
    pdf.body_text(
        "Five ONNX models run locally for real-time image analysis. "
        "No external API dependency for ML inference."
    )

    widths3 = [50, 40, 100]
    pdf.table_row(["Model", "Input Size", "Purpose"], widths3, bold=True, fill=True)
    pdf.table_row(["NSFW Detection", "224x224", "Binary classification for inappropriate content"], widths3)
    pdf.table_row(["FER+ (Emotion)", "64x64", "Facial emotion recognition (smile detection)"], widths3)
    pdf.table_row(["NIMA (Aesthetic)", "224x224", "Image quality & attractiveness scoring"], widths3)
    pdf.table_row(["ArcFace", "112x112", "512-dim face embedding for verification"], widths3)
    pdf.table_row(["Liveness", "80x80", "Anti-spoofing for selfie verification"], widths3)
    pdf.ln(3)

    vision_output = """
VisionAnalysis {
    attractiveness_score: f32,   // 0-1, aesthetic quality
    authenticity_score: f32,     // 0-1, liveness check
    quality_score: f32,          // 0-1, overall quality
    inappropriate_content: bool, // NSFW flag
    face_detected: bool,         // face presence
    smile_intensity: f32,        // 0-1, smile detection
    style_embedding: Vec<f32>,   // 512-dim face embedding
}

Thresholds:
  - Selfie match: 0.45 (ArcFace cosine similarity)
  - Liveness: 0.50 (anti-spoofing confidence)"""
    pdf.code_block(vision_output)

    pdf.ln(2)
    pdf.sub_title("Federated Learning")
    fl_items = [
        "Privacy-preserving ML training across user devices",
        "Min 10 clients before starting a round",
        "10% client fraction selected per round",
        "Differential Privacy enabled (noise multiplier: 1.0, clip norm: 1.0)",
        "Endpoints: /fl/register, /fl/round, /fl/update, /fl/aggregate, /fl/model",
    ]
    for item in fl_items:
        pdf.bullet(item)

    # ===================== 12. PAYMENTS =====================
    pdf.add_page()
    pdf.section_title("12. Payment System")
    pdf.ln(2)

    pdf.sub_title("Dual Gateway Architecture")
    pdf.body_text(
        "Razorpay for India (INR), Stripe for global users. "
        "Multi-currency support: INR, USD, EUR, GBP, AED, SGD, AUD. "
        "Automatic gateway selection based on region_code."
    )

    payment_flow = """
Payment Flow:
  1. Client calls POST /api/payments/create-order
  2. Server determines gateway (India -> Razorpay, else -> Stripe)
  3. Creates order in payment_orders table
  4. Calls gateway API to create order/intent
  5. Returns payment link/intent to client
  6. Client completes payment on gateway
  7. Gateway calls webhook (POST /webhook/razorpay or /webhook/stripe)
  8. Server validates signature, updates order status
  9. Grants subscription/product to user
  10. Failed operations queued to DLQ for retry"""
    pdf.code_block(payment_flow)

    pdf.sub_title("Fault Tolerance")
    fault_items = [
        "Dead Letter Queue (DLQ) for failed payment operations",
        "Exponential backoff with jitter for retries",
        "Idempotency keys to prevent duplicate charges",
        "Webhook retry logic for missed events",
        "DLQ processor runs as background job",
    ]
    for item in fault_items:
        pdf.bullet(item)

    pdf.ln(3)
    pdf.sub_title("Location Pass Pricing")
    widths4 = [35, 35, 40, 80]
    pdf.table_row(["Pass Type", "Duration", "Radius", "Description"], widths4, bold=True, fill=True)
    pdf.table_row(["Free", "Unlimited", "0 km", "Default - no location discovery"], widths4)
    pdf.table_row(["Hourly", "1 hour", "2 km", "Short-term nearby discovery"], widths4)
    pdf.table_row(["Daily", "24 hours", "5 km", "Day pass for local discovery"], widths4)
    pdf.table_row(["Weekly", "7 days", "10 km", "Week-long expanded radius"], widths4)
    pdf.table_row(["Monthly", "30 days", "25 km", "Monthly wide-area discovery"], widths4)
    pdf.table_row(["Ultra", "Unlimited", "Infinite", "Unlimited discovery everywhere"], widths4)

    # ===================== 13. BACKGROUND JOBS =====================
    pdf.add_page()
    pdf.section_title("13. Background Jobs")
    pdf.ln(2)

    pdf.sub_title("Sync Job (sync_job.rs)")
    pdf.body_text(
        "Periodically synchronizes data between Neo4j and PostgreSQL. "
        "Runs initial sync on startup if Neo4j is available. "
        "Drains queued operations from the dual-write manager."
    )

    pdf.sub_title("DLQ Processor (dlq_processor.rs)")
    pdf.body_text(
        "Processes failed payment operations from the dead letter queue. "
        "Uses exponential backoff strategy with configurable max attempts. "
        "Handles webhook retries for Razorpay and Stripe."
    )

    pdf.sub_title("Instance Heartbeat")
    pdf.body_text(
        "Every 15 seconds, registers this instance in Redis with a 30-second TTL. "
        "Key format: instance:{instance_id}. Enables horizontal scaling with "
        "WebSocket routing to the correct server instance."
    )

    # ===================== 14. CIRCUIT BREAKER =====================
    pdf.ln(2)
    pdf.section_title("14. Circuit Breaker (Dual-Write Manager)")
    pdf.ln(2)

    cb_diagram = """
Circuit Breaker States:

  CLOSED (normal) --[5 failures]--> OPEN (failing)
       ^                               |
       |                          [30s timeout]
       |                               |
       +---[3 successes]--- HALF-OPEN <-+
                           (testing)

  - Separate circuit breaker per database (PostgreSQL + Neo4j)
  - Queues failed operations (up to 10k per DB)
  - Background sync drains queued operations
  - DualWriteResult: any_success() / all_success() / has_queued()"""
    pdf.code_block(cb_diagram)

    # ===================== 15. DEPLOYMENT =====================
    pdf.add_page()
    pdf.section_title("15. Deployment (Docker + Kubernetes)")
    pdf.ln(2)

    pdf.sub_title("Docker")
    docker_items = [
        "Multi-stage build: Rust 1.76 builder -> debian:bookworm-slim runtime",
        "Stripped release binary for minimal image size",
        "Non-root user: appuser (UID 1000)",
        "Exposed port: 8080",
        "Health check via Kubernetes readiness probe",
    ]
    for item in docker_items:
        pdf.bullet(item)

    pdf.ln(3)
    pdf.sub_title("Kubernetes")
    k8s_items = [
        "3 replicas (configurable) with rolling updates",
        "Resource limits: 2 CPU, 2GB RAM per pod",
        "Resource requests: 0.5 CPU, 512MB RAM per pod",
        "Readiness & liveness probes via /ready and /live",
        "Graceful shutdown: 30-second timeout",
        "Pod Disruption Budget for high availability",
        "Network policies to restrict ingress/egress",
        "Persistent volumes for uploads, models, DB data",
        "ConfigMap for environment variables",
        "Secrets for credentials (JWT key, DB password, API keys)",
    ]
    for item in k8s_items:
        pdf.bullet(item)

    pdf.ln(3)
    pdf.sub_title("Monitoring & Observability")
    mon_items = [
        "Prometheus metrics at /metrics endpoint",
        "Structured JSON logging in production",
        "OpenTelemetry tracing (optional feature flag)",
        "Key metrics: requests_total, errors_total, cache_hits/misses, "
        "websocket_connections, db_pool_size, dlq_entries_pending",
    ]
    for item in mon_items:
        pdf.bullet(item)

    pdf.ln(3)
    pdf.sub_title("Environment Modes")
    widths5 = [40, 50, 100]
    pdf.table_row(["Mode", "Rate Limit", "Characteristics"], widths5, bold=True, fill=True)
    pdf.table_row(["development", "60 req/min", "Debug logging, test payments, relaxed validation"], widths5)
    pdf.table_row(["staging", "120 req/min", "Production settings, test payments"], widths5)
    pdf.table_row(["production", "120 req/min", "Strict validation, real payments, JSON logs"], widths5)

    # ===================== 16. TESTING =====================
    pdf.add_page()
    pdf.section_title("16. Testing Infrastructure")
    pdf.ln(2)
    pdf.body_text(
        "The platform has a comprehensive, production-grade testing suite spanning 7 main test files "
        "plus inline tests across 5 source modules. Over 3,500 lines of test code covering "
        "50+ individual test cases across 8 testing methodologies."
    )

    # Test types overview table
    pdf.sub_title("Test Types Overview")
    widths_t = [35, 15, 70, 70]
    pdf.table_row(["Type", "Count", "Location", "Purpose"], widths_t, bold=True, fill=True)
    pdf.table_row(["Unit", "30+", "tests/api_tests.rs", "Individual function validation"], widths_t)
    pdf.table_row(["Integration", "5+", "tests/api_tests.rs", "Database operations"], widths_t)
    pdf.table_row(["Security", "8+", "tests/api_tests.rs + inline", "Attack pattern detection"], widths_t)
    pdf.table_row(["E2E", "5", "tests/e2e/user_flows.rs", "Complete user flows"], widths_t)
    pdf.table_row(["Contract", "15+", "tests/contract/", "API schema validation"], widths_t)
    pdf.table_row(["Load", "4", "tests/load/k6-load-test.js", "Performance under load"], widths_t)
    pdf.table_row(["Smoke", "20+", "tests/smoke/smoke_tests.sh", "Quick health checks"], widths_t)
    pdf.table_row(["Fuzz", "8", "tests/fuzz/fuzz_targets.rs", "Random input crash detection"], widths_t)
    pdf.table_row(["Chaos", "10", "tests/chaos/chaos_tests.sh", "Resilience testing"], widths_t)
    pdf.ln(4)

    # Test file structure
    pdf.sub_title("Test File Structure")
    test_struct = """
rust-backend/
  tests/
    api_tests.rs             # 30+ unit, integration & security tests
    common/
      mod.rs                 # Test utilities, fixtures, TestClient
  src/ (inline tests)
    middleware/security.rs   # 6 security middleware tests
    middleware/dual_write.rs # Circuit breaker tests
    storage.rs               # 2 storage service tests
    jobs/dlq_processor.rs    # 2 DLQ processing tests
    services/payments/retry.rs # 3 payment retry tests

tests/ (parent directory)
  e2e/
    user_flows.rs            # 5 end-to-end user flow tests
  contract/
    api_contract_tests.rs    # 15+ API contract tests
  load/
    k6-load-test.js          # k6 load test (4 scenarios)
  smoke/
    smoke_tests.sh           # 20+ smoke tests (bash)
  fuzz/
    fuzz_targets.rs          # 8 fuzz test targets
  chaos/
    chaos_tests.sh           # 10 chaos/resilience tests"""
    pdf.code_block(test_struct)

    # Unit Tests
    pdf.add_page()
    pdf.sub_title("Unit Tests (api_tests.rs - 30+ tests)")
    pdf.body_text(
        "Core business logic validation using Rust's built-in #[test] framework."
    )
    unit_areas = [
        "JWT token creation and validation (user + admin)",
        "Phone number validation (valid/invalid formats, +prefix, 10-15 digits)",
        "Email validation (RFC format checking)",
        "Age calculation with 18+ enforcement",
        "Compatibility score calculation (preference matching)",
        "Haversine distance calculation between coordinates",
        "Interest overlap scoring",
        "Pass pricing (hourly, daily, weekly, monthly, ultra)",
        "Student discount tiers (Ivy: 30%, Top50: 20%, State: 10%, Alumni: 15%)",
        "Rate limiting key generation",
        "Gender validation (male, female, non_binary, other)",
        "Token expiration handling",
        "Input sanitization (control chars, length limits)",
        "UUID generation and validation",
        "Date parsing and JSON serialization",
    ]
    for item in unit_areas:
        pdf.bullet(item)

    # Security Tests
    pdf.ln(3)
    pdf.sub_title("Security Tests (8+ tests)")
    pdf.body_text("Attack pattern detection and security hardening validation.")
    sec_tests = [
        "JWT token tampering detection (modified payload)",
        "Different secret key verification (rejects wrong key)",
        "Admin privilege escalation prevention",
        "SQL injection pattern detection (DROP TABLE, UNION SELECT, etc.)",
        "XSS pattern detection (<script>, javascript:, onerror=)",
        "Path traversal prevention (../, /etc/passwd)",
        "Command injection detection (;, |, &&, backticks)",
        "Phone number and email redaction in logs",
    ]
    for item in sec_tests:
        pdf.bullet(item)

    # E2E Tests
    pdf.add_page()
    pdf.sub_title("End-to-End Tests (5 complete flows)")
    pdf.body_text(
        "Full user journey tests using reqwest HTTP client against the running API."
    )

    e2e_flows = [
        ("1. User Registration", "OTP send -> OTP verify -> JWT token -> Profile completion -> "
         "Photo upload -> Selfie verification"),
        ("2. Discovery & Matching", "Load discover feed -> View profiles -> Like/Pass actions -> "
         "Check mutual matches -> Match details"),
        ("3. Chat Flow", "Get matches -> Load conversation history -> Send text message -> "
         "Verify message delivery -> Read receipt"),
        ("4. Premium Subscription", "Check subscription status -> Get available plans -> "
         "Create payment intent -> Verify payment -> Activate subscription"),
        ("5. Student Verification", "Check verification status -> Search universities -> "
         "Submit .edu email -> Verify OTP -> Apply discount tier"),
    ]
    for title, desc in e2e_flows:
        pdf.set_font("Helvetica", "B", 10)
        pdf.set_text_color(26, 26, 80)
        pdf.cell(0, 6, title, new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(60, 60, 60)
        pdf.set_x(14)
        pdf.multi_cell(180, 5, desc)
        pdf.ln(2)

    # Contract Tests
    pdf.ln(2)
    pdf.sub_title("Contract Tests (15+ schema validations)")
    pdf.body_text(
        "API response schema validation ensuring backward compatibility. "
        "Custom JSON schema checker validates required fields, types, and structure."
    )
    contract_items = [
        "User profile schema (required fields: id, name, age, photos, is_verified)",
        "Auth response schema (access_token, user_id, is_new_user)",
        "Match response schema (match_id, is_mutual, other_user)",
        "Discovery response schema (profiles array, total count)",
        "Swipe response schema (success, is_mutual, match_id)",
        "Message schema (id, sender_id, content, type, created_at)",
        "Error response schema (detail field, HTTP status codes)",
        "Subscription status schema",
        "Nullable field handling (optional fields accepted as null)",
        "Backward compatibility (extra fields don't break parsing)",
    ]
    for item in contract_items:
        pdf.bullet(item)

    # Load Tests
    pdf.add_page()
    pdf.sub_title("Load Tests (k6 - 4 scenarios)")
    pdf.body_text(
        "Performance testing using k6. Ramps from 10 to 50 to 100 virtual users "
        "over 6+ minutes with custom latency metrics per endpoint."
    )

    widths_l = [50, 20, 120]
    pdf.table_row(["Scenario", "Weight", "Flow"], widths_l, bold=True, fill=True)
    pdf.table_row(["New User Registration", "30%", "OTP -> Verify -> Profile update"], widths_l)
    pdf.table_row(["Active User Browsing", "30%", "Discover -> View profiles -> Swipe"], widths_l)
    pdf.table_row(["Matching & Chatting", "20%", "Get matches -> Messages -> Send"], widths_l)
    pdf.table_row(["Profile Updates", "20%", "Get profile -> Update bio -> Location"], widths_l)
    pdf.ln(3)

    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(26, 26, 80)
    pdf.cell(0, 7, "Performance Thresholds:", new_x="LMARGIN", new_y="NEXT")
    widths_p = [80, 50, 60]
    pdf.table_row(["Metric", "Threshold", "Target"], widths_p, bold=True, fill=True)
    pdf.table_row(["p95 Response Time", "< 500ms", "General API"], widths_p)
    pdf.table_row(["p99 Response Time", "< 1000ms", "General API"], widths_p)
    pdf.table_row(["Error Rate", "< 10%", "All requests"], widths_p)
    pdf.table_row(["Auth Latency (p95)", "< 300ms", "OTP/Verify endpoints"], widths_p)
    pdf.table_row(["Discover Latency (p95)", "< 800ms", "Discovery feed"], widths_p)
    pdf.table_row(["Profile Latency (p95)", "< 200ms", "Profile endpoints"], widths_p)
    pdf.table_row(["Match Latency (p95)", "< 300ms", "Match endpoints"], widths_p)

    # Fuzz Tests
    pdf.ln(4)
    pdf.sub_title("Fuzz Tests (8 targets)")
    pdf.body_text(
        "Randomized input testing using cargo-fuzz (requires nightly Rust). "
        "Detects crashes, panics, and undefined behavior with random inputs."
    )
    fuzz_targets = [
        "fuzz_json_parser - Malformed JSON handling",
        "fuzz_phone_validator - Invalid phone formats",
        "fuzz_email_validator - Invalid email formats",
        "fuzz_jwt_decoder - Malformed JWT tokens",
        "fuzz_url_parser - Arbitrary path parsing",
        "fuzz_date_parser - Invalid date strings",
        "fuzz_sanitizer - XSS payload prevention",
        "fuzz_haversine - Numerical edge cases (NaN, Infinity)",
    ]
    for item in fuzz_targets:
        pdf.bullet(item)

    # Smoke Tests
    pdf.add_page()
    pdf.sub_title("Smoke Tests (20+ checks)")
    pdf.body_text(
        "Quick bash-based health checks for deployment validation. "
        "Color-coded output. Run against any environment."
    )
    smoke_cats = [
        "Infrastructure: /health, /ready, /live endpoints",
        "Auth Endpoints: /send-otp, /verify-otp reachability",
        "Public Endpoints: /universities, /subscription/plans",
        "Protected Endpoints: all return 401 without auth token",
        "GraphQL: introspection query validation",
        "Microservices: optional external service health",
        "Response Time: all critical endpoints < configured threshold",
    ]
    for item in smoke_cats:
        pdf.bullet(item)

    # Chaos Tests
    pdf.ln(3)
    pdf.sub_title("Chaos Tests (10 resilience scenarios)")
    pdf.body_text(
        "Infrastructure resilience testing via Docker and system tools. "
        "Validates graceful degradation and recovery under failure conditions."
    )
    chaos_scenarios = [
        ("1. Database Failure", "Stop PostgreSQL, verify API returns 503, restart, verify recovery"),
        ("2. Kafka Failure", "Stop Kafka broker, verify message queue fallback"),
        ("3. Service Restart", "Kill and restart API server, verify zero downtime"),
        ("4. Network Latency", "Inject 200ms latency with tc, verify timeout handling"),
        ("5. Memory Pressure", "Consume 90% memory, verify OOM handling"),
        ("6. Disk Pressure", "Fill disk to 95%, verify write failure handling"),
        ("7. Cascading Failure", "Kill multiple dependencies, verify partial service"),
        ("8. Dependency Timeout", "Slow external APIs, verify circuit breaker activation"),
        ("9. Graceful Degradation", "Disable Neo4j, verify PostgreSQL-only operation"),
        ("10. RTO Validation", "Full restart, verify recovery < 30 seconds"),
    ]
    for title, desc in chaos_scenarios:
        pdf.set_font("Helvetica", "B", 9)
        pdf.set_text_color(26, 26, 80)
        pdf.cell(45, 5.5, title, new_x="END")
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(60, 60, 60)
        pdf.multi_cell(145, 5.5, "- " + desc)
        pdf.ln(1)

    # Test Utilities
    pdf.ln(3)
    pdf.sub_title("Test Utilities (tests/common/mod.rs)")
    pdf.body_text("Shared test helpers and fixtures for consistent test setup.")
    test_utils = """
TestConfig {
    database_url: String,
    redis_url: String,
    secret_key: String,
    bind_addr: String,
}

TestClient {
    get(url) -> Response
    get_with_auth(url, token) -> Response
    post_json(url, body) -> Response
    post_json_with_auth(url, body, token) -> Response
}

Helpers:
    create_test_token(user_id) -> JWT (1-hour expiry)
    create_admin_test_token(user_id) -> Admin JWT
    setup_test_db() -> PgPool (with auto-migration)
    cleanup_test_user(phone) -> ()
    generate_test_phone() -> unique phone number"""
    pdf.code_block(test_utils)

    # How to Run Tests
    pdf.add_page()
    pdf.sub_title("How to Run Tests")
    pdf.ln(2)

    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(26, 26, 80)
    pdf.cell(0, 7, "Rust Tests (cargo):", new_x="LMARGIN", new_y="NEXT")
    cargo_cmds = """
# Run all unit tests
cargo test

# Run with database (integration tests)
export TEST_DATABASE_URL="postgres://user:pass@localhost:5432/test_db"
cargo test -- --ignored

# Run specific module
cargo test unit_tests
cargo test security_tests
cargo test integration_tests -- --ignored

# Run E2E tests
cargo test --test user_flows -- --ignored

# Run contract tests
cargo test --test api_contract_tests"""
    pdf.code_block(cargo_cmds)

    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(26, 26, 80)
    pdf.cell(0, 7, "Load Tests (k6):", new_x="LMARGIN", new_y="NEXT")
    k6_cmds = """
# Basic load test
k6 run tests/load/k6-load-test.js

# Custom VUs and duration
k6 run --vus 50 --duration 2m tests/load/k6-load-test.js

# With environment variables
k6 run -e BASE_URL=http://api.example.com -e TEST_TOKEN=xxx tests/load/k6-load-test.js

# Stress test (200 virtual users)
k6 run --vus 200 --duration 1m tests/load/k6-load-test.js"""
    pdf.code_block(k6_cmds)

    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(26, 26, 80)
    pdf.cell(0, 7, "Smoke & Chaos Tests (bash):", new_x="LMARGIN", new_y="NEXT")
    bash_cmds = """
# Smoke tests (requires running server)
./tests/smoke/smoke_tests.sh http://localhost:8080

# Chaos tests (requires Docker)
./tests/chaos/chaos_tests.sh http://localhost:8080

# Chaos tests with destructive DB/Kafka scenarios
RUN_DESTRUCTIVE=true ./tests/chaos/chaos_tests.sh"""
    pdf.code_block(bash_cmds)

    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(26, 26, 80)
    pdf.cell(0, 7, "Fuzz Tests (cargo-fuzz, nightly):", new_x="LMARGIN", new_y="NEXT")
    fuzz_cmds = """
# List fuzz targets
cargo +nightly fuzz list

# Run specific fuzz target
cargo +nightly fuzz run fuzz_json_parser
cargo +nightly fuzz run fuzz_phone_validator
cargo +nightly fuzz run fuzz_jwt_decoder"""
    pdf.code_block(fuzz_cmds)

    # Test Coverage Summary
    pdf.ln(3)
    pdf.sub_title("Test Coverage by Area")
    widths_c = [60, 60, 70]
    pdf.table_row(["Area", "Test Types", "Coverage"], widths_c, bold=True, fill=True)
    pdf.table_row(["Authentication", "Unit, Security, E2E, Smoke", "JWT, OTP, tokens"], widths_c)
    pdf.table_row(["User Profiles", "Unit, Integration, E2E", "CRUD, validation, photos"], widths_c)
    pdf.table_row(["Matching/Discovery", "Unit, E2E, Load, Contract", "Scoring, distance, feed"], widths_c)
    pdf.table_row(["Security", "Security, Fuzz", "SQLi, XSS, traversal, CSRF"], widths_c)
    pdf.table_row(["Payments", "Unit, E2E, Contract", "Pricing, discounts, orders"], widths_c)
    pdf.table_row(["Chat/WebSocket", "E2E, Load", "Messages, typing, delivery"], widths_c)
    pdf.table_row(["Infrastructure", "Smoke, Chaos", "Health, recovery, degradation"], widths_c)
    pdf.table_row(["Performance", "Load", "Latency, throughput, VUs"], widths_c)
    pdf.table_row(["Input Handling", "Fuzz, Unit", "Crash detection, edge cases"], widths_c)

    # ===================== OUTPUT =====================
    output_path = os.path.expanduser(
        "~/Downloads/telugu-dating-backend-main/Telugu_Dating_Architecture.pdf"
    )
    pdf.output(output_path)
    print(f"PDF generated: {output_path}")
    return output_path


if __name__ == "__main__":
    generate()
