from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete

from app.db import get_db
from app.models.user import User

router = APIRouter(prefix="/admin", tags=["Admin"])

@router.delete("/users/cleanup")
async def delete_unverified_users(db: AsyncSession = Depends(get_db)):
    two_days_ago = datetime.utcnow() - timedelta(days=2)

    result = await db.execute(
        delete(User).where(
            (User.is_verified == False) &
            (User.created_at <= two_days_ago)
        )
    )

    await db.commit()

    return {
        "message": "Eski tasdiqlanmagan userlar o'chirildi",
        "deleted_count": result.rowcount
    }