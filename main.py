from fastapi import FastAPI
from routes.student_routes import router as student_router
from database import init_db

app = FastAPI()

# Initialize database
init_db()

# Include routes
app.include_router(student_router, prefix="/students", tags=["Students"])

@app.get("/")
def root():
    return {"message": "Welcome to the Student Management API"}
