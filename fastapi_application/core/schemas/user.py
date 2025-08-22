from typing import Literal

from pydantic import BaseModel


class UserBase(BaseModel):
    username: str


class UserCreateGet(UserBase):
    password: str
    role: list[Literal["supplier", "customer", "admin"]]

class UserCreate(UserBase):
    hashed_password: str
    role_id: list[int]
