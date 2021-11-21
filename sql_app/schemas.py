from pydantic import BaseModel,EmailStr
from typing import Optional,List




class User_registration(BaseModel):
    name:str
    email:EmailStr
    phone:int
    password:str


class User_login(BaseModel):
    email:EmailStr
    pasword:str


class Blog(BaseModel):
    title:str
    description:str
    class Config():
        orm_mode = True







class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user: Optional[str] = None