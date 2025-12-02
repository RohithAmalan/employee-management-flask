# app/schemas.py

from datetime import date, datetime
from typing import Optional, List

from pydantic import BaseModel, EmailStr, Field


class EmployeeBase(BaseModel):
    name: str = Field(..., min_length=1)
    email: EmailStr
    phone: str
    role: Optional[str] = None
    department: Optional[str] = None
    salary: Optional[float] = None
    date_of_joining: Optional[date] = None
    status: Optional[str] = Field("Active", pattern="^(Active|Inactive)$")


class EmployeeCreate(EmployeeBase):
    # Same as base, but you can make additional required fields if you want
    pass


class EmployeeUpdate(BaseModel):
    # All fields optional for PATCH/PUT
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    role: Optional[str] = None
    department: Optional[str] = None
    salary: Optional[float] = None
    date_of_joining: Optional[date] = None
    status: Optional[str] = Field(None, pattern="^(Active|Inactive)$")


class EmployeeOut(EmployeeBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True  # Needed so Pydantic can read SQLAlchemy objects


class EmployeeListResponse(BaseModel):
    items: List[EmployeeOut]
    total: int
    page: int
    page_size: int
    total_pages: int
