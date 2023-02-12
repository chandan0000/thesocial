from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


# class PostBase(BaseModel):
#     title: str
#     content: str
#     published: bool = True

class UserOut(BaseModel):
    id: int
    email: EmailStr
    create_at: datetime

    class Config:
        orm_mode = True

class PostCreate(PostBase):
    pass


class Post(PostBase):
    id: int
    create_at: datetime
    owner:UserOut

    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    email: EmailStr
    password: str



class UserLogin(BaseModel):
    email:EmailStr
    password:str


class Token(BaseModel):
    access_token:str
    token_type:str
class TokenData(BaseModel):
    id:Optional[str]=None
 