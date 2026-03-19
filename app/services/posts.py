from http.client import HTTPException
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models import User
from app.models.post import Post
from app.schemas.posts import PostCreate


async def get_posts(db: AsyncSession, page: int = 1, limit: int = 10):
    offset = (page - 1) * limit
    total_result = await db.execute(select(func.count(Post.id)))
    total = total_result.scalar()

    result = await db.execute(
        select(Post)
        .options(selectinload(Post.author))
        .order_by(Post.created_at.desc())
        .offset(offset)
        .limit(limit)
    )
    posts = result.scalars().all()

    return {"total": total, "posts": posts}


async def create_post(db: AsyncSession, data: PostCreate, author_id):
    post = Post(**data.model_dump(), author_id=author_id)
    db.add(post)
    await db.commit()
    await db.refresh(post)
    return post


async def update_post(
        db: AsyncSession,
        post_id: UUID,
        author: User,
        data: PostCreate,
):
    result = await db.execute(select(Post).where(Post.id == post_id))
    post = result.scalar_one_or_none()

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    if post.author != author:
        raise HTTPException(status_code=403, detail="Not your post")

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(post, key, value)

    await db.commit()
    await db.refresh(post)
    return post



