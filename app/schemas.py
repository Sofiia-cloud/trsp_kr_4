from pydantic import BaseModel, EmailStr, conint, constr
from typing import Optional


class User(BaseModel):
    username: str
    age: conint(gt=18) 
    email: EmailStr
    password: constr(min_length=8, max_length=16)
    phone: Optional[str] = "Unknown"


class ErrorResponse(BaseModel):
    error: str
    status_code: int


class UserIn(BaseModel):
    username: str
    age: int

class UserOut(BaseModel):
    id: int
    username: str
    age: int