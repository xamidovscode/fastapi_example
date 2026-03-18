from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_user
from app.db import get_db
from app.models.user import User
from app.schemas.user import UserResponse, UserUpdateRequest
from app.services.user import get_profile, update_profile

router = APIRouter(prefix="/user", tags=["User"])


@router.get("/profile", response_model=UserResponse)
async def profile(current_user: User = Depends(get_current_user)):
    return await get_profile(current_user)


@router.patch("/profile", response_model=UserResponse)
async def edit_profile(
    data: UserUpdateRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await update_profile(data, current_user, db)