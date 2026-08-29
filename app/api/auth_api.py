"""Simple JWT authentication endpoints for the application."""
from datetime import UTC, datetime, timedelta
import logging
import re
import secrets

from fastapi import APIRouter, Depends, HTTPException, Response, status
from pydantic import BaseModel, Field, field_validator
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import create_token, decode_token, get_current_user, hash_password, token_digest, validate_password, verify_password
from app.db.database import get_db
from app.models.auth import PasswordResetToken, RefreshToken
from app.models.user import Role, User
from app.models.admin import AdminActivityLog
from app.services.email_service import send_password_reset_email

router = APIRouter(prefix="/auth", tags=["Authentication"])
logger = logging.getLogger(__name__)
EMAIL_PATTERN = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")


def normalize_email(value: str) -> str:
    email = value.strip().lower()
    if not EMAIL_PATTERN.fullmatch(email) or len(email) > 254:
        raise ValueError("Enter a valid email address")
    return email


class RegisterRequest(BaseModel):
    full_name: str = Field(min_length=2, max_length=120)
    email: str
    password: str = Field(min_length=8, max_length=128)
    confirm_password: str = Field(min_length=8, max_length=128)

    _validate_email = field_validator("email")(normalize_email)


class LoginRequest(BaseModel):
    email: str
    password: str = Field(min_length=1, max_length=128)

    _validate_email = field_validator("email")(normalize_email)


class RefreshRequest(BaseModel):
    refresh_token: str = Field(min_length=20, max_length=2048)


class ForgotPasswordRequest(BaseModel):
    email: str

    _validate_email = field_validator("email")(normalize_email)


class PasswordResetRequest(BaseModel):
    token: str = Field(min_length=32, max_length=2048)
    password: str = Field(min_length=8, max_length=128)
    confirm_password: str = Field(min_length=8, max_length=128)


def user_data(user: User) -> dict:
    return {
        "id": user.id,
        "full_name": user.full_name,
        "email": user.email,
        "role": user.role.value,
        "is_active": user.is_active,
        "created_at": user.created_at,
        "updated_at": user.updated_at,
        "last_login": user.last_login,
    }


def tokens_for(db: Session, user: User) -> dict:
    access_token = create_token(user.id, "access", timedelta(minutes=settings.JWT_ACCESS_TOKEN_MINUTES))
    refresh_token = create_token(user.id, "refresh", timedelta(days=settings.JWT_REFRESH_TOKEN_DAYS))
    db.add(
        RefreshToken(
            user_id=user.id,
            token_hash=token_digest(refresh_token),
            expires_at=datetime.now(UTC) + timedelta(days=settings.JWT_REFRESH_TOKEN_DAYS),
        )
    )
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "expires_in": settings.JWT_ACCESS_TOKEN_MINUTES * 60,
        "user": user_data(user),
    }


def issue_reset_token(db: Session, user: User) -> str:
    now = datetime.now(UTC)
    db.query(PasswordResetToken).filter(
        PasswordResetToken.user_id == user.id,
        PasswordResetToken.used_at.is_(None),
    ).update({PasswordResetToken.used_at: now})
    token = secrets.token_urlsafe(48)
    db.add(
        PasswordResetToken(
            user_id=user.id,
            token_hash=token_digest(token),
            expires_at=now + timedelta(minutes=settings.PASSWORD_RESET_TOKEN_MINUTES),
        )
    )
    return token


def validate_reset_password(password: str) -> None:
    if not re.search(r"[A-Z]", password) or not re.search(r"[a-z]", password) or not re.search(r"\d", password) or not re.search(r"[^A-Za-z0-9]", password):
        raise HTTPException(422, "Password must include uppercase, lowercase, number, and special character.")


def is_expired(expires_at: datetime) -> bool:
    """Compare token expirations safely across PostgreSQL and local SQLite tests."""
    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=UTC)
    return expires_at <= datetime.now(UTC)


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    if data.password != data.confirm_password:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, "Passwords do not match")
    validate_password(data.password)
    if db.query(User).filter(User.email == data.email).first():
        raise HTTPException(status.HTTP_409_CONFLICT, "An account with that email already exists")

    user = User(full_name=data.full_name.strip(), email=data.email, password_hash=hash_password(data.password), role=Role.USER)
    db.add(user)
    db.flush()
    result = tokens_for(db, user)
    db.commit()
    return result


@router.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    if user is None or not verify_password(data.password, user.password_hash):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid email or password")
    if not user.is_active:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Account is deactivated")

    user.last_login = datetime.now(UTC)
    db.add(AdminActivityLog(admin_user_id=user.id if user.role == Role.ADMIN else None, action="login", resource="auth", detail=f"user:{user.id}"))
    result = tokens_for(db, user)
    db.commit()
    return result


@router.post("/refresh")
def refresh(data: RefreshRequest, db: Session = Depends(get_db)):
    payload = decode_token(data.refresh_token, "refresh")
    stored = db.query(RefreshToken).filter(
        RefreshToken.token_hash == token_digest(data.refresh_token),
        RefreshToken.revoked_at.is_(None),
    ).first()
    if stored is None or is_expired(stored.expires_at) or int(payload["sub"]) != stored.user_id:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Refresh token is invalid or expired")

    user = db.get(User, stored.user_id)
    if user is None or not user.is_active:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Account is unavailable")

    stored.revoked_at = datetime.now(UTC)
    result = tokens_for(db, user)
    db.commit()
    return result


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(data: RefreshRequest, db: Session = Depends(get_db)) -> Response:
    stored = db.query(RefreshToken).filter(
        RefreshToken.token_hash == token_digest(data.refresh_token),
        RefreshToken.revoked_at.is_(None),
    ).first()
    if stored:
        stored.revoked_at = datetime.now(UTC)
        db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/forgot-password", status_code=status.HTTP_202_ACCEPTED)
def forgot_password(data: ForgotPasswordRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    if user and user.is_active:
        token = issue_reset_token(db, user)
        reset_url = f"{settings.FRONTEND_URL.rstrip('/')}/reset-password?token={token}"
        db.flush()
        try:
            send_password_reset_email(user.full_name, user.email, reset_url)
        except Exception:
            logger.exception("Password reset email could not be sent")
            # Local development should remain usable without a paid SMTP
            # provider or a Gmail app password. Never expose this in production.
            if settings.ENVIRONMENT.lower() == "development":
                db.commit()
                return {
                    "message": "Email delivery is unavailable locally. Continue with the reset link below.",
                    "reset_url": reset_url,
                }
            db.rollback()
            return {"message": "If an account with that email exists, a password reset link has been sent."}
        db.commit()
        logger.info("Password reset email sent")
    logger.info("Password reset requested")
    return {"message": "If an account with that email exists, a password reset link has been sent."}


@router.post("/reset-password")
def reset_password(data: PasswordResetRequest, db: Session = Depends(get_db)):
    if data.password != data.confirm_password:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, "Passwords do not match")
    validate_password(data.password)
    validate_reset_password(data.password)
    now = datetime.now(UTC)
    reset_token = db.query(PasswordResetToken).filter(
        PasswordResetToken.token_hash == token_digest(data.token),
        PasswordResetToken.used_at.is_(None),
    ).first()
    if reset_token is None or is_expired(reset_token.expires_at):
        logger.info("Expired or invalid password reset token")
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Reset token is invalid or expired")

    reset_token.used_at = now
    reset_token.user.password_hash = hash_password(data.password)
    db.query(RefreshToken).filter(
        RefreshToken.user_id == reset_token.user_id,
        RefreshToken.revoked_at.is_(None),
    ).update({RefreshToken.revoked_at: now})
    db.commit()
    logger.info("Password reset successful")
    return {"message": "Password updated. Please sign in."}


@router.get("/me")
def me(user: User = Depends(get_current_user)):
    return user_data(user)
