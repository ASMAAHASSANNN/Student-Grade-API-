# Student Grades API

A simple REST API built with **FastAPI** for a **Software Requirements Engineering** lab.

This project is meant to be shared through **GitHub** so that colleagues can:
- clone the repository
- install the dependencies
- run the API locally
- test the endpoints using Swagger UI or cURL

---

## What this API does

This API manages grades for students.

It provides **3 endpoints**:
1. **Add a grade** for a student
2. **Get all grades** for a student
3. **Get the average grade** for a student

---

## API Endpoints

### 1. Add a grade
**POST** `/students/{student_id}/grades`

Adds a grade for a specific student.

#### Path parameter
- `student_id` — must be an integer greater than `0`

#### Request body example
```json
{
  "course": "Software Requirements Engineering",
  "score": 85,
  "semester": "Semester 1"
}
```

#### Success response
- `201 Created`

#### Error responses
- `400 Bad Request` — duplicate grade for same course and semester
- `422 Unprocessable Entity` — invalid input data

---

### 2. Get all grades for a student
**GET** `/students/{student_id}/grades`

Returns all grades stored for a student.

#### Success response
- `200 OK`

#### Error responses
- `404 Not Found` — no grades found for the student

---

### 3. Get average grade for a student
**GET** `/students/{student_id}/average`

Calculates and returns the student’s average score.

#### Success response
- `200 OK`

#### Error responses
- `404 Not Found` — no grades found for the student

---

## Validation Rules

The API uses **FastAPI + Pydantic** validation.

Rules in this project:
- `student_id` must be greater than `0`
- `course` must be between `2` and `50` characters
- `score` must be between `0` and `100`
- `semester` must be either:
  - `Semester 1`
  - `Semester 2`

---

## Error Handling

The API returns JSON error responses.

Examples:
- invalid request body → `422`
- duplicate course in same semester → `400`
- missing student records → `404`

---

## Project Structure

```text
student-grades-api/
├── main.py
├── openapi.yaml
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Important GitHub Note

The virtual environment is **not** pushed to GitHub.

Just like `node_modules` in Node.js projects, `venv/` should be ignored because it contains local machine-specific files that can be recreated.

This project already includes a `.gitignore` file that ignores:
- `venv/`
- `.venv/`
- `__pycache__/`
- `.env`
- other local/dev files

So when pushing to GitHub, only the actual project files should go up.

---

## Requirements

Install these first:
- Python 3.10+
- pip
- Git

---

## How to Install and Run the API

### Step 1: Clone the repository
After this project is pushed to GitHub, your colleagues can clone it with:

```bash
git clone <your-github-repo-url>
cd student-grades-api
```

---

### Step 2: Create a virtual environment

#### Windows
```bash
python -m venv venv
venv\Scripts\activate
```

#### macOS / Linux
```bash
python3 -m venv venv
source venv/bin/activate
```

---

### Step 3: Install dependencies
```bash
pip install -r requirements.txt
```

---

### Step 4: Start the FastAPI server
```bash
uvicorn main:app --reload
```

If everything works, the API should run on:

```text
http://127.0.0.1:8000
```

---

## API Documentation in Browser

Once the server is running, open:

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`
- OpenAPI JSON: `http://127.0.0.1:8000/openapi.json`

Swagger UI is the easiest place to test the API.

---

## How to Test the API

### Option A: Test in Swagger UI

1. Open `http://127.0.0.1:8000/docs`
2. Expand an endpoint
3. Click **Try it out**
4. Enter values
5. Click **Execute**
6. Check the response body and status code

---

### Option B: Test using cURL

#### Test 1 — Add first grade
```bash
curl -X POST "http://127.0.0.1:8000/students/1/grades" \
-H "Content-Type: application/json" \
-d '{
  "course": "Software Requirements Engineering",
  "score": 85,
  "semester": "Semester 1"
}'
```

#### Test 2 — Add second grade
```bash
curl -X POST "http://127.0.0.1:8000/students/1/grades" \
-H "Content-Type: application/json" \
-d '{
  "course": "Computer Networks",
  "score": 74,
  "semester": "Semester 2"
}'
```

#### Test 3 — Get all grades
```bash
curl "http://127.0.0.1:8000/students/1/grades"
```

#### Test 4 — Get average
```bash
curl "http://127.0.0.1:8000/students/1/average"
```

---

## Invalid Test Cases

### Invalid score
```bash
curl -X POST "http://127.0.0.1:8000/students/1/grades" \
-H "Content-Type: application/json" \
-d '{
  "course": "Security",
  "score": 150,
  "semester": "Semester 1"
}'
```
Expected:
- `422 Unprocessable Entity`

### Invalid semester
```bash
curl -X POST "http://127.0.0.1:8000/students/1/grades" \
-H "Content-Type: application/json" \
-d '{
  "course": "Security",
  "score": 70,
  "semester": "Term 3"
}'
```
Expected:
- `422 Unprocessable Entity`

### Duplicate course in same semester
```bash
curl -X POST "http://127.0.0.1:8000/students/1/grades" \
-H "Content-Type: application/json" \
-d '{
  "course": "Software Requirements Engineering",
  "score": 90,
  "semester": "Semester 1"
}'
```
Expected:
- `400 Bad Request`

### Student with no grades
```bash
curl "http://127.0.0.1:8000/students/99/grades"
```
Expected:
- `404 Not Found`

---

## How to Push This Project to GitHub

### 1. Create a new empty repository on GitHub
On GitHub:
1. Sign in
2. Click **New repository**
3. Name it `student-grades-api`
4. Keep it empty
   - do **not** add a README
   - do **not** add a `.gitignore`
5. Create repository

---

### 2. Open terminal in this project folder
Run:

```bash
git init
git add .
git commit -m "Initial Student Grades API"
git branch -M main
git remote add origin <your-github-repo-url>
git push -u origin main
```

Replace:
```bash
<your-github-repo-url>
```
with something like:
```bash
https://github.com/your-username/student-grades-api.git
```

---

## How Colleagues Can Use It After You Push

They only need to run:

```bash
git clone <your-github-repo-url>
cd student-grades-api
python -m venv venv
```

#### Windows
```bash
venv\Scripts\activate
```

#### macOS / Linux
```bash
source venv/bin/activate
```

Then:

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

Then open:

```text
http://127.0.0.1:8000/docs
```

---

## Summary

This project demonstrates:
- API contract design using OpenAPI
- REST API implementation using FastAPI
- input validation
- error handling
- project sharing through GitHub
- easy testing through Swagger UI
