"""
AI-Powered Dating App with Computer Vision, Location Features, and Student Discounts
Version 3.0.0
"""

import os
import shutil
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
import uuid
from fastapi import FastAPI, UploadFile, File, Form, Depends, HTTPException, Body, Query, BackgroundTasks, WebSocket, WebSocketDisconnect, Request
from strawberry.fastapi import GraphQLRouter
from graphql_schema import schema as graphql_schema
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import create_engine, and_, or_
from sqlalchemy.orm import sessionmaker, Session
from jose import jwt, JWTError
from pydantic import BaseModel, field_validator
from enum import Enum
import logging
import asyncio
import numpy as np
import cv2
import redis
from decimal import Decimal

# Import existing ML components
from ml_models import matching_intelligence, UserFeatures, UserFeatureExtractor
from models import Base, User, Match, Message, UserPreferences

# Import NEW components
from core.matching_intelligence import MatchingIntelligence
from vision.models import DatingAppVisionAnalyzer, ImageAnalysisResult
from vision.face_verification import RealTimeSelfieVerification, SelfieVerificationResult
from location.pass_manager import EnhancedLocationPassManager, PassType, LocationPass
from location.location_matcher import NationwideLocationMatcher, HeatmapGenerator, PathOptimizer
from location.student_discounts import (
    StudentVerificationSystem,
    integrate_student_discounts,
    StudentTier,
    STUDENT_PASS_CONFIGS
)

# --- Config ---
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
STRIPE_API_KEY = os.getenv("STRIPE_API_KEY", "sk_test_your_key")

# Allow Postgres/MySQL/etc. without sqlite-only connect args
CONNECT_ARGS = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, connect_args=CONNECT_ARGS)
SessionLocal = sessionmaker(bind=engine)

Base.metadata.create_all(bind=engine)

# Setup Redis
try:
    redis_client = redis.from_url(REDIS_URL)
    redis_client.ping()
except:
    redis_client = None
    print("⚠️ Redis not available - using in-memory cache")

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

print("🤖 AI-Powered Dating App Starting...")
print("📸 Computer Vision Models Loading...")
print("📍 Location Services Initializing...")
print("🎓 Student Discount System Ready...")

# --- Initialize Enhanced Components ---

# Vision Components
vision_analyzer = DatingAppVisionAnalyzer()

# Location Components
pass_manager = EnhancedLocationPassManager(redis_client=redis_client, stripe_api_key=STRIPE_API_KEY)
pass_manager = integrate_student_discounts(pass_manager)  # Add student discounts
location_matcher = NationwideLocationMatcher(pass_manager)
heatmap_generator = HeatmapGenerator(location_matcher)
path_optimizer = PathOptimizer(location_matcher)

# Selfie Verification
verification_system = RealTimeSelfieVerification(
    vision_analyzer=vision_analyzer,
    rl_agent=matching_intelligence.rl_agent,
    federated_manager=matching_intelligence.federated_manager
)

# Enhanced matching intelligence with vision
matching_intelligence.vision_analyzer = vision_analyzer

print("✅ All systems loaded successfully!")

# --- Pydantic Models ---
class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"
    NON_BINARY = "non_binary"
    OTHER = "other"

class UserProfile(BaseModel):
    id: int
    name: str
    age: int
    gender: str
    bio: Optional[str] = None
    photos: List[str] = []
    distance: Optional[float] = None
    ai_score: Optional[float] = None
    city: Optional[str] = None  # NEW
    verification_status: Optional[str] = None  # NEW
    student_verified: Optional[bool] = None  # NEW

class LocationUpdateRequest(BaseModel):
    latitude: float
    longitude: float
    accuracy: float = 10.0

class PurchasePassRequest(BaseModel):
    pass_type: str  # 'hourly', 'daily', 'weekly', 'monthly', 'ultra'
    payment_method: str
    promo_code: Optional[str] = None

class StudentVerificationRequest(BaseModel):
    email: str
    student_id: Optional[str] = None

class SelfieVerificationRequest(BaseModel):
    selfie_image: str  # Base64 encoded image

class LikeRequest(BaseModel):
    target_user_id: int

# --- App setup ---
app = FastAPI(
    title="AI-Powered Dating App API",
    version="3.0.0",
    description="Dating app with AI/ML, Computer Vision, Location Features, and Student Discounts"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve uploaded images
if not os.path.exists("uploads"):
    os.makedirs("uploads")
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# --- Helper Functions (keep existing) ---
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user_id(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = int(payload.get("sub"))
        return user_id
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

def calculate_age(birth_date):
    today = datetime.now().date()
    return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

def compute_profile_completion(user: User) -> int:
    """Compute a simple profile completion percentage based on filled fields and photos."""
    checks = [
        bool(user.name),
        bool(user.dob),
        bool(user.gender),
        bool(user.bio),
        bool(user.profile_photo_1 or user.profile_photo_2 or user.profile_photo_3),
        bool(user.voice_intro_url),
    ]
    filled = sum(1 for c in checks if c)
    total = len(checks) or 1
    return int(round((filled / total) * 100))

def get_or_create_match(user_id: int, target_user_id: int, db: Session) -> Match:
    match = db.query(Match).filter(
        or_(
            and_(Match.user1_id == user_id, Match.user2_id == target_user_id),
            and_(Match.user1_id == target_user_id, Match.user2_id == user_id)
        )
    ).first()
    if not match:
        match = Match(
            id=str(uuid.uuid4()),
            user1_id=user_id,
            user2_id=target_user_id,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        db.add(match)
        db.flush()
    return match

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# GraphQL context per request
def graphql_context(request: Request):
    db = SessionLocal()
    try:
        yield {"db": db, "request": request}
    finally:
        db.close()

# GraphQL endpoint
graphql_app = GraphQLRouter(graphql_schema, context_getter=graphql_context)
app.include_router(graphql_app, prefix="/graphql")

# --- Enhanced Feature Extraction with Vision ---
def extract_user_features_from_db(user_id: int, db: Session) -> Optional[UserFeatures]:
    """Extract user features for ML models from database with vision analysis"""
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user or not user.dob:
            return None
        
        # Calculate basic features (keep existing)
        age = calculate_age(user.dob)
        gender_map = {"male": 0.0, "female": 1.0, "non_binary": 0.5, "other": 0.5}
        gender_encoded = gender_map.get(user.gender, 0.5)
        
        # Calculate activity score
        recent_matches = db.query(Match).filter(
            or_(Match.user1_id == user_id, Match.user2_id == user_id),
            Match.created_at > datetime.now() - timedelta(days=30)
        ).count()
        activity_score = min(recent_matches / 50.0, 1.0)
        
        # Calculate selectivity
        total_swipes = db.query(Match).filter(Match.user1_id == user_id).count()
        likes_given = db.query(Match).filter(Match.user1_id == user_id, Match.liked == True).count()
        selectivity_score = 1 - (likes_given / max(total_swipes, 1))
        
        # Bio sentiment (enhanced with actual analysis if needed)
        bio_sentiment = 0.0
        if user.bio:
            positive_words = ['love', 'happy', 'fun', 'adventure', 'smile', 'joy']
            negative_words = ['hate', 'sad', 'boring', 'tired', 'angry']
            bio_lower = user.bio.lower()
            pos_count = sum(1 for word in positive_words if word in bio_lower)
            neg_count = sum(1 for word in negative_words if word in bio_lower)
            bio_sentiment = (pos_count - neg_count) / max(len(user.bio.split()), 1)
        
        # NEW: Photo attractiveness using vision analyzer
        photo_attractiveness = 0.5  # Default
        if user.profile_photo_url:
            photos = user.profile_photo_url.split(',')
            if photos:
                try:
                    # Analyze first photo with vision model
                    with open(photos[0], 'rb') as f:
                        photo_data = f.read()
                    analysis = vision_analyzer.analyze_image(photo_data)
                    photo_attractiveness = analysis.attractiveness_score
                except Exception as e:
                    logger.error(f"Error analyzing photo: {e}")
        
        # Location cluster
        location_cluster = hash(str(user_id)) % 10
        
        return UserFeatures(
            age=float(age),
            gender_encoded=gender_encoded,
            activity_score=activity_score,
            selectivity_score=selectivity_score,
            bio_sentiment=bio_sentiment,
            photo_attractiveness=photo_attractiveness,
            location_cluster=location_cluster
        )
    except Exception as e:
        logger.error(f"Error extracting features for user {user_id}: {e}")
        return None

# Update the feature extractor
class EnhancedDatabaseFeatureExtractor(UserFeatureExtractor):
    def __init__(self):
        super().__init__()
        self.db_session = SessionLocal()
    
    def _extract_features_from_db(self, user_id: int) -> Optional[UserFeatures]:
        return extract_user_features_from_db(user_id, self.db_session)

# Replace the feature extractor
matching_intelligence.feature_extractor = EnhancedDatabaseFeatureExtractor()

# --- Keep existing authentication endpoints ---
@app.post("/send-otp")
def send_otp(phone_number: str, db: Session = Depends(get_db)):
    """Send OTP to phone number (currently mocked)"""
    # Keep existing implementation
    try:
        user = db.query(User).filter_by(phone_number=phone_number).first()
        if not user:
            user = User(phone_number=phone_number)
            db.add(user)
            db.commit()
        
        logger.info(f"OTP request for {phone_number}")
        return {"message": "OTP sent successfully", "otp": "1234"}
    except Exception as e:
        logger.error(f"Error sending OTP: {e}")
        raise HTTPException(status_code=500, detail="Failed to send OTP")

@app.post("/verify-otp")
def verify_otp(phone_number: str, otp: str, db: Session = Depends(get_db)):
    """Verify OTP and return access token"""
    # Keep existing implementation
    if otp != "1234":
        raise HTTPException(status_code=400, detail="Invalid OTP")
    
    user = db.query(User).filter_by(phone_number=phone_number).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    token = create_access_token(
        {"sub": str(user.id)}, 
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    
    return {
        "access_token": token,
        "token_type": "bearer",
        "user_id": user.id,
        "is_profile_complete": bool(user.name and user.dob)
    }

# --- Enhanced Profile with Photo Analysis ---
@app.post("/update-profile")
async def update_profile(
    name: str = Form(...),
    dob: str = Form(...),
    gender: str = Form(...),
    profile_photo_1: UploadFile = File(...),
    profile_photo_2: UploadFile = File(...),
    profile_photo_3: UploadFile = File(...),
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db),
    background_tasks: BackgroundTasks = BackgroundTasks()
):
    """Update user profile with photo analysis"""
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Validate date and gender (keep existing)
        dob_obj = datetime.strptime(dob, "%Y-%m-%d").date()
        age = calculate_age(dob_obj)
        if age < 18:
            raise HTTPException(status_code=400, detail="Must be at least 18 years old")

        if gender.lower() not in [g.value for g in Gender]:
            raise HTTPException(status_code=400, detail="Invalid gender")

        upload_dir = "uploads"
        os.makedirs(upload_dir, exist_ok=True)

        # Save and analyze photos
        filenames = []
        photo_analyses = []
        
        for idx, photo in enumerate([profile_photo_1, profile_photo_2, profile_photo_3], start=1):
            if not photo.content_type.startswith('image/'):
                raise HTTPException(status_code=400, detail=f"Photo {idx} must be an image")
            
            filename = f"{user_id}_photo_{idx}_{int(datetime.now().timestamp())}.jpg"
            file_path = os.path.join(upload_dir, filename)
            
            # Save photo
            with open(file_path, "wb") as buffer:
                content = await photo.read()
                buffer.write(content)
            
            filenames.append(file_path)
            
            # Analyze photo with vision model
            try:
                analysis = vision_analyzer.analyze_image(content)
                photo_analyses.append(analysis)
                
                # Check for inappropriate content
                if analysis.inappropriate_content:
                    os.remove(file_path)
                    raise HTTPException(status_code=400, detail=f"Photo {idx} contains inappropriate content")
            except Exception as e:
                logger.error(f"Error analyzing photo {idx}: {e}")

        # Update user
        user.name = name
        user.dob = dob_obj
        user.gender = gender.lower()
        user.profile_photo_url = ",".join(filenames)
        
        # Store average attractiveness score
        if photo_analyses:
            avg_attractiveness = np.mean([a.attractiveness_score for a in photo_analyses])
            user.attractiveness_score = avg_attractiveness  # Add this field to your User model
        
        db.commit()
        user.is_profile_complete = True
        try:
            db.commit()
        except:
            db.rollback()
        
        # Clear ML feature cache
        matching_intelligence.feature_extractor.extract_user_features(user_id, force_refresh=True)
        
        # Get photo insights
        insights = []
        for analysis in photo_analyses:
            insights.append({
                "quality": analysis.quality_score,
                "smile_detected": analysis.smile_intensity > 0.5,
                "authenticity": analysis.authenticity_score
            })
        
        logger.info(f"Profile updated for user {user_id} with photo analysis")
        
        return {
            "message": "Profile updated successfully",
            "photos": filenames,
            "photo_insights": insights
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating profile: {e}")
        raise HTTPException(status_code=500, detail="Failed to update profile")

# --- NEW: Selfie Verification Endpoint ---
@app.post("/verify/selfie")
async def verify_selfie(
    selfie: UploadFile = File(...),
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Verify user identity with real-time selfie"""
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user or not user.profile_photo_url:
            raise HTTPException(status_code=400, detail="Complete your profile first")
        
        # Read selfie
        selfie_data = await selfie.read()
        selfie_array = np.frombuffer(selfie_data, np.uint8)
        selfie_image = cv2.imdecode(selfie_array, cv2.IMREAD_COLOR)
        
        # Get user's stored photos
        stored_photos = []
        for photo_path in user.profile_photo_url.split(','):
            if os.path.exists(photo_path):
                img = cv2.imread(photo_path)
                if img is not None:
                    stored_photos.append(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        
        if not stored_photos:
            raise HTTPException(status_code=400, detail="No valid photos found")
        
        # Perform verification
        result = await verification_system.verify_realtime_selfie(
            user_id=user_id,
            selfie_image=cv2.cvtColor(selfie_image, cv2.COLOR_BGR2RGB),
            stored_photos=stored_photos
        )
        
        # Update user verification status
        if result.is_match:
            user.is_verified = True
            user.verified_at = datetime.now()
            db.commit()
        
        return {
            "verified": result.is_match,
            "confidence": result.confidence_score,
            "liveness_score": result.liveness_score,
            "face_match_score": result.face_match_score,
            "failure_reasons": result.failure_reasons if not result.is_match else None
        }
        
    except Exception as e:
        logger.error(f"Selfie verification error: {e}")
        raise HTTPException(status_code=500, detail="Verification failed")

# --- NEW: Location Endpoints ---
@app.post("/location/update")
async def update_location(
    request: LocationUpdateRequest,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Update user's location"""
    try:
        # Update location in matcher
        location_matcher.update_user_location(
            user_id=user_id,
            latitude=request.latitude,
            longitude=request.longitude,
            accuracy=request.accuracy
        )
        
        # Check pass status
        has_pass = pass_manager.has_active_pass(user_id)
        search_radius = pass_manager.get_enhanced_radius(user_id)
        
        # Get location info
        location = location_matcher.user_locations.get(user_id)
        
        response = {
            "success": True,
            "has_active_pass": has_pass,
            "search_radius": search_radius,
            "location_updated": datetime.now().isoformat()
        }
        
        # Add city info for premium users
        if location and pass_manager.can_see_city_names(user_id):
            response["your_location"] = {
                "city": location.city,
                "state": location.state
            }
        
        return response
        
    except Exception as e:
        logger.error(f"Location update error: {e}")
        raise HTTPException(status_code=500, detail="Failed to update location")

@app.post("/location/purchase-pass")
async def purchase_location_pass(
    request: PurchasePassRequest,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Purchase a location pass with student discount if applicable"""
    try:
        pass_type = PassType[request.pass_type.upper()]
    except KeyError:
        raise HTTPException(status_code=400, detail="Invalid pass type")
    
    # Process purchase (student discounts applied automatically)
    result = await pass_manager.purchase_pass(
        user_id=user_id,
        pass_type=pass_type,
        payment_method=request.payment_method,
        promo_code=request.promo_code
    )
    
    if not result['success']:
        raise HTTPException(status_code=400, detail=result['error'])
    
    return result

@app.get("/location/nearby")
async def get_nearby_matches(
    limit: int = Query(20, le=100),
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Get nearby matches based on location and pass status"""
    try:
        # Get matches from location matcher
        matches = await location_matcher.find_nationwide_matches(
            user_id=user_id,
            max_results=limit
        )
        
        # Enhance with user data
        enhanced_matches = []
        for match in matches:
            user = db.query(User).filter(User.id == match['user_id']).first()
            if user:
                age = calculate_age(user.dob) if user.dob else None
                photos = user.profile_photo_url.split(',')[:1] if user.profile_photo_url else []
                
                enhanced_match = {
                    "id": user.id,
                    "name": user.name,
                    "age": age,
                    "photos": photos,
                    "distance": match['distance_display'],
                    "location": match['location_display']
                }
                
                # Add exact distance for premium users
                if 'exact_distance' in match:
                    enhanced_match['exact_distance'] = match['exact_distance']
                
                # Add city for premium users
                if 'city' in match:
                    enhanced_match['city'] = match['city']
                    enhanced_match['state'] = match.get('state')
                
                enhanced_matches.append(enhanced_match)
        
        # Get pass info
        has_pass = pass_manager.has_active_pass(user_id)
        
        return {
            "matches": enhanced_matches,
            "has_premium": has_pass,
            "total_found": len(enhanced_matches)
        }
        
    except Exception as e:
        logger.error(f"Error getting nearby matches: {e}")
        raise HTTPException(status_code=500, detail="Failed to get matches")

# --- NEW: Student Verification Endpoints ---
@app.post("/student/verify")
async def verify_student_status(
    request: StudentVerificationRequest,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Verify student status for discounts"""
    result = await pass_manager.student_verification.verify_student_email(
        user_id=user_id,
        email=request.email,
        student_id=request.student_id
    )
    
    if not result['success']:
        raise HTTPException(status_code=400, detail=result['error'])
    
    # Update user record
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        user.is_student_verified = True
        user.university = result['verification']['university']
        db.commit()
    
    return result

@app.get("/student/status")
async def get_student_status(
    user_id: int = Depends(get_current_user_id)
):
    """Get student verification status and available discounts"""
    verification = pass_manager.student_verification.get_student_status(user_id)
    
    if not verification:
        return {
            "verified": False,
            "message": "Not verified as student"
        }
    
    tier = StudentTier(verification.discount_tier)
    config = STUDENT_PASS_CONFIGS[tier]
    
    return {
        "verified": True,
        "university": verification.university_name,
        "tier": verification.discount_tier,
        "expiry_date": verification.expiry_date.isoformat(),
        "discount_percentage": config['discount_percentage'],
        "special_prices": config['pass_prices'],
        "special_features": config['special_features']
    }

# --- Enhanced Discovery with Location and Vision ---
@app.get("/discover")
async def discover_users(
    limit: int = Query(10, le=50),
    use_ai: bool = Query(True),
    use_location: bool = Query(True),
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Get AI-powered potential matches with location and vision analysis"""
    current_user = db.query(User).filter(User.id == user_id).first()
    if not current_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Get location-based matches if enabled
    if use_location:
        location_matches = await location_matcher.find_nationwide_matches(
            user_id=user_id,
            max_results=limit * 2
        )
        
        # Convert to user IDs
        location_user_ids = [m['user_id'] for m in location_matches]
        
        # Prioritize location-based matches
        query = db.query(User).filter(
            User.id.in_(location_user_ids),
            User.id != user_id,
            User.name.isnot(None),
            User.dob.isnot(None)
        )
    else:
        # Original query logic
        matched_user_ids = db.query(Match.user2_id).filter(
            Match.user1_id == user_id
        ).union(
            db.query(Match.user1_id).filter(Match.user2_id == user_id)
        ).subquery()
        
        query = db.query(User).filter(
            User.id != user_id,
            User.name.isnot(None),
            User.dob.isnot(None),
            ~User.id.in_(matched_user_ids)
        )
    
    # Get users
    users = query.limit(limit * 2).all()
    
    # Build potential matches with enhanced data
    potential_matches = []
    for user in users:
        user_age = calculate_age(user.dob)
        photos = user.profile_photo_url.split(',') if user.profile_photo_url else []
        
        match_data = {
            "id": user.id,
            "name": user.name,
            "age": user_age,
            "gender": user.gender,
            "bio": user.bio,
            "photos": photos[:1],
            "is_verified": getattr(user, 'is_verified', False)
        }
        
        # Add location data if available
        if use_location and user.id in location_user_ids:
            location_match = next(
                (m for m in location_matches if m['user_id'] == user.id), 
                None
            )
            if location_match:
                match_data["distance"] = location_match.get('distance_display')
                match_data["city"] = location_match.get('city')
        
        # Add visual compatibility if both users have photos
        if current_user.profile_photo_url and user.profile_photo_url:
            try:
                compatibility = vision_analyzer.calculate_visual_compatibility(
                    current_user.profile_photo_url.split(',')[:1],
                    user.profile_photo_url.split(',')[:1]
                )
                match_data["visual_compatibility"] = compatibility
            except:
                pass
        
        potential_matches.append(match_data)
    
    # Apply AI recommendations
    if use_ai and len(potential_matches) > 0:
        try:
            ai_recommendations = matching_intelligence.get_smart_recommendations(
                user_id, potential_matches, limit
            )
            return {
                "users": ai_recommendations,
                "ai_powered": True,
                "location_enabled": use_location,
                "total_candidates": len(potential_matches)
            }
        except Exception as e:
            logger.error(f"AI recommendation error: {e}")
    
    return {
        "users": potential_matches[:limit],
        "ai_powered": False,
        "location_enabled": use_location,
        "total_candidates": len(potential_matches)
    }

# Alias route for frontend expectations
@app.get("/profiles/discover")
async def profiles_discover(
    limit: int = Query(10, le=50),
    use_ai: bool = Query(True),
    use_location: bool = Query(True),
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    return await discover_users(limit=limit, use_ai=use_ai, use_location=use_location, user_id=user_id, db=db)

# --- WebSocket for Real-time Location Updates ---
@app.websocket("/ws/location/{user_id}")
async def websocket_location(websocket: WebSocket, user_id: int):
    """WebSocket for real-time location updates (premium feature)"""
    await websocket.accept()
    
    try:
        # Check if user has premium pass
        features = pass_manager.get_user_features(user_id)
        
        if not features.get('real_time_updates', False):
            await websocket.send_json({
                "error": "Real-time updates require a premium pass",
                "upgrade_options": {
                    "hourly": "$12 for 1 hour",
                    "daily": "$20 for 24 hours"
                }
            })
            await websocket.close()
            return
        
        # Add to real-time subscribers
        location_matcher.real_time_subscribers.add(user_id)
        
        while True:
            # Send nearby matches every 30 seconds
            matches = await location_matcher.find_nationwide_matches(user_id)
            
            await websocket.send_json({
                "type": "location_update",
                "matches": matches[:10],
                "timestamp": datetime.now().isoformat()
            })
            
            await asyncio.sleep(30)
            
    except WebSocketDisconnect:
        location_matcher.real_time_subscribers.discard(user_id)
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        location_matcher.real_time_subscribers.discard(user_id)

# --- Keep existing endpoints (matches, messages, etc.) ---
# [Include all your existing endpoints here - they remain the same]

# Like/Pass endpoints
@app.post("/match/like")
def like_user(request: LikeRequest, user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    target_id = request.target_user_id
    if user_id == target_id:
        raise HTTPException(status_code=400, detail="Cannot like yourself")
    match = get_or_create_match(user_id, target_id, db)
    if match.user1_id == user_id:
        match.user1_liked = True
    else:
        match.user2_liked = True
    match.is_mutual_match = bool(match.user1_liked and match.user2_liked)
    match.updated_at = datetime.utcnow()
    db.commit()
    return {"match_id": match.id, "is_mutual": match.is_mutual_match}

@app.post("/match/pass")
def pass_user(request: LikeRequest, user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    target_id = request.target_user_id
    if user_id == target_id:
        raise HTTPException(status_code=400, detail="Cannot pass yourself")
    match = get_or_create_match(user_id, target_id, db)
    if match.user1_id == user_id:
        match.user1_liked = False
    else:
        match.user2_liked = False
    match.is_mutual_match = False
    match.updated_at = datetime.utcnow()
    db.commit()
    return {"match_id": match.id, "is_mutual": match.is_mutual_match}

# Aliases for frontend compatibility
@app.post("/profiles/like")
def profiles_like(request: LikeRequest, user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    return like_user(request, user_id=user_id, db=db)

@app.post("/profiles/pass")
def profiles_pass(request: LikeRequest, user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    return pass_user(request, user_id=user_id, db=db)

# Profile status endpoint to report completion percentage
@app.get("/profile/status")
def profile_status(
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    percent = compute_profile_completion(user)
    return {
        "profile_completion": percent,
        "is_profile_complete": user.is_profile_complete,
    }

# --- Health Check with All Systems ---
@app.get("/health")
def health_check():
    """Health check endpoint with all system statuses"""
    try:
        ai_stats = matching_intelligence.get_system_stats()
        ai_healthy = True
    except:
        ai_stats = {"error": "AI system unavailable"}
        ai_healthy = False
    
    try:
        vision_status = "healthy" if vision_analyzer else "unavailable"
    except:
        vision_status = "error"
    
    try:
        location_status = "healthy" if location_matcher else "unavailable"
    except:
        location_status = "error"
    
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow(),
        "systems": {
            "ai": {"status": "healthy" if ai_healthy else "degraded", "stats": ai_stats},
            "vision": {"status": vision_status},
            "location": {"status": location_status},
            "student_discounts": {"status": "active"}
        },
        "features": {
            "reinforcement_learning": True,
            "federated_learning": True,
            "computer_vision": True,
            "selfie_verification": True,
            "location_matching": True,
            "student_discounts": True,
            "real_time_updates": True
        }
    }

# --- System Statistics ---
@app.get("/admin/stats")
def get_system_statistics(
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Get comprehensive system statistics (admin endpoint)"""
    
    # Check if user is admin (implement your admin check)
    # if not is_admin(user_id):
    #     raise HTTPException(status_code=403, detail="Admin access required")
    
    return {
        "ai_stats": matching_intelligence.get_system_stats(),
        "location_stats": {
            "active_passes": len(pass_manager.active_passes),
            "revenue": pass_manager.get_revenue_report()
        },
        "student_stats": pass_manager.student_verification.get_university_analytics(),
        "vision_stats": {
            "cache_size": len(vision_analyzer.cache),
            "verifications_performed": len(verification_system.verification_history)
        }
    }

# --- Run server ---
if __name__ == "__main__":
    import uvicorn
    logger.info("🚀 Starting AI-Powered Dating App v3.0...")
    logger.info("🤖 Features: AI/ML + Computer Vision + Location + Student Discounts")
    uvicorn.run(app, host="0.0.0.0", port=8000)
