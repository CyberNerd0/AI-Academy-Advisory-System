from sqlalchemy.orm import Session
from typing import Dict, List
import re
import models, logic

def get_student_context(student_id: int, db: Session) -> Dict:
    """
    Retrieves the full academic context for a student to feed into the AI.
    This acts as the 'Retrieval' step in RAG.
    """
    # 1. Get Basic Student Info
    student = db.query(models.Student).filter(models.Student.student_id == student_id).first()
    if not student:
        return None

    # 2. Get Performance Metrics (GPA/CGPA)
    cgpa_data = logic.calculate_student_cgpa(student_id, db)

    # 3. Get Course Eligibility Status
    # We reuse the logic from the dashboard to see what is blocked and why.
    all_courses = db.query(models.Course).all()
    course_status_map = {}
    
    for course in all_courses:
        # Check if passed
        passed = db.query(models.Result).filter(
            models.Result.student_id == student_id,
            models.Result.course_id == course.course_id,
            models.Result.grade != 'F'
        ).first()

        if passed:
            status = "Completed"
            reason = "Passed"
        else:
            is_eligible, reason = logic.check_course_eligibility(student_id, course.course_id, db)
            status = "Eligible" if is_eligible else "Blocked"
            
        course_status_map[course.course_code] = {
            "name": course.course_name,
            "status": status,
            "reason": reason,
            "credits": course.credits
        }

    return {
        "student_name": f"{student.first_name} {student.last_name}",
        "cgpa": cgpa_data["cgpa"],
        "courses": course_status_map
    }

def heuristic_intent_analysis(question: str, context: Dict) -> str:
    """
    A rule-based 'AI' that analyzes the question and context to generate a response.
    In a full production system, this would be replaced by an LLM call (e.g., OpenAI API)
    passing the 'context' JSON as the system prompt.
    
    For the MVP/Defense, this deterministic logic ensures the demo never fails.
    """
    question_lower = question.lower()
    
    # Scenario 1: "Why can't I take [Course]?"
    # Regex to extract course code (e.g., "CSC301", "MTH101")
    match = re.search(r'\b([a-z]{3}\d{3})\b', question_lower)
    if ("why" in question_lower or "can't" in question_lower) and match:
        course_code = match.group(1).upper()
        course_data = context["courses"].get(course_code)
        
        if not course_data:
            return f"I couldn't find a course with code {course_code} in our curriculum."
            
        if course_data["status"] == "Blocked":
            return f"You cannot take {course_code}: {course_data['name']} yet because: {course_data['reason']}"
        elif course_data["status"] == "Completed":
            return f"You have already completed {course_code}. Good job!"
        else:
            return f"You are currently eligible to take {course_code}. There are no missing prerequisites."

    # Scenario 2: "How can I improve my CGPA?"
    if "improve" in question_lower and ("cgpa" in question_lower or "gpa" in question_lower):
        current_cgpa = context["cgpa"]
        advice = f"Your current CGPA is {current_cgpa}. "
        
        if current_cgpa < 2.0:
            advice += "You are at risk. Focus on retaking failed courses immediately to replace the 'F' grades."
        elif current_cgpa < 3.5:
            advice += "To boost this, prioritize courses with higher credit units (3 or 4 credits) as they have a heavier weight on your GPA."
        else:
            advice += "You are doing great! Maintain your performance by keeping up with attendance and continuous assessments."
            
        return advice

    # Fallback for unknown questions
    return "I am an academic advisor AI. I can answer questions about your course eligibility (e.g., 'Why can't I take CSC401?') or your academic performance."

def ask_academic_advisor(student_id: int, question: str, db: Session) -> str:
    """
    Main entry point for the Chatbot.
    1. Fetches Context (RAG)
    2. Generates Response (Heuristic/AI)
    """
    # 1. Retrieval
    context = get_student_context(student_id, db)
    if not context:
        return "Student record not found."

    # 2. Generation (Augmented by Context)
    response = heuristic_intent_analysis(question, context)
    
    return response

# --- Usage Example ---
if __name__ == "__main__":
    # Mocking DB for demonstration
    print("--- AI Advisor Demo ---")
    
    # Mock Context (what get_student_context would return)
    mock_context = {
        "student_name": "John Doe",
        "cgpa": 2.4,
        "courses": {
            "CSC499": {"name": "Capstone Project", "status": "Blocked", "reason": "Missing prerequisites: CSC301"},
            "CSC301": {"name": "Software Engineering", "status": "Eligible", "reason": "Eligible"}
        }
    }
    
    print("Context Loaded: John Doe, CGPA 2.4")
    
    q1 = "Why can't I take CSC499?"
    print(f"\nStudent: {q1}")
    print(f"Advisor: {heuristic_intent_analysis(q1, mock_context)}")
    
    q2 = "How can I improve my CGPA?"
    print(f"\nStudent: {q2}")
    print(f"Advisor: {heuristic_intent_analysis(q2, mock_context)}")
