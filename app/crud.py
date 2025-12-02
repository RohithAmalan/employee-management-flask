# app/crud.py

from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import or_, func

from . import models, schemas


def get_employee_by_id(db: Session, employee_id: int) -> Optional[models.Employee]:
    return db.query(models.Employee).filter(models.Employee.id == employee_id).first()


def get_employee_by_email(db: Session, email: str) -> Optional[models.Employee]:
    return db.query(models.Employee).filter(models.Employee.email == email).first()


def get_employees(
    db: Session,
    page: int = 1,
    page_size: int = 10,
    search: Optional[str] = None,
    department: Optional[str] = None,
    status: Optional[str] = None,
) -> Tuple[List[models.Employee], int]:
    """
    Returns a page of employees and the total count.
    """
    query = db.query(models.Employee)

    if search:
        like_pattern = f"%{search}%"
        query = query.filter(
            or_(
                models.Employee.name.ilike(like_pattern),
                models.Employee.email.ilike(like_pattern),
            )
        )

    if department:
        query = query.filter(models.Employee.department == department)

    if status:
        query = query.filter(models.Employee.status == status)

    total = query.count()

    # Pagination
    if page < 1:
        page = 1
    if page_size < 1:
        page_size = 10

    offset = (page - 1) * page_size

    items = query.order_by(models.Employee.id).offset(offset).limit(page_size).all()
    return items, total


def create_employee(db: Session, employee_in: schemas.EmployeeCreate) -> models.Employee:
    existing = get_employee_by_email(db, employee_in.email)
    if existing:
        # We'll handle the error in the route; here we just check
        raise ValueError("Email already exists")

    employee = models.Employee(
        name=employee_in.name,
        email=employee_in.email,
        phone=employee_in.phone,
        role=employee_in.role,
        department=employee_in.department,
        salary=employee_in.salary,
        date_of_joining=employee_in.date_of_joining,
        status=employee_in.status or "Active",
    )
    db.add(employee)
    db.commit()
    db.refresh(employee)
    return employee


def update_employee(
    db: Session, employee: models.Employee, employee_in: schemas.EmployeeUpdate
) -> models.Employee:
    data = employee_in.dict(exclude_unset=True)

    # If email is updated, ensure it is unique
    if "email" in data and data["email"] != employee.email:
        existing = get_employee_by_email(db, data["email"])
        if existing:
            raise ValueError("Email already exists")

    for field, value in data.items():
        setattr(employee, field, value)

    db.commit()
    db.refresh(employee)
    return employee


def delete_employee(db: Session, employee: models.Employee) -> None:
    """
    Hard delete: removes the record from database.
    If you want soft delete, you can instead set `status="Inactive"`.
    """
    db.delete(employee)
    db.commit()
