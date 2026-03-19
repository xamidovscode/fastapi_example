from datetime import datetime
from typing import List

from pydantic import BaseModel
from uuid import UUID

class AuthorResponse(BaseModel):
    id: UUID
    fullname: str
    username: str

    model_config = {"from_attributes": True}


class PostResponse(BaseModel):
    id: UUID
    title: str
    content: str
    author: AuthorResponse
    created_at: datetime


class PostListResponse(BaseModel):
    total: int
    posts: List[PostResponse]


class PostCreate(BaseModel):
    title: str
    content: str



