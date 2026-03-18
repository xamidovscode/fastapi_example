from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.schemas.auth import UserRegister, UserLogin, UserVerify, UserResponse, Token
from app.services.auth import register_user, login_user, verify_user

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=UserResponse, status_code=201)
async def register(data: UserRegister, db: AsyncSession = Depends(get_db)):
    return await register_user(data, db)


@router.post("/verify")
async def verify(data: UserVerify, db: AsyncSession = Depends(get_db)):
    return await verify_user(data.email, data.otp, db)


@router.post("/login", response_model=Token)
async def login(data: UserLogin, db: AsyncSession = Depends(get_db)):
    return await login_user(data.email, data.password, db)
