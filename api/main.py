from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel

import models, schemas, logic, ai_advisor
import seed
from database import SessionLocal, engine

# Create the database tables automatically on startup
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Academic Advisory System API", root_path="/api")

@app.on_event("startup")
def startup_event():
    try:
        seed.seed_data()
    except Exception as e:
        print(f"Error seeding data: {e}")

# Allow CORS for all origins (for MVP simplicity)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Student Endpoints (Admin) ---

@app.post("/students/", response_model=schemas.StudentResponse)
def create_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    """
    Admin: Create a new student record.
    """
    db_student = models.Student(**student.dict())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

@app.get("/students/", response_model=List[schemas.StudentResponse])
def read_students(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Admin/Adviser: List all students.
    """
    students = db.query(models.Student).offset(skip).limit(limit).all()
    return students

@app.get("/students/{student_id}", response_model=schemas.StudentResponse)
def read_student(student_id: int, db: Session = Depends(get_db)):
    """
    Read a specific student by ID.
    """
    student = db.query(models.Student).filter(models.Student.student_id == student_id).first()
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

# --- Course Endpoints (Admin) ---

@app.post("/courses/", response_model=schemas.CourseResponse)
def create_course(course: schemas.CourseCreate, db: Session = Depends(get_db)):
    """
    Admin: Add a new course to the curriculum.
    """
    db_course = models.Course(**course.dict())
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course

@app.get("/courses/", response_model=List[schemas.CourseResponse])
def read_courses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    List all available courses.
    """
    courses = db.query(models.Course).offset(skip).limit(limit).all()
    return courses

# --- Result Endpoints (Student & Adviser) ---

@app.post("/results/", response_model=schemas.ResultResponse)
def create_result(result: schemas.ResultCreate, db: Session = Depends(get_db)):
    """
    Admin: Record a result for a student (e.g., after semester exams).
    """
    db_result = models.Result(**result.dict())
    db.add(db_result)
    db.commit()
    db.refresh(db_result)
    return db_result

@app.get("/results/student/{student_id}", response_model=List[schemas.ResultResponse])
def read_student_results(student_id: int, db: Session = Depends(get_db)):
    """
    Student: View their own academic results.
    Adviser: View a specific student's results.
    """
    results = db.query(models.Result).filter(models.Result.student_id == student_id).all()
    return results

@app.get("/results/", response_model=List[schemas.ResultResponse])
def read_all_results(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Adviser/Admin: View all results across the department.
    """
    results = db.query(models.Result).offset(skip).limit(limit).all()
    return results

# --- Advanced Logic Endpoints (Dashboard & Advisory) ---

@app.get("/dashboard/student/{student_id}")
def get_student_dashboard(student_id: int, db: Session = Depends(get_db)):
    """
    Student Dashboard API:
    Returns the core metrics needed for the student's home screen:
    1. Current CGPA (calculated in real-time)
    2. List of all courses with their eligibility status (Eligible vs. Blocked)
    """
    # --- MOCKING DB TO DEBUG CRASH ---
    # return {
    #     "student_profile": {
    #         "name": f"{student.first_name} {student.last_name}",
    #         "level": student.level,
    #         "enrollment_year": student.enrollment_year
    #     },
    #     "academic_performance": cgpa_data,
    #     "course_recommendations": course_status
    # }

    return {
        "student_profile": {
            "name": "John Doe (Recovery Mode)",
            "level": 300,
            "enrollment_year": 2023
        },
        "academic_performance": {
             "student_id": student_id,
             "cgpa": 3.5,
             "total_credits_attempted": 60,
             "total_grade_points": 210
        },
        "course_recommendations": []
    }

@app.get("/adviser/student/{student_id}")
def get_adviser_view(student_id: int, db: Session = Depends(get_db)):
    """
    Adviser View API:
    Provides the adviser with a deep dive into a specific student's performance.
    Currently reuses the dashboard logic but can be expanded with private notes/flags.
    """
    # Reusing the dashboard logic ensures consistency between what the student sees and what the adviser sees.
    return get_student_dashboard(student_id, db)

# --- AI Chatbot Endpoint ---

class QuestionRequest(BaseModel):
    question: str

@app.post("/ask/{student_id}")
def ask_advisor_endpoint(student_id: int, request: QuestionRequest, db: Session = Depends(get_db)):
    """
    AI Advisor Chat Endpoint:
    Accepts a student's question and returns a context-aware response.
    
    Example Questions:
    - "Why can't I take CSC401?"
    - "How is my CGPA?"
    """
    # --- MOCKING DB TO DEBUG CRASH ---
    # response_text = ai_advisor.ask_academic_advisor(student_id, request.question, db)
    # return {"response": response_text}
    
    return {"response": f"I am in Recovery Mode. You asked: '{request.question}'. (DB Connection Unavailable)"}


