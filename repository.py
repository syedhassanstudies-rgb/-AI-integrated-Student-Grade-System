from typing import Optional, List
from student import Student
from database import get_session
from grade import Grade
from sqlalchemy.exc import IntegrityError

def create_student(name: str, roll_number: str, department: Optional[str] = None) -> Student:
        session = get_session()
        try:
                new_student = Student(
                        name = name,
                        roll_number = roll_number,
                        department = department,
                )
                session.add(new_student)
                session.commit()
                session.refresh(new_student)
                return new_student
        except IntegrityError:
                session.rollback()
                print(f"A student with roll number '{roll_number}' already exists.")
                return None
        finally:
                session.close()

def  get_student_by_id(student_id: int) -> Optional[Student]:
        session = get_session()
        try:
                return session.query(Student).filter(Student.id == student_id).first()
        finally:
                session.close()

def get_all_students() -> List[Student]:
        session = get_session()
        try:
                return session.query(Student).all()
        finally:
                session.close()
def delete_student(student_id: int) -> bool:
        session = get_session()
        try:
                student = session.query(Student).filter(Student.id == student_id).first()
                if not student:
                        return False
                session.query(Grade).filter(Grade.student_id == student_id).delete()
                session.delete(student)
                session.commit()
                return True
        except Exception:
                session.rollback()
                raise
        finally:
                session.close()

def add_grade(student_id: int, subject: str, marks_obtained: int, total_marks: int) -> Optional[Grade]:
        if marks_obtained > total_marks:
                print("Obtained Marks cannot be greated then total Marks")
                return None

        session = get_session()
        try:
                student = session.query(Student).filter(Student.id == student_id).first()
                if not student:
                        print(f"No student found with id {student_id}.")
                        return None
                new_grade = Grade(
                        student_id = student_id,
                        subject = subject,
                        marks_obtained = marks_obtained,
                        total_marks = total_marks,
                )
                session.add(new_grade)
                session.commit()
                session.refresh(new_grade)
                return new_grade
        finally:
                session.close()

def get_grades_by_student(student_id : int) -> List[Grade]:
        session = get_session()
        try :
                return session.query(Grade).filter(Grade.student_id == student_id).all()
        finally:
                session.close()

def calculate_gpa(student_id: int) -> Optional[float]:
        session = get_session()
        try:
                grades = session.query(Grade).filter(Grade.student_id == student_id).all()
                if not grades:
                        return None
                total_obtained = sum(g.marks_obtained for g in grades)
                total_possible = sum(g.total_marks for g in grades)

                if total_possible == 0:
                        return None

                percentage = (total_obtained / total_possible) * 100
                return round((percentage / 100) * 4, 2)
        finally:
                session.close()

def get_transcript(student_id: int) -> Optional[dict]:
        session = get_session()
        try:
                student = session.query(Student).filter(Student.id == student_id).first()
                if not student:
                        return None
                grades = session.query(Grade).filter(Grade.student_id == student_id).all()
        finally:
                session.close()

        gpa = calculate_gpa(student_id)
        return {
                "student": student,
                "grades" : grades,
                "gpa" : gpa,
                }

