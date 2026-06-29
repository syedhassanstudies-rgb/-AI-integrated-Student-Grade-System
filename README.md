# Student Grade System

A command-line student grade management system with AI-powered study recommendations, built with Python, PostgreSQL, and SQLAlchemy ORM.

## Features

- Add, view, and delete students
- Record grades per subject for each student
- View full academic transcripts with GPA calculation
- Filter students by ID or roll number
- AI-generated study recommendations using Groq LLaMA — identifies weak subjects and suggests targeted improvements
- Color-coded GPA display (green / yellow / red)
- Persistent storage via PostgreSQL — data survives after the app closes
- Seed script to populate the database with realistic test data

## Tech Stack

- Python 3.11
- FastAPI (PostgreSQL driver via psycopg2-binary)
- SQLAlchemy ORM
- PostgreSQL
- Groq API (LLaMA 4 Scout — `meta-llama/llama-4-scout-17b-16e-instruct`)
- python-dotenv

## Project Structure

```
student-grade-system/
├── main.py           # CLI interface and entry point
├── repository.py     # All database operations (CRUD, GPA, transcript)
├── student.py        # Student SQLAlchemy model
├── grade.py          # Grade SQLAlchemy model with foreign key
├── database.py       # Engine, session factory, Base, init_db
├── ai_helper.py      # Groq AI study recommendation
├── seed.py           # Populates database with test data
├── .env              # Environment variables (never committed)
├── .env.example      # Template showing required variables
└── requirements.txt
```

## Setup

### 1. Prerequisites

- Python 3.11+
- PostgreSQL installed and running
- A Groq API key (free at [console.groq.com](https://console.groq.com))

### 2. Create the database

Open your PostgreSQL shell and run:

```sql
CREATE DATABASE grade_system;
```

### 3. Clone and set up the environment

```bash
git clone https://github.com/syedhassanstudies-rgb/student-grade-system
cd student-grade-system
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root (use `.env.example` as a template):

```
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/grade_system
GROQ_API_KEY=your_groq_key_here
```

### 5. Run the app

```bash
python main.py
```

### 6. (Optional) Seed test data

```bash
python seed.py
```

This populates the database with 5 students and realistic grade data so every menu option has real data to interact with immediately.

## How It Works

### Database Layer

`database.py` creates a SQLAlchemy engine and session factory bound to your PostgreSQL instance. `init_db()` reads all models that inherit from `Base` and creates the corresponding tables on first run — no manual SQL required.

### Models

`Student` and `Grade` are SQLAlchemy models mapped directly to PostgreSQL tables. The `Grade` table holds a `student_id` foreign key referencing `students.id`, enforcing referential integrity at the database level — PostgreSQL will reject any grade that references a non-existent student.

### Repository Pattern

All database operations live in `repository.py` as plain functions. Every function opens its own session and closes it in a `finally` block, guaranteeing the connection is released even if something fails mid-operation.

### GPA Calculation

GPA is calculated on a 0–4 scale from the percentage of total marks obtained across all of a student's grades:

```
percentage = (sum of marks_obtained / sum of total_marks) × 100
gpa = round((percentage / 100) × 4, 2)
```

### AI Feature

When you request an AI study recommendation, the app fetches the student's full transcript, builds a structured prompt with their grades and GPA, and sends it to Groq LLaMA 4 Scout. The model identifies which subjects need the most improvement and provides a specific, actionable study suggestion in 3–4 sentences.

## Key Concepts

| Concept | Where Used |
|---|---|
| SQLAlchemy ORM | student.py, grade.py, repository.py |
| Foreign keys | grade.py — `ForeignKey("students.id")` |
| Session management | repository.py — try/finally pattern |
| `session.refresh()` | After every commit — prevents DetachedInstanceError |
| Environment variables | database.py, ai_helper.py via python-dotenv |
| ANSI color codes | main.py — green/yellow/red GPA display |
| Input validation | main.py — `get_valid_int()` retry loop |
| try/except Exception | main.py — wraps AI network call for graceful failure |