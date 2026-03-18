import random
from datetime import datetime, timedelta, timezone

from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status

from app.core import config
from app.models.user import User
from app.schemas.auth import UserRegister
from app.core.security import hash_password, verify_password, create_access_token, create_refresh_token


def generate_otp() -> str:
    # return str(random.randint(100000, 999999))
    return '77777'


async def register_user(data: UserRegister, db: AsyncSession, redis: Redis):

    email_result = await db.execute(select(User).where(User.email == data.email))
    email_user = email_result.scalar_one_or_none()

    username_result = await db.execute(select(User).where(User.username == data.username))
    username_user = username_result.scalar_one_or_none()

    if email_user and email_user.is_verified:
        raise HTTPException(status_code=400, detail="Bu email band!")

    if username_user and username_user.is_verified:
        raise HTTPException(status_code=400, detail="Bu username band!")

    if email_user and username_user and email_user.id != username_user.id:
        raise HTTPException(status_code=400, detail="Bu email yoki username band!")

    user = email_user or username_user

    cached_otp = await redis.get(f"otp:{data.email}")
    if user and cached_otp:
        raise HTTPException(status_code=400, detail="Sizga allaqachon tasdiqlash kodi yuborilgan!")

    if user:
        user.username = data.username
        user.email = data.email
        user.fullname = data.fullname
        user.hashed_password = hash_password(data.password)
    else:
        user = User(
            username=data.username,
            email=data.email,
            fullname=data.fullname,
            hashed_password=hash_password(data.password),
        )
        db.add(user)

    await db.commit()
    await db.refresh(user)

    otp = generate_otp()
    await redis.setex(f"otp:{user.email}", config.OTP_LIFE_TIME, otp)

    return user


async def verify_user(email: str, otp: str, db: AsyncSession, redis: Redis):
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="Foydalanuvchi topilmadi")

    if user.is_verified:
        raise HTTPException(status_code=400, detail="Allaqachon tasdiqlangan")

    cached_otp = await redis.get(f"otp:{user.email}")

    if not cached_otp:
        raise HTTPException(status_code=400, detail="OTP muddati o'tgan yoki yuborilmagan")

    if cached_otp != otp:
        raise HTTPException(status_code=400, detail="OTP kod noto'g'ri")

    user.is_verified = True
    await db.commit()

    await redis.delete(f"otp:{user.email}")

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