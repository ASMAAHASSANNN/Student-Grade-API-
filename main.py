from typing import List, Literal, Annotated
from fastapi import FastAPI, HTTPException, Path
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

app = FastAPI(
    title="Student Grades API",
    version="1.0.0",
    description="A simple REST API for managing student grades"
)

# In-memory storage for lab/demo purposes
grades_db: dict[int, list[dict]] = {}
grade_counter = 1


# ---------------------------
# Pydantic models
# ---------------------------
class GradeCreate(BaseModel):
    course: str = Field(..., min_length=2, max_length=50, example="Software Engineering")
    score: float = Field(..., ge=0, le=100, example=78.5)
    semester: Literal["Semester 1", "Semester 2"]


class Grade(GradeCreate):
    grade_id: int


class GradesResponse(BaseModel):
    student_id: int
    grades: List[Grade]


class AverageResponse(BaseModel):
    student_id: int
    average: float


class ErrorResponse(BaseModel):
    detail: str


# ---------------------------
# Custom validation handler
# ---------------------------
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=422,
        content={
            "detail": "Validation error",
            "errors": exc.errors()
        }
    )


# ---------------------------
# Endpoints
# ---------------------------
@app.post(
    "/students/{student_id}/grades",
    response_model=Grade,
    status_code=201,
    responses={
        400: {"model": ErrorResponse},
        422: {"model": ErrorResponse}
    }
)
def add_grade(
    student_id: Annotated[int, Path(gt=0, description="Student ID must be greater than 0")],
    grade: GradeCreate
):
    global grade_counter

    student_grades = grades_db.get(student_id, [])

    # Example business rule: same course in same semester should not be duplicated
    for g in student_grades:
        if g["course"].lower() == grade.course.lower() and g["semester"] == grade.semester:
            raise HTTPException(
                status_code=400,
                detail=f"Grade for course '{grade.course}' in {grade.semester} already exists for this student."
            )

    new_grade = {
        "grade_id": grade_counter,
        "course": grade.course,
        "score": grade.score,
        "semester": grade.semester
    }

    student_grades.append(new_grade)
    grades_db[student_id] = student_grades
    grade_counter += 1

    return new_grade


@app.get(
    "/students/{student_id}/grades",
    response_model=GradesResponse,
    responses={404: {"model": ErrorResponse}}
)
def get_student_grades(
    student_id: Annotated[int, Path(gt=0, description="Student ID must be greater than 0")]
):
    if student_id not in grades_db or len(grades_db[student_id]) == 0:
        raise HTTPException(status_code=404, detail="No grades found for this student.")

    return {
        "student_id": student_id,
        "grades": grades_db[student_id]
    }


@app.get(
    "/students/{student_id}/average",
    response_model=AverageResponse,
    responses={404: {"model": ErrorResponse}}
)
def get_student_average(
    student_id: Annotated[int, Path(gt=0, description="Student ID must be greater than 0")]
):
    if student_id not in grades_db or len(grades_db[student_id]) == 0:
        raise HTTPException(status_code=404, detail="No grades found for this student.")

    scores = [g["score"] for g in grades_db[student_id]]
    average = round(sum(scores) / len(scores), 2)

    return {
        "student_id": student_id,
        "average": average
    }