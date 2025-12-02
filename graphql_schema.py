import os
import uuid
import strawberry
import asyncio
from datetime import datetime
from typing import List, Optional
from strawberry.types import Info
from models import User, Match, Message, UserPreferences
from sqlalchemy.orm import Session
from strawberry.schema.config import StrawberryConfig
from strawberry.file_uploads import Upload
from jose import jwt

SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"

# GraphQL types mapping to your SQLAlchemy models
@strawberry.type
class UserType:
    id: int
    name: Optional[str]
    email: Optional[str]
    phone_number: Optional[str]
    bio: Optional[str]
    gender: Optional[str]
    is_active: bool
    is_verified: bool
    is_student_verified: bool

@strawberry.type
class UserPreferencesType:
    id: int
    min_age: Optional[int]
    max_age: Optional[int]
    preferred_genders: Optional[str]
    max_distance: Optional[int]
    only_verified: bool
    only_students: bool

@strawberry.type
class MatchType:
    id: str
    user1_id: int
    user2_id: int
    is_mutual_match: bool
    status: Optional[str]

@strawberry.type
class MessageType:
    id: int
    match_id: str
    sender_id: int
    receiver_id: int
    content: str
    message_type: Optional[str]
    is_read: bool


@strawberry.type
class AuthPayload:
    access_token: str
    user_id: Optional[int] = None
    is_profile_complete: Optional[bool] = None
    token_type: Optional[str] = "bearer"
    profile_photo_1_url: Optional[str] = None
    profile_photo_2_url: Optional[str] = None
    profile_photo_3_url: Optional[str] = None


def get_db(info: Info) -> Session:
    return info.context["db"]


def to_user_type(user: User) -> UserType:
    return UserType(
        id=user.id,
        name=user.name,
        email=user.email,
        phone_number=user.phone_number,
        bio=user.bio,
        gender=user.gender,
        is_active=user.is_active,
        is_verified=user.is_verified,
        is_student_verified=user.is_student_verified,
    )


def to_preferences_type(pref: UserPreferences) -> UserPreferencesType:
    return UserPreferencesType(
        id=pref.id,
        min_age=pref.min_age,
        max_age=pref.max_age,
        preferred_genders=','.join(pref.preferred_genders) if pref.preferred_genders else None,
        max_distance=pref.max_distance,
        only_verified=pref.only_verified,
        only_students=pref.only_students,
    )


def to_match_type(match: Match) -> MatchType:
    return MatchType(
        id=match.id,
        user1_id=match.user1_id,
        user2_id=match.user2_id,
        is_mutual_match=match.is_mutual_match,
        status=match.status,
    )


def to_message_type(message: Message) -> MessageType:
    return MessageType(
        id=message.id,
        match_id=message.match_id,
        sender_id=message.sender_id,
        receiver_id=message.receiver_id,
        content=message.content,
        message_type=message.message_type,
        is_read=message.is_read,
    )


@strawberry.type
class Query:
    @strawberry.field
    def user(self, info: Info, id: int) -> Optional[UserType]:
        db = get_db(info)
        user = db.query(User).filter(User.id == id).first()
        return to_user_type(user) if user else None

    @strawberry.field
    def users(self, info: Info, limit: int = 20) -> List[UserType]:
        db = get_db(info)
        results = db.query(User).limit(limit).all()
        return [to_user_type(u) for u in results]

    @strawberry.field
    def matches(self, info: Info, user_id: int) -> List[MatchType]:
        db = get_db(info)
        results = db.query(Match).filter((Match.user1_id == user_id) | (Match.user2_id == user_id)).all()
        return [to_match_type(m) for m in results]

    @strawberry.field
    def messages(self, info: Info, match_id: str) -> List[MessageType]:
        db = get_db(info)
        results = db.query(Message).filter(Message.match_id == match_id).all()
        return [to_message_type(m) for m in results]

    @strawberry.field
    def preferences(self, info: Info, user_id: int) -> Optional[UserPreferencesType]:
        db = get_db(info)
        pref = db.query(UserPreferences).filter(UserPreferences.user_id == user_id).first()
        return to_preferences_type(pref) if pref else None

    @strawberry.field
    def me(self, info: Info) -> Optional[UserType]:
        db = get_db(info)
        request = info.context.get("request") if info.context else None
        user_id = None
        if request:
            auth = request.headers.get("authorization")
            if auth and auth.lower().startswith("bearer "):
                token = auth.split(" ", 1)[1]
                try:
                    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
                    user_id = int(payload.get("sub"))
                except Exception:
                    user_id = None
        if not user_id:
            return None
        user = db.query(User).filter(User.id == user_id).first()
        return to_user_type(user) if user else None


@strawberry.type
class Mutation:
    @strawberry.mutation
    def send_message(self, info: Info, match_id: str, sender_id: int, receiver_id: int, content: str) -> MessageType:
        db = get_db(info)
        message = Message(
            match_id=match_id,
            sender_id=sender_id,
            receiver_id=receiver_id,
            content=content,
        )
        db.add(message)
        db.commit()
        db.refresh(message)
        return to_message_type(message)

    @strawberry.mutation
    def verify_otp(self, info: Info, phone_number: str, otp: str) -> AuthPayload:
        # Mock verification: accept only OTP 1234
        if otp != "1234":
            raise Exception("Invalid OTP")
        # In a real implementation, generate JWT/access token and fetch user
        return AuthPayload(
            access_token=f"mock-token-for-{phone_number}",
            user_id=1,
            is_profile_complete=False,
            token_type="bearer",
        )

    @strawberry.mutation
    def add_profession_option(self, info: Info, category: str, name: str) -> bool:
        # Mock: accept and return True. Persist if/when a model/table is added.
        return True

    @strawberry.mutation
    async def update_profile(
        self,
        info: Info,
        name: str,
        dob: str,
        gender: str,
        bio: str,
        location: str,
        looking_for: str,
        interests: List[str],
        languages: List[str],
        height_cm: Optional[int] = None,
        profession_category: Optional[str] = None,
        profession_title: Optional[str] = None,
        profile_photo_1: Optional[Upload] = None,
        profile_photo_2: Optional[Upload] = None,
        profile_photo_3: Optional[Upload] = None,
        user_id: int = 1,
    ) -> bool:
        db: Session = get_db(info)

        # Save uploads to local /uploads and return URLs
        async def save_upload(file: Upload) -> str:
            uploads_dir = os.path.join(os.getcwd(), "uploads")
            os.makedirs(uploads_dir, exist_ok=True)
            ext = os.path.splitext(file.filename or "")[1] or ".jpg"
            filename = f"{uuid.uuid4().hex}{ext}"
            dest = os.path.join(uploads_dir, filename)
            content = file.read()
            if asyncio.iscoroutine(content):
                content = await content
            with open(dest, "wb") as f:
                f.write(content)
            return f"/uploads/{filename}"

        photo_urls = [None, None, None]
        uploads = [profile_photo_1, profile_photo_2, profile_photo_3]
        for idx, file in enumerate(uploads):
            if file:
                photo_urls[idx] = await save_upload(file)

        # Persist basic profile fields
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return False

        # Parse dob
        parsed_dob = None
        for fmt in ("%Y-%m-%d", "%Y/%m/%d", "%b %d %Y", "%a %b %d %Y", "%Y-%m-%dT%H:%M:%S"):
            try:
                parsed_dob = datetime.strptime(dob, fmt).date()
                break
            except Exception:
                continue
        if parsed_dob is None:
            try:
                parsed_dob = datetime.fromisoformat(dob).date()
            except Exception:
                parsed_dob = None

        user.name = name
        user.gender = gender
        user.bio = bio
        if parsed_dob:
            user.dob = parsed_dob

        # Store profile photos
        user.profile_photo_1 = photo_urls[0] or user.profile_photo_1
        user.profile_photo_2 = photo_urls[1] or user.profile_photo_2
        user.profile_photo_3 = photo_urls[2] or user.profile_photo_3
        user.profile_photos = [p for p in photo_urls if p] or user.profile_photos

        user.is_profile_complete = True

        db.add(user)
        db.commit()

        return True


schema = strawberry.Schema(
    query=Query,
    mutation=Mutation,
    config=StrawberryConfig(auto_camel_case=False),
)
