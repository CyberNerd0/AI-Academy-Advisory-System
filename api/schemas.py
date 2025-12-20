from pydantic import BaseModel
from typing import List, Optional
from datetime import date

# --- Student Schemas ---
class StudentBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    enrollment_year: int
    level: int

class StudentCreate(StudentBase):
    pass

class StudentResponse(StudentBase):
    student_id: int

    class Config:
        orm_mode = True

# --- Course Schemas ---
class CourseBase(BaseModel):
    course_code: str
    course_name: str
    credits: int
    semester_offered: int
    department: str

class CourseCreate(CourseBase):
    pass

class CourseResponse(CourseBase):
    course_id: int

    class Config:
        orm_mode = True

# --- Semester Schemas ---
class SemesterBase(BaseModel):
    semester_name: str
    start_date: date
    end_date: date

class SemesterCreate(SemesterBase):
    pass

class SemesterResponse(SemesterBase):
    semester_id: int

    class Config:
        orm_mode = True

# --- Result Schemas ---
class ResultBase(BaseModel):
    student_id: int
    course_id: int
    semester_id: int
    grade: str
    grade_point: float
    credits: int

class ResultCreate(ResultBase):
    pass

class ResultResponse(ResultBase):
    result_id: int
    # We can include nested objects here if needed, e.g., course details
    course: Optional[CourseResponse] = None
    semester: Optional[SemesterResponse] = None

    class Config:
        orm_mode = True

# --- Prerequisite Schemas ---
class PrerequisiteBase(BaseModel):
    course_id: int
    prerequisite_course_id: int

class PrerequisiteCreate(PrerequisiteBase):
    pass

class PrerequisiteResponse(PrerequisiteBase):
    prerequisite_id: int

    class Config:
        orm_mode = True
