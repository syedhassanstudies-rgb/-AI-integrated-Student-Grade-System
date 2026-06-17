import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def get_study_recommendation(transcript: dict) -> str:
    student = transcript["student"]
    grades = transcript["grades"]
    gpa = transcript["gpa"]

    grade_lines = "\n".join(
        f"{g.subject}: {g.marks_obtained}/{g.total_marks}" for g in grades
    )

    prompt = f"""You are an academic advisor. A student has the following results:

Student: {student.name}
GPA (out of 4.0): {gpa}

Grades:
{grade_lines}

In 3-4 sentences, identify which subject(s) need the most improvement and give one practical, specific study suggestion."""

    response = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=220,
        temperature=0.6,
    )

    return response.choices[0].message.content.strip()