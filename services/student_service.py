from database import db
from bson import ObjectId

async def create_student_service(student_data):
    result = await db.students.insert_one(student_data.dict())
    return {"id": str(result.inserted_id)}

async def list_students_service(country=None, age=None):
    query = {}
    if country:
        query["address.country"] = country
    if age:
        query["age"] = {"$gte": age}
    students = await db.students.find(query).to_list(1000)
    if country and age:
        students = [student for student in students if student["address"]["country"] == country and student["age"] >= age]
    for student in students:
        student["id"] = str(student["_id"])
        student.pop("_id")
    return {"data": students}

async def fetch_student_service(student_id):
    student = await db.students.find_one({"_id": ObjectId(student_id)})
    if student:
        student["id"] = str(student["_id"])
        student.pop("_id")
    return student

async def update_student_service(student_id, update_data):
    await db.students.update_one({"_id": ObjectId(student_id)}, {"$set": update_data.dict(exclude_unset=True)})

async def delete_student_service(student_id):
    await db.students.delete_one({"_id": ObjectId(student_id)})
