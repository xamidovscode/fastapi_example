from http.client import HTTPException
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.models import Post
from app.schemas.posts import PostListResponse, PostResponse, PostCreate
from app.services.posts import get_posts, create_post, update_post
from app.core.dependencies import get_current_user

router = APIRouter(prefix="/posts", tags=["Posts"])

@router.get("", response_model=PostListResponse)
async def list_posts_api(
    page: int = 1,
    limit: int = 10,
    db: AsyncSession = Depends(get_db)
):
    return await get_posts(db, page, limit)


@router.post('', response_model=PostResponse)
async def create_post_api(
        data: PostCreate,
        db: AsyncSession = Depends(get_db),
        current_user = Depends(get_current_user),
):
    return await create_post(db, data, current_user.id)


@router.patch('/{uuid}', response_model=PostResponse)
async def update_post_api(
        uuid: UUID,
        data: PostCreate,
        db: AsyncSession = Depends(get_db),
        current_user = Depends(get_current_user)
):
    return await update_post(
        db=db,
        post_id=uuid,
        data=data,
        author=current_user
    )


@router.delete('/{uuid}', status_code=204)
async def delete_post_api(
        uuid: UUID,
        current_user = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        delete(Post).where(Post.id == uuid, Post.author_id == current_user.id)
    )
    await db.commit()

    if result.rowcount == 0:
        post = await db.execute(select(Post).where(Post.id == uuid))
        if not post.scalar_one_or_none():
            raise HTTPException(status_code=404, detail="Post not found")
        raise HTTPException(status_code=403, detail="Not your post")


