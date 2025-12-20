from sqlalchemy.orm import Session
from datetime import date
from backend import models, database
from backend.database import engine

# Create tables if they don't exist
models.Base.metadata.create_all(bind=engine)

def seed_data():
    db = database.SessionLocal()
    
    # Check if data exists
    if db.query(models.Student).first():
        print("Data already seeded.")
        return

    print("Seeding data...")

    # 1. Students
    student1 = models.Student(
        student_id=1,
        first_name="John",
        last_name="Doe",
        email="john@uni.edu",
        enrollment_year=2023,
        level=300
    )
    db.add(student1)

    # 2. Semesters
    sem1 = models.Semester(semester_id=1, semester_name="Year 1 Sem 1", start_date=date(2023, 1, 1), end_date=date(2023, 5, 1))
    sem2 = models.Semester(semester_id=2, semester_name="Year 1 Sem 2", start_date=date(2023, 6, 1), end_date=date(2023, 10, 1))
    db.add_all([sem1, sem2])
    
    # 3. Courses
    # Year 1 Courses
    c_math = models.Course(course_code="MTH101", course_name="Calculus I", credits=3, semester_offered=1, department="Math")
    c_java = models.Course(course_code="CSC101", course_name="Intro to Java", credits=3, semester_offered=1, department="CS")
    c_eng = models.Course(course_code="GST101", course_name="Use of English", credits=2, semester_offered=1, department="General")
    
    # Year 2/3 Courses (include Prerequisites)
    c_ds = models.Course(course_code="CSC201", course_name="Data Structures", credits=3, semester_offered=1, department="CS")
    c_adv_java = models.Course(course_code="CSC301", course_name="Advanced Java", credits=4, semester_offered=1, department="CS")
    c_capstone = models.Course(course_code="CSC499", course_name="Capstone Project", credits=6, semester_offered=2, department="CS")
    
    db.add_all([c_math, c_java, c_eng, c_ds, c_adv_java, c_capstone])
    db.commit() # Commit courses to get IDs for foreign keys

    # 4. Prerequisites
    # Data Structures needs Intro to Java
    p1 = models.Prerequisite(course_id=c_ds.course_id, prerequisite_course_id=c_java.course_id)
    # Advanced Java needs Data Structures
    p2 = models.Prerequisite(course_id=c_adv_java.course_id, prerequisite_course_id=c_ds.course_id)
    # Capstone needs Advanced Java
    p3 = models.Prerequisite(course_id=c_capstone.course_id, prerequisite_course_id=c_adv_java.course_id)
    
    db.add_all([p1, p2, p3])

    # 5. Results (John Doe's History)
    # Passed Math and English
    r1 = models.Result(student_id=1, course_id=c_math.course_id, semester_id=1, grade='A', grade_point=4.0, credits=3)
    r2 = models.Result(student_id=1, course_id=c_eng.course_id, semester_id=1, grade='B', grade_point=3.0, credits=2)
    # Failed Intro to Java (Will block Data Structures)
    r3 = models.Result(student_id=1, course_id=c_java.course_id, semester_id=1, grade='F', grade_point=0.0, credits=3)
    
    db.add_all([r1, r2, r3])
    
    db.commit()
    print("Seeding Complete!")
    db.close()

if __name__ == "__main__":
    seed_data()
