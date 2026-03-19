from sqlalchemy import Column, ForeignKey, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from app.models.common import BaseModel


class Post(BaseModel):
    __tablename__ = "posts"

    title = Column(
        String(255),
        nullable=False,
    )
    content = Column(
        Text,
        nullable=False,
    )
    author_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False,
    )
    author = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="post")
    likes = relationship("Like", back_populates="post")


