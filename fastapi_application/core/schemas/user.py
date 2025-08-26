from typing import Literal

from pydantic import BaseModel


class UserBase(BaseModel):
    username: str

class UserAuth(UserBase):
    password: str

class UserToken(BaseModel):
    user_id: int
    roles: list[Literal["supplier", "customer", "admin"]]

class UserCreateGet(UserBase):
    password: str
    role: list[Literal["supplier", "customer", "admin"]]

class UserCreate(UserBase):
    hashed_password: str
    role_id: list[int]
