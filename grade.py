from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
from database import Base

class Grade(Base):
    __tablename__ = "grades"
    id = Column(Integer, primary_key=True)
    subject = Column(String, nullable=False)
    marks_obtained = Column(Integer, nullable=False)
    total_marks = Column(Integer, nullable=False)
    student_id = Column(Integer, ForeignKey("students.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
