"""
seed.py
Populates the database with realistic test data.
Run once after setting up the project to have meaningful data to test with.
Skips students that already exist in the database.
"""

from database import init_db
from repository import create_student, add_grade


def seed() -> None:
    init_db()
    print("\n🌱 Seeding database with test data...\n")

    students_data = [
        {
            "name": "Hassan Zaidi",
            "roll_number": "24BSIT21",
            "department": "Information Technology",
            "grades": [
                ("Database Systems", 88, 100),
                ("Operating Systems", 75, 100),
                ("Calculus", 65, 100),
                ("Programming Fundamentals", 92, 100),
                ("English Communication", 80, 100),
            ],
        },
        {
            "name": "Ali Khan",
            "roll_number": "24BSIT05",
            "department": "Information Technology",
            "grades": [
                ("Database Systems", 70, 100),
                ("Operating Systems", 65, 100),
                ("Calculus", 55, 100),
                ("Programming Fundamentals", 78, 100),
            ],
        },
        {
            "name": "Sara Ahmed",
            "roll_number": "24BSIT12",
            "department": "Computer Science",
            "grades": [
                ("Data Structures", 95, 100),
                ("Discrete Mathematics", 90, 100),
                ("Linear Algebra", 85, 100),
            ],
        },
        {
            "name": "Usman Malik",
            "roll_number": "24BSIT08",
            "department": "Information Technology",
            "grades": [
                ("Database Systems", 50, 100),
                ("Operating Systems", 45, 100),
                ("Calculus", 40, 100),
            ],
        },
        {
            "name": "Ayesha Raza",
            "roll_number": "24BSIT17",
            "department": "Software Engineering",
            "grades": [
                ("Object Oriented Programming", 91, 100),
                ("Web Technologies", 87, 100),
                ("Software Engineering", 83, 100),
                ("Computer Networks", 76, 100),
            ],
        },
    ]

    for s_data in students_data:
        student = create_student(
            name=s_data["name"],
            roll_number=s_data["roll_number"],
            department=s_data["department"],
        )
        if student:
            for subject, marks_obtained, total_marks in s_data["grades"]:
                add_grade(student.id, subject, marks_obtained, total_marks)
            print(f"  ✓ Added {student.name} with {len(s_data['grades'])} grades")
        else:
            print(f"  ⚠  Skipped {s_data['name']} — already exists")

    print("\n✅ Seed complete. Database is ready.\n")


if __name__ == "__main__":
    seed()