# app/routes/employees.py

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from .. import schemas, crud, models

router = APIRouter(
    prefix="/employees",
    tags=["Employees"],
)


@router.get("/", response_model=schemas.EmployeeListResponse)
def list_employees(
    page: int = 1,
    page_size: int = 10,
    search: Optional[str] = None,
    department: Optional[str] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """
    List employees with pagination, optional search and filters.
    """
    items, total = crud.get_employees(
        db=db,
        page=page,
        page_size=page_size,
        search=search,
        department=department,
        status=status,
    )

    # Calculate total_pages
    if page_size <= 0:
        page_size = 10
    total_pages = (total + page_size - 1) // page_size

    return schemas.EmployeeListResponse(
        items=items,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
    )


@router.get("/{employee_id}", response_model=schemas.EmployeeOut)
def get_employee(
    employee_id: int,
    db: Session = Depends(get_db),
):
    employee = crud.get_employee_by_id(db, employee_id)
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found",
        )
    return employee


@router.post(
    "/", response_model=schemas.EmployeeOut, status_code=status.HTTP_201_CREATED
)
def create_employee(
    employee_in: schemas.EmployeeCreate,
    db: Session = Depends(get_db),
):
    try:
        employee = crud.create_employee(db, employee_in)
    except ValueError as e:
        # For example, duplicate email
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    return employee


@router.put("/{employee_id}", response_model=schemas.EmployeeOut)
def update_employee(
    employee_id: int,
    employee_in: schemas.EmployeeUpdate,
    db: Session = Depends(get_db),
):
    employee = crud.get_employee_by_id(db, employee_id)
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found",
        )

    try:
        updated = crud.update_employee(db, employee, employee_in)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    return updated


@router.patch("/{employee_id}", response_model=schemas.EmployeeOut)
def patch_employee(
    employee_id: int,
    employee_in: schemas.EmployeeUpdate,
    db: Session = Depends(get_db),
):
    # Same logic as PUT, but typically used for partial updates
    employee = crud.get_employee_by_id(db, employee_id)
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found",
        )

    try:
        updated = crud.update_employee(db, employee, employee_in)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    return updated


@router.delete("/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_employee(
    employee_id: int,
    db: Session = Depends(get_db),
):
    employee = crud.get_employee_by_id(db, employee_id)
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found",
        )

    crud.delete_employee(db, employee)
    return None
