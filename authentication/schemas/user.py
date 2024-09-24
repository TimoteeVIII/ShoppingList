from typing import Optional
from ninja import Schema, Field
from pydantic import EmailStr


class UserCreateSchema(Schema):
    username: str = Field(..., min_length=2, max_length=255, alias="username")
    password: str = Field(..., min_length=4, max_length=255, alias="password")
    email: EmailStr = Field(..., min_length=2, max_length=255, alias="email")
    first_name: Optional[str] = Field(None)
    last_name: Optional[str] = Field(None)


class UserLoginSchema(Schema):
    username: Optional[str] = Field(None)
    email: Optional[EmailStr] = Field(None)
    password: str = Field(..., min_length=4, max_length=255, alias="password")
