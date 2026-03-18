from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime


class UserRegister(BaseModel):
    username: str
    email: EmailStr
    fullname: str
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserVerify(BaseModel):
    email: EmailStr
    otp: str


class UserResponse(BaseModel):
    id: UUID
    username: str
    email: EmailStr
    fullname: str
    is_verified: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"