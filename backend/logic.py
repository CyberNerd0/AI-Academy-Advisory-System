from sqlalchemy.orm import Session
from typing import List, Dict, Tuple
from . import models

def calculate_gpa_metrics(results: List[models.Result]) -> Dict:
    """
    Calculates the GPA metrics for a given list of results.
    This function is used for both Semester GPA (passing results for one semester)
    and CGPA (passing results for all semesters).
    
    Formula:
    TNU (Total Number of Units) = Sum of Credits for all registered courses
    TGP (Total Grade Points) = Sum of (Grade Point * Credits)
    GPA = TGP / TNU
    """
    tnu = 0  # Total Number of Units (Credits)
    tgp = 0.0  # Total Grade Points

    for result in results:
        # We assume all results passed in are valid for calculation.
        # In some systems, 'F' grades count towards TNU but contribute 0 to TGP.
        # Here we follow the standard:
        credits = result.credits
        grade_point = float(result.grade_point)

        tnu += credits
        tgp += (grade_point * credits)

    gpa = 0.0
    if tnu > 0:
        gpa = tgp / tnu

    return {
        "tnu": tnu,
        "tgp": round(tgp, 2),
        "gpa": round(gpa, 2)
    }

def calculate_student_cgpa(student_id: int, db: Session) -> Dict:
    """
    Retrieves all results for a student and calculates the Cumulative Grade Point Average (CGPA).
    
    Returns:
        Dict containing 'cgpa', 'total_credits_earned', and 'total_grade_points'.
    """
    # 1. Fetch all results for the student
    all_results = db.query(models.Result).filter(models.Result.student_id == student_id).all()

    # 2. Calculate metrics using the helper function
    metrics = calculate_gpa_metrics(all_results)

    # 3. Return the cumulative data
    return {
        "student_id": student_id,
        "cgpa": metrics["gpa"],
        "total_credits_attempted": metrics["tnu"],
        "total_grade_points": metrics["tgp"]
    }

def check_course_eligibility(student_id: int, course_id: int, db: Session) -> Tuple[bool, str]:
    """
    Determines if a student is eligible to take a specific course based on prerequisites.
    
    Logic:
    1. Identify all prerequisites for the target course.
    2. Check if the student has passed each prerequisite.
    3. If any prerequisite is missing or failed, eligibility is denied.
    
    Returns:
        Tuple (is_eligible: bool, message: str)
    """
    # 1. Get the target course to ensure it exists
    target_course = db.query(models.Course).filter(models.Course.course_id == course_id).first()
    if not target_course:
        return False, "Course not found."

    # 2. Find all prerequisites for this course
    # Query the Prerequisites table where course_id matches the target
    prereq_entries = db.query(models.Prerequisite).filter(models.Prerequisite.course_id == course_id).all()
    
    if not prereq_entries:
        return True, "No prerequisites required."

    missing_prereqs = []

    for entry in prereq_entries:
        prereq_course_id = entry.prerequisite_course_id
        
        # 3. Check if student has a passing grade for this prerequisite
        # We look for a result for this student and this prerequisite course
        # Assuming 'F' is the failing grade. Adjust logic if 'D' is also fail.
        passed_prereq = db.query(models.Result).filter(
            models.Result.student_id == student_id,
            models.Result.course_id == prereq_course_id,
            models.Result.grade != 'F' # Rule: Must not be F
        ).first()

        if not passed_prereq:
            # Get the name of the missing course for the message
            prereq_course = db.query(models.Course).filter(models.Course.course_id == prereq_course_id).first()
            course_name = prereq_course.course_code if prereq_course else f"ID {prereq_course_id}"
            missing_prereqs.append(course_name)

    # 4. Final Decision
    if missing_prereqs:
        return False, f"Missing prerequisites: {', '.join(missing_prereqs)}"
    
    return True, "Eligible."

# --- Usage Examples (for demonstration/testing) ---
if __name__ == "__main__":
    # This block is for manual testing and explanation purposes.
    # It mocks the database objects to demonstrate logic without a live DB connection.
    
    print("--- Logic Demonstration ---")
    
    # Mock Results for a student
    class MockResult:
        def __init__(self, grade_point, credits, grade):
            self.grade_point = grade_point
            self.credits = credits
            self.grade = grade

    # Student took 3 courses: A (4.0), B (3.0), C (2.0)
    mock_results = [
        MockResult(4.0, 3, 'A'),
        MockResult(3.0, 3, 'B'),
        MockResult(2.0, 2, 'C')
    ]
    
    print(f"Calculating GPA for 3 mock courses...")
    gpa_data = calculate_gpa_metrics(mock_results)
    print(f"TNU (Total Units): {gpa_data['tnu']}")
    print(f"TGP (Total Points): {gpa_data['tgp']}")
    print(f"GPA: {gpa_data['gpa']}")
    
    print("\n--- Prerequisite Check Explanation ---")
    print("To check eligibility for 'Advanced Java':")
    print("1. System looks up prerequisites for 'Advanced Java' -> finds 'Intro to Java'.")
    print("2. System queries Student's results for 'Intro to Java'.")
    print("3. If result exists AND grade != 'F', returns True.")
    print("4. Otherwise, returns False with message 'Missing: Intro to Java'.")
