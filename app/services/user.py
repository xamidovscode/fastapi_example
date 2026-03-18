from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status

from app.models.user import User
from app.schemas.user import UserUpdateRequest


async def get_profile(current_user: User):
    return current_user


async def update_profile(data: UserUpdateRequest, current_user: User, db: AsyncSession):
    if data.username and data.username != current_user.username:
        existing = await db.execute(select(User).where(User.username == data.username))
        if existing.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Bu username band"
            )

    for key, value in data.model_dump(exclude_none=True).items():
        setattr(current_user, key, value)

    await db.commit()
    await db.refresh(current_user)
    return current_user