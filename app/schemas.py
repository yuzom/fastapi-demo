# Pydantic models which define post and user, request and response format between frontend and our API

from pydantic import BaseModel, EmailStr, Field		# to define post schema
from datetime import datetime
from typing import Optional, Annotated

# User schemas

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    # Tell pydantic that it can expect a non-dict value SQLalchemy
    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Post schemas

class PostBase(BaseModel):                      # extend this class to query and response classes
    title: str
    content: str
    published: bool = True						# default value is True

class PostCreate(PostBase):                     # class for creating posts
    pass

class Post(PostBase):                           # class for responding with posts
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

    # Tell pydantic that it can expect a non-dict value from SQLalchemy
    class Config:
        from_attributes = True

class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
        from_attributes = True

# Token schemas

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None


# Vote s chemas

class Vote(BaseModel):
    post_id: int
    dir: Annotated[int, Field(ge=0, le=1)]      # Must be 0 or 1
