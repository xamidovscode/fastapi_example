from sqlalchemy import Column, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from app.models.common import BaseModel

class Comment(BaseModel):
    __tablename__ = "likes"

    post_id = Column(
        UUID(as_uuid=True),
        ForeignKey("posts.id"),
        nullable=False,
    )
    author_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False,
    )
    author = relationship("User", back_populates="likes")
    post = relationship("Post", back_populates="likes")


