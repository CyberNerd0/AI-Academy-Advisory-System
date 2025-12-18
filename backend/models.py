from sqlalchemy import Column, Integer, String, Date, ForeignKey, DECIMAL
from sqlalchemy.orm import relationship
from .database import Base

class Student(Base):
    """
    Represents a student in the university.
    """
    __tablename__ = "students"

    student_id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    enrollment_year = Column(Integer, nullable=False)
    level = Column(Integer, nullable=False) # e.g., 100, 200

    # Relationship to Results: One student has many results
    results = relationship("Result", back_populates="student")


class Course(Base):
    """
    Represents an academic course offered by the department.
    """
    __tablename__ = "courses"

    course_id = Column(Integer, primary_key=True, index=True)
    course_code = Column(String, unique=True, nullable=False) # e.g., CSC101
    course_name = Column(String, nullable=False)
    credits = Column(Integer, nullable=False)
    semester_offered = Column(Integer, nullable=False) # 1 or 2
    department = Column(String, nullable=False)

    # Relationship to Results: One course appears in many results
    results = relationship("Result", back_populates="course")
    
    # Relationships for Prerequisites
    # We will define the Prerequisite table explicitly below
    

class Semester(Base):
    """
    Represents an academic semester (e.g., 2023/2024 First Semester).
    """
    __tablename__ = "semesters"

    semester_id = Column(Integer, primary_key=True, index=True)
    semester_name = Column(String, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)

    # Relationship to Results: One semester has many results
    results = relationship("Result", back_populates="semester")


class Result(Base):
    """
    Links a Student, Course, and Semester to record a grade.
    This is the core table for calculating GPA/CGPA.
    """
    __tablename__ = "results"

    result_id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.student_id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.course_id"), nullable=False)
    semester_id = Column(Integer, ForeignKey("semesters.semester_id"), nullable=False)
    grade = Column(String, nullable=False) # e.g., 'A', 'B'
    grade_point = Column(DECIMAL(3, 2), nullable=False) # e.g., 4.00
    credits = Column(Integer, nullable=False) # Credits earned

    # Relationships
    student = relationship("Student", back_populates="results")
    course = relationship("Course", back_populates="results")
    semester = relationship("Semester", back_populates="results")


class Prerequisite(Base):
    """
    Defines prerequisite rules. 
    A course (course_id) may require another course (prerequisite_course_id) to be passed first.
    """
    __tablename__ = "prerequisites"

    prerequisite_id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.course_id"), nullable=False)
    prerequisite_course_id = Column(Integer, ForeignKey("courses.course_id"), nullable=False)

    # Relationships to Course
    # We use 'foreign_keys' to specify which column the relationship refers to
    course = relationship("Course", foreign_keys=[course_id])
    prerequisite_course = relationship("Course", foreign_keys=[prerequisite_course_id])
