from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime


class UserResponse(BaseModel):
    id: UUID
    username: str
    email: EmailStr
    fullname: str
    is_verified: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class UserUpdateRequest(BaseModel):
    username: str | None = None
    fullname: str | None = None