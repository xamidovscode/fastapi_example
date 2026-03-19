from sqlalchemy import Column, String, Boolean
from sqlalchemy.orm import relationship

from app.models.common import BaseModel


class User(BaseModel):
    __tablename__ = "users"

    username = Column(
        String(50),
        unique=True, index=True, nullable=False
    )
    email = Column(
        String(255),
        unique=True, index=True, nullable=False
    )
    fullname = Column(
        String(255),
        nullable=False
    )
    hashed_password = Column(
        String, nullable=False
    )
    is_verified = Column(
        Boolean, default=False
    )

    posts = relationship("Post", back_populates="author", cascade="all, delete-orphan")
    comments = relationship("Comment", back_populates="author", cascade="all, delete-orphan")
    likes = relationship("Like", back_populates="author", cascade="all, delete-orphan")

