import random
from datetime import datetime, timedelta, timezone

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status

from app.models.user import User
from app.schemas.auth import UserRegister
from app.core.security import hash_password, verify_password, create_access_token, create_refresh_token


def generate_otp() -> str:
    return str(random.randint(100000, 999999))


async def register_user(data: UserRegister, db: AsyncSession):
    existing = await db.execute(
        select(User).where((User.email == data.email) | (User.username == data.username))
    )
    if existing.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email yoki username band"
        )

    otp = generate_otp()
    otp_expires_at = datetime.now(timezone.utc) + timedelta(minutes=10)

    user = User(
        username=data.username,
        email=data.email,
        fullname=data.fullname,
        hashed_password=hash_password(data.password),
        # otp_code=otp,
        # otp_expires_at=otp_expires_at
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)

    print(f"[OTP] {user.email} uchun kod: {otp}")

    return user


async def verify_user(email: str, otp: str, db: AsyncSession):
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="Foydalanuvchi topilmadi")

    if user.is_verified:
        raise HTTPException(status_code=400, detail="Allaqachon tasdiqlangan")

    if user.otp_code != otp:
        raise HTTPException(status_code=400, detail="OTP kod noto'g'ri")

    if datetime.now(timezone.utc) > user.otp_expires_at:
        raise HTTPException(status_code=400, detail="OTP kodning muddati o'tgan")

    user.is_verified = True
    user.otp_code = None
    user.otp_expires_at = None
    await db.commit()

    return {"message": "Email muvaffaqiyatli tasdiqlandi"}


async def login_user(email: str, password: str, db: AsyncSession):
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()

    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email yoki parol noto'g'ri"
        )

    if not user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Avval emailni tasdiqlang"
        )

    payload = {"sub": str(user.id), "email": user.email}
    return {
        "access_token": create_access_token(payload),
        "refresh_token": create_refresh_token(payload),
        "token_type": "bearer"
    }