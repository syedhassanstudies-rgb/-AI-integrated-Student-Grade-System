from typing import Optional
from repository import (
    create_student,
    get_all_students,
    get_student_by_id,
    add_grade,
    get_transcript,
    delete_student,
)
from ai_helper import get_study_recommendation
from database import init_db

init_db()

GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"
BOLD = "\033[1m"


def get_gpa_color(gpa: float) -> str:
    if gpa >= 3.00:
        return GREEN
    elif gpa >= 2.80:
        return YELLOW
    else:
        return RED


def print_header() -> None:
    print(f"\n{BOLD}{'-' * 50}")
    print("        🎓  Student Grade System + AI")
    print(f"{'-' * 50}{RESET}")


def print_menu() -> None:
    print(f"""
{BOLD}What would you like to do?{RESET}
  1. Add a Student
  2. View all Students
  3. Add a Grade
  4. View a Student's Transcript
  5. Get AI Study Recommendation
  6. Delete a Student
  0. Exit
""")


def get_valid_int(prompt: str) -> int:
    while True:
        raw = input(prompt).strip()
        try:
            return int(raw)
        except ValueError:
            print("Please enter a valid whole number.")


def print_transcript(transcript: Optional[dict]) -> None:
    if not transcript:
        print("  Student not found.")
        return

    student = transcript["student"]
    grades = transcript["grades"]
    gpa = transcript["gpa"]

    print(f"\n{BOLD}{student.name}{RESET} (Roll No: {student.roll_number})")

    if not grades:
        print("  No grades recorded yet.")
        return

    print(f"  {'-' * 40}")
    for g in grades:
        print(f"  {g.subject:<20} {g.marks_obtained}/{g.total_marks}")
    print(f"  {'-' * 40}")

    if gpa is not None:
        color = get_gpa_color(gpa)
        print(f"  {BOLD}GPA: {color}{gpa}{RESET}")
    else:
        print("  GPA: Not available yet.")


def handle_add_student() -> None:
    print(f"\n{BOLD}New Student{RESET}")
    name = input("  Name: ").strip()
    if not name:
        print("  Name cannot be empty.")
        return

    roll_number = input("  Roll Number: ").strip()
    if not roll_number:
        print("  Roll number cannot be empty.")
        return

    department = input("  Department (optional): ").strip()
    department = department if department else None

    student = create_student(name, roll_number, department)
    if student:
        print(f"\n  Student '{student.name}' added with ID {student.id}.")


def handle_view_all_student() -> None:
    students = get_all_students()

    if not students:
        print("  No students found.")
        return

    print(f"\n  {'-' * 50}")
    for s in students:
        print(f"  [{s.id}] {s.name} — {s.roll_number} ({s.department or 'N/A'})")
    print(f"  {'-' * 50}")


def handle_add_grade() -> None:
    student_id = get_valid_int("  Student ID: ")
    student = get_student_by_id(student_id)
    if not student:
        print(f"  No student found with ID {student_id}.")
        return

    subject = input("  Subject: ").strip()
    if not subject:
        print("  Subject cannot be empty.")
        return

    marks_obtained = get_valid_int("  Marks obtained: ")
    total_marks = get_valid_int("  Total marks: ")
    grade = add_grade(student_id, subject, marks_obtained, total_marks)

    if grade:
        print(f"\n  Grade added: {grade.subject} — {grade.marks_obtained}/{grade.total_marks}")


def handle_view_transcript() -> None:
    student_id = get_valid_int("  Student ID: ")
    transcript = get_transcript(student_id)
    print_transcript(transcript)


def handle_ai_recommendation() -> None:
    student_id = get_valid_int("  Student ID: ")
    transcript = get_transcript(student_id)

    if not transcript or not transcript["grades"]:
        print("  Not enough data to generate a recommendation.")
        return

    print("\n  🤖 Generating study recommendation...")
    try:
        advice = get_study_recommendation(transcript)
        print(f"\n  {advice}")
    except Exception as e:
        print(f"  Could not generate a recommendation right now. ({e})")


def handle_delete_student() -> None:
    student_id = get_valid_int("  Student ID: ")
    confirm = input(f"  Delete student {student_id} and all their grades? (y/n): ").strip().lower()
    if confirm != "y":
        print("  Cancelled.")
        return

    deleted = delete_student(student_id)
    if deleted:
        print("  Student deleted.")
    else:
        print(f"  No student found with ID {student_id}.")


def main() -> None:
    print_header()
    while True:
        print_menu()
        choice = input("  Enter choice: ").strip()
        print()

        if choice == "1":
            handle_add_student()
        elif choice == "2":
            handle_view_all_student()
        elif choice == "3":
            handle_add_grade()
        elif choice == "4":
            handle_view_transcript()
        elif choice == "5":
            handle_ai_recommendation()
        elif choice == "6":
            handle_delete_student()
        elif choice == "0":
            print("  Goodbye. 👋")
            break
        else:
            print("  Invalid choice. Try again.")


if __name__ == "__main__":
    main()

    