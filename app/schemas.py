from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class CandidateBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    mobile: Optional[str] = None
    job_title: Optional[str] = None
    address: Optional[str] = None

class CandidateCreate(CandidateBase):
    pass

class CandidateOut(CandidateBase):
    id: int
    status: str
    applied_on: datetime

    class Config:
        orm_mode = True

###

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    id: int

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str