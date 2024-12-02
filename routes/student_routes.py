from fastapi import APIRouter, HTTPException
from services.student_service import (
    create_student_service,
    list_students_service,
    fetch_student_service,
    update_student_service,
    delete_student_service
)
from models.student import Student, StudentUpdate, StudentResponse, StudentListResponse

router = APIRouter()

@router.post("/", status_code=201, response_model=StudentResponse)
async def create_student(student: Student):
    return await create_student_service(student)

@router.get("/", response_model=StudentListResponse)
async def list_students(country: str = None, age: int = None):
    return await list_students_service(country, age)

@router.get("/{id}", response_model=Student)
async def fetch_student(id: str):
    student = await fetch_student_service(id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@router.patch("/{id}")
async def update_student(id: str, student_update: StudentUpdate):
    await update_student_service(id, student_update)
    return {}

@router.delete("/{id}")
async def delete_student(id: str):
    await delete_student_service(id)
    return {}
