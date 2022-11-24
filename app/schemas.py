from pydantic import BaseModel , EmailStr
from datetime import datetime
from typing import Optional
from pydantic import conint

class PostBase(BaseModel):            # this is pydantic model
    title : str
    content : str
    published : bool = True

class PostCreate(PostBase):
    pass

class UserOut(BaseModel):                       # schema for returning response of user
    id : int
    email : EmailStr
    created_at : datetime

    class Config:
        orm_mode = True

class Post(PostBase):                           # schema for returning response of post
    id : int
    created_at : datetime
    owner_id : int
    owner : UserOut

    class Config:
        orm_mode = True

class PostOut(BaseModel):
    Post : Post
    votes : int 

    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    email : EmailStr
    password : str

# class UserOut(BaseModel):                       # schema for returning response of user
#     id : int
#     email : EmailStr
#     created_at : datetime

#     class Config:
#         orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token : str
    token_type : str

class Tokendata(BaseModel):
    id : Optional[str] = None

class Vote(BaseModel):
    post_id: int
    dir : conint(le=1)