from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import UserCreate, UserRead
from app.crud.user import get_users, create_user
from app.db.session import get_db

router = APIRouter()

@router.get("/", response_model=list[UserRead])
async def list_users(db: AsyncSession = Depends(get_db)):
    return await get_users(db)

@router.post("/", response_model=UserRead)
async def add_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    return await create_user(db, username=user.username)