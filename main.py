from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from typing import List, Optional
from bson import ObjectId
from urllib.parse import quote_plus
import os
import uvicorn
app = FastAPI()

# Encode password
password = "password@11feb"  # Replace with your actual password
encoded_password = quote_plus(password)

# MongoDB connection
client = AsyncIOMotorClient(
    f"mongodb+srv://sarthak:pwdd@cluster0.fdl9e.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
)
db = client.student_management

class Address(BaseModel):
    city: str
    country: str

class Student(BaseModel):
    name: str
    age: int
    address: Address

class StudentUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    address: Optional[Address] = None

class StudentResponse(BaseModel):
    id: str

class StudentListResponse(BaseModel):
    data: List[Student]

@app.post("/students", response_model=StudentResponse, status_code=201)
async def create_student(student: Student):
    result = await db.students.insert_one(student.dict())
    return {"id": str(result.inserted_id)}

@app.get("/students", response_model=StudentListResponse)
async def list_students(country: Optional[str] = None, age: Optional[int] = None):
    query = {}
    if country:
        query["address.country"] = country
    if age:
        query["age"] = {"$gte": age}
    students = await db.students.find(query).to_list(1000)
    for student in students:
        student["id"] = str(student["_id"])
        student.pop("_id")
    return {"data": students}

@app.get("/students/{id}", response_model=Student)
async def fetch_student(id: str):
    student = await db.students.find_one({"_id": ObjectId(id)})
    if student:
        student["id"] = str(student["_id"])
        student.pop("_id")
        return student
    return {"error": "Student not found"}

@app.patch("/students/{id}", status_code=204)
async def update_student(id: str, student_update: StudentUpdate):
    update_data = {k: v for k, v in student_update.dict().items() if v is not None}
    if update_data:
        await db.students.update_one({"_id": ObjectId(id)}, {"$set": update_data})
    return

@app.delete("/students/{id}", status_code=200)
async def delete_student(id: str):
    await db.students.delete_one({"_id": ObjectId(id)})
    return {}

port = int(os.getenv("PORT", 8000))
uvicorn.run(app, host="0.0.0.0", port=port)
