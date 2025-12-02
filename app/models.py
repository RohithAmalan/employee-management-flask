# app/models.py

from sqlalchemy import Column, Integer, String, Float, Date, DateTime, func
from .database import Base


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    email = Column(String, nullable=False, unique=True, index=True)
    phone = Column(String, nullable=False)
    role = Column(String, nullable=True)
    department = Column(String, nullable=True, index=True)
    salary = Column(Float, nullable=True)
    date_of_joining = Column(Date, nullable=True)
    status = Column(String, nullable=False, default="Active")  # Active / Inactive
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
