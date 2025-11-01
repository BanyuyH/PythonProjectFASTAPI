from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    name: str
    email: EmailStr
    age: Optional[int] = None
    password: str


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: str = Field(alias="_id")
    created_at: datetime

    model_config = ConfigDict(
        populate_by_name=True,  # Allows using both id and _id
        json_encoders={},
    )