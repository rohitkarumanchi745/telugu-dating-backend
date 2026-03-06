# Nava — AI-Powered Dating Platform Backend

Production Python backend powering the Nava dating platform. Built with **FastAPI**, **PostgreSQL**, **Redis**, real-time **WebSocket** chat & calling, **GraphQL** (Strawberry), ML-powered matching (PyTorch), computer vision verification, and location-based discovery.

## Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                        Client Applications                         │
│   ┌──────────────┐   ┌───────────────────┐   ┌────────────────┐   │
│   │   iOS App    │   │  React Native App │   │   Ambassador   │   │
│   │  (SwiftUI)   │   │    (Expo / RN)    │   │   Dashboard    │   │
│   └──────┬───────┘   └────────┬──────────┘   └───────┬────────┘   │
└──────────┼────────────────────┼───────────────────────┼────────────┘
           └────────────────────┼───────────────────────┘
                                │
                    ┌───────────▼───────────┐
                    │  FastAPI Application  │
                    │  (main.py — Uvicorn)  │
                    │                       │
                    │  REST · GraphQL · WS  │
                    │  JWT · CORS · OAuth2  │
                    └───────────┬───────────┘
                                │
        ┌───────────┬───────────┼───────────┬───────────┐
        ▼           ▼           ▼           ▼           ▼
   ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐
   │  Auth   │ │ Profile │ │ Match & │ │  Chat   │ │ Payment │
   │  (OTP)  │ │ & Media │ │Discovery│ │ & Calls │ │ & Passes│
   └────┬────┘ └────┬────┘ └────┬────┘ └────┬────┘ └────┬────┘
        └───────────┴───────────┼───────────┴───────────┘
                                │
        ┌───────────────────────┼───────────────────────┐
        ▼                       ▼                        ▼
  ┌───────────┐          ┌───────────┐           ┌───────────┐
  │PostgreSQL │          │   Redis   │           │  Uploads  │
  │ (psycopg2)│          │  (Cache,  │           │  (Local / │
  │  Users,   │          │   OTP,    │           │    S3)    │
  │  Matches, │          │  Sessions)│           │           │
  │  Messages │          └───────────┘           └───────────┘
  └───────────┘

  ┌─────────────────────────────────────────────────┐
  │              ML / AI Layer (PyTorch)             │
  │                                                  │
  │  ┌──────────┐  ┌───────────┐  ┌──────────────┐ │
  │  │ Matching │  │ Computer  │  │   LinUCB      │ │
  │  │  Intel.  │  │  Vision   │  │   Contextual  │ │
  │  │  (RL +   │  │ (ResNet,  │  │   Bandit      │ │
  │  │Federated)│  │ ViT, NSFW)│  │  (Ranking)    │ │
  │  └──────────┘  └───────────┘  └──────────────┘ │
  └─────────────────────────────────────────────────┘
```

## Tech Stack

| Layer | Technologies |
|-------|-------------|
| **Framework** | Python 3.9, FastAPI, Uvicorn, Pydantic v2 |
| **API** | REST + GraphQL (Strawberry) + WebSocket |
| **Database** | PostgreSQL 15 (psycopg2 raw SQL, connection pooling) |
| **Cache** | Redis 7 (OTP, sessions, location, rate limiting) |
| **Auth** | Phone OTP + JWT (python-jose), OAuth2 bearer |
| **ML/AI** | PyTorch, scikit-learn, NumPy, Pandas |
| **Computer Vision** | OpenCV, face-recognition (dlib), PIL, custom ResNet/ViT |
| **Payments** | Stripe, Apple StoreKit 2, RevenueCat, Razorpay |
| **Real-Time** | WebSocket (chat messaging, call signaling, live location) |
| **gRPC** | grpcio + protobuf (inter-service communication) |
| **Infrastructure** | Docker, Docker Compose |

## Project Structure

```
├── main.py                          # FastAPI app — all REST + WS endpoints
├── graphql_schema.py                # Strawberry GraphQL schema & resolvers
├── models.py                        # SQLAlchemy ORM models (User, Match, Message, etc.)
├── models_reco.py                   # Recommendation engine models (embeddings, interactions)
├── db_raw.py                        # psycopg2 connection pool + raw SQL helpers
├── database.py                      # SQLAlchemy engine setup
├── auth.py                          # JWT token utilities
├── event_bus.py                     # In-process event emitter
├── schemas.py                       # Pydantic request/response schemas
├── ml_models.py                     # PyTorch ML models (ResNet, ViT, matching, federated learning)
├── core/
│   └── matching_intelligence.py     # RL agent (Q-learning) + federated learning for matching
├── vision/
│   ├── models.py                    # Computer vision: ResNet, EfficientNet, ViT, NSFW detection
│   └── face_verification.py         # Real-time selfie liveness + face match verification
├── location/
│   ├── location_matcher.py          # Nationwide geo matching, heatmaps, path optimization
│   ├── pass_manager.py              # Location pass management (hourly/daily/weekly/monthly)
│   └── student_discounts.py         # University-tiered student verification & pricing
├── services/
│   └── linucb.py                    # LinUCB contextual bandit for content ranking
├── grpc_server.py                   # gRPC server for inter-service calls
├── grpc_client.py                   # gRPC client
├── protos/                          # Protocol buffer definitions
├── ambassador-dashboard/            # React/TypeScript analytics dashboard
├── tests/                           # E2E, load, contract, smoke, fuzz, chaos tests
├── Dockerfile                       # Python container (python:3.9-slim)
├── docker-compose.yml               # PostgreSQL + Redis + API
├── requirements.txt                 # Python dependencies
└── scripts/                         # Utility scripts
```

## API Endpoints

### Authentication (REST)
| Endpoint | Method | Auth | Description |
|----------|--------|------|-------------|
| `/send-otp` | POST | No | Send OTP to phone number |
| `/verify-otp` | POST | No | Verify OTP → JWT access token |

### Profile Management (REST)
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/update-profile` | POST | Update name, dob, gender, bio, location, interests, photos |
| `/update-bio` | POST | Quick bio update |
| `/profile/me` | GET | Get authenticated user profile |
| `/profile/status` | GET | Profile completion status |
| `/verify/selfie` | POST | Selfie liveness + face verification (multipart) |

### Discovery & Matching (REST)
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/discover` | GET | AI-powered profile discovery with compatibility scoring |
| `/match/like` | POST | Like a user → returns `{ isMutual, matchId }` |
| `/match/pass` | POST | Pass on a user |
| `/match/{match_id}` | GET | Get match details with message history |

### Location Services (REST)
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/location/update` | POST | Update GPS coordinates (lat, lng, city, state, country) |
| `/location/nearby` | GET | Find nearby matches within pass radius |
| `/location/purchase-pass` | POST | Buy location pass (hourly/daily/weekly/monthly) |
| `/location/search` | GET | Search locations by name |

### Student Verification (REST)
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/student/verify` | POST | Send OTP to .edu email |
| `/student/status` | GET | Check verification status & tier |

### Video Spots (REST)
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/spots` | POST | Upload video spot (mp4, max 30s) |
| `/spots` | GET | List video feed |

### Calls (REST)
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/calls` | POST | Initiate audio/video call → `{ callId, token, signalingUrl }` |

### WebSocket Endpoints
| Endpoint | Description |
|----------|-------------|
| `/ws/chat?match_id=&token=` | Real-time chat (message, typing, read receipts) |
| `/ws/call?call_id=&match_id=&token=` | Call signaling (ringing, joined, left) |
| `/ws/location/{user_id}` | Live location updates |

### GraphQL (`/graphql`)
| Operation | Type | Description |
|-----------|------|-------------|
| `sendOtp` | Mutation | Send phone OTP |
| `verifyOtp` | Mutation | Verify OTP → access token |
| `me` | Query | Get authenticated user profile |
| `updateProfile` | Mutation | Update profile fields |
| `discover` | Query | AI-powered discovery with filters |
| `likeUser` | Mutation | Like → check mutual match |
| `passUser` | Mutation | Pass on user |
| `matches` | Query | Get all matches with partner details |
| `conversation` | Query | Load message history |
| `sendChatMessage` | Mutation | Send chat message |
| `verifySelfie` | Mutation | Selfie liveness verification |
| `myPreferences` | Query | Get dating preferences |
| `savePreferences` | Mutation | Save min/max age, distance, gender filters |

### Admin
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/admin/stats` | GET | System statistics (users, matches, messages, etc.) |
| `/health` | GET | Health check |

## ML & AI Architecture

### Matching Intelligence (`core/matching_intelligence.py`)
- **Q-Learning RL Agent** — Learns optimal match recommendations per user based on swipe outcomes
- **User Feature Vectors** — Age, gender, activity score, selectivity, bio sentiment, photo attractiveness, location cluster
- **Federated Learning** — Privacy-preserving model aggregation across clients with differential privacy (noise multiplier + gradient clipping)
- **Reward Signal** — Mutual matches = high reward, one-way likes = medium, passes = low

### Computer Vision Pipeline (`vision/`)
- **ResNet + EfficientNet + Vision Transformer** — Multi-model ensemble for photo analysis
- **Attractiveness scoring** (0-1), **authenticity detection** (real vs filtered), **quality scoring**
- **Selfie Liveness Detection** — Anti-spoofing with face embedding comparison
- **NSFW Content Moderation** — Flags inappropriate content before it's visible
- **Face Recognition** — dlib-based face encoding + cosine similarity matching

### LinUCB Contextual Bandit (`services/linucb.py`)
- Ranks spots/users in discovery feed using exploration-exploitation trade-off
- 16-dimensional feature vectors with upper confidence bound scoring
- Per-user arm state stored in `bandit_arm_stats` database table
- Observation decay (0.995) for adapting to changing user preferences

### Recommendation Engine (`models_reco.py`)
- 512-dim user embeddings (short-term + long-term behavioral)
- Interaction tracking across surfaces: discover, playground, search, profile
- Collaborative filtering based on engagement rates and creator affinities

## Database Schema (Key Tables)

```
users            — id, phone, email, name, dob, gender, bio, location, interests,
                   languages, photos, height, profession, looking_for, verified
user_preferences — user_id, min_age, max_age, max_distance_km, preferred_genders
matches          — id (UUID), user_a, user_b, is_mutual, status, matched_at
messages         — id, match_id, sender_id, receiver_id, content, is_read, created_at
user_locations   — user_id, lat, lng, city, state, country, accuracy, updated_at
location_passes  — user_id, pass_type, radius_miles, expires_at, payment_id
subscriptions    — user_id, tier (gold/platinum/ultra), platform, expires_at
student_verifications — user_id, university, tier, verified_at
spots            — id, user_id, video_url, caption, like_count, view_count, expires_at
bandit_arm_stats — arm_id, arm_type, user_id, A_matrix, b_vector, pulls, reward
```

## Revenue Model

### Subscription Tiers
| Tier | Features |
|------|----------|
| **Gold** | Unlimited likes, see who likes you, 5 super likes/day, 1 boost/month |
| **Platinum** | All Gold + priority matching, read receipts, weekly boost, undo swipe |
| **Ultra** | All Platinum + priority support, exclusive events, unlimited super likes |

### Location Passes
| Pass | Duration | Radius |
|------|----------|--------|
| Hourly | 1 hr | 2 mi |
| Daily | 24 hr | 5 mi |
| Weekly | 7 days | 10 mi |
| Monthly | 30 days | 25 mi |
| Ultra | Unlimited | Unlimited |

### Student Discounts
| Tier | Discount |
|------|----------|
| Ivy / Top Private | 30% |
| Top 50 Public | 20% |
| State University | 15% |
| Graduate Student | 15% |
| Other (.edu) | 10% |
| Alumni | 5% |

### Payment Gateways
Apple StoreKit 2 (iOS) · RevenueCat (cross-platform) · Stripe (global) · Razorpay (India)

## Quick Start

```bash
# 1. Start PostgreSQL + Redis
docker compose up -d db redis

# 2. Install Python dependencies
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 3. Set environment variables
export DATABASE_URL=postgresql://nava:nava@localhost:5432/nava
export REDIS_URL=redis://localhost:6379/0
export SECRET_KEY=your-secret-key

# 4. Run the server
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Docker
```bash
docker compose -f docker-compose.python.yml up -d
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `DATABASE_URL` | `postgresql://nava:nava@localhost:5432/nava` | PostgreSQL connection |
| `REDIS_URL` | `redis://localhost:6379/0` | Redis connection |
| `SECRET_KEY` | — | JWT signing secret |
| `STRIPE_API_KEY` | — | Stripe payments |

## Testing

```bash
tests/e2e/run_tests.sh          # End-to-end user flows
tests/load/k6 run load_tests.js # k6 load tests
tests/contract/run_tests.sh     # API contract validation
tests/smoke/run_tests.sh        # Health checks
```

## API Base URLs

| Environment | HTTP | WebSocket |
|-------------|------|-----------|
| Development | `http://localhost:8000` | `ws://localhost:8000` |
| Production | `https://api.nava.app` | `wss://api.nava.app` |
