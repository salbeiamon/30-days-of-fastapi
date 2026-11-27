
"""
DAY 3 - FASTAPI
Pydantic Models, Validation, Nested Models and Form Data

Install:
    pip install -r requirements.txt

Run:
    uvicorn main:app --reload

Documentation:
    http://127.0.0.1:8000/docs

Note:
    This project uses in-memory storage.
    Data resets when the server restarts.
"""

from typing import Optional

from fastapi import FastAPI, Form, HTTPException, status
from pydantic import BaseModel, EmailStr, Field


app = FastAPI(
    title="Day 3 - Student Registration API",
    description="Learning Pydantic Models and Form Data",
    version="1.0.0"
)


class Address(BaseModel):
    county: str = Field(min_length=2, max_length=50)
    town: str = Field(min_length=2, max_length=50)


class Guardian(BaseModel):
    name: str = Field(min_length=2, max_length=80)
    phone: str = Field(min_length=7, max_length=20)


class StudentBase(BaseModel):
    name: str = Field(
        min_length=2,
        max_length=50,
        description="Student's full name"
    )

    age: int = Field(
        ge=18,
        le=100,
        description="Student's age"
    )

    email: EmailStr

    phone: Optional[str] = Field(
        default=None,
        min_length=7,
        max_length=20
    )

    course: str = Field(
        min_length=3,
        max_length=80
    )

    gender: Optional[str] = None


class StudentCreate(StudentBase):
    address: Address
    guardian: Optional[Guardian] = None


class StudentUpdate(BaseModel):
    name: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=50
    )

    age: Optional[int] = Field(
        default=None,
        ge=18,
        le=100
    )

    email: Optional[EmailStr] = None

    phone: Optional[str] = Field(
        default=None,
        min_length=7,
        max_length=20
    )

    course: Optional[str] = Field(
        default=None,
        min_length=3,
        max_length=80
    )

    gender: Optional[str] = None
    address: Optional[Address] = None
    guardian: Optional[Guardian] = None


class StudentResponse(StudentBase):
    student_id: int
    address: Address
    guardian: Optional[Guardian] = None


students: dict[int, dict] = {}
next_student_id = 1


@app.get("/")
async def home():
    return {
        "message": "Welcome to Student Registration API",
        "documentation": "/docs",
        "version": "1.0.0"
    }


@app.get("/health")
async def health_check():
    return {
        "status": "running"
    }


@app.post(
    "/students",
    response_model=StudentResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_student(student: StudentCreate):

    global next_student_id

    # Convert Pydantic model into a dictionary
    student_data = student.model_dump()

    # Assign a unique ID
    student_data["student_id"] = next_student_id

    # Store student information
    students[next_student_id] = student_data

    next_student_id += 1

    return student_data


@app.get(
    "/students",
    response_model=list[StudentResponse]
)
async def get_all_students():

    return list(students.values())


@app.get(
    "/students/{student_id}",
    response_model=StudentResponse
)
async def get_student(student_id: int):

    student = students.get(student_id)

    if student is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )

    return student


@app.patch(
    "/students/{student_id}",
    response_model=StudentResponse
)
async def update_student(
    student_id: int,
    student_update: StudentUpdate
):

    existing_student = students.get(student_id)

    if existing_student is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )

    # Only include fields supplied by the client
    update_data = student_update.model_dump(
        exclude_unset=True
    )

    # Convert nested models into dictionaries
    if (
        "address" in update_data
        and student_update.address is not None
    ):
        update_data["address"] = (
            student_update.address.model_dump()
        )

    if (
        "guardian" in update_data
        and student_update.guardian is not None
    ):
        update_data["guardian"] = (
            student_update.guardian.model_dump()
        )

    # Update existing student information
    existing_student.update(update_data)

    return existing_student


@app.delete("/students/{student_id}")
async def delete_student(student_id: int):

    if student_id not in students:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )

    del students[student_id]

    return {
        "message": "Student deleted successfully",
        "student_id": student_id
    }


@app.post("/register-form")
async def register_student_form(
    name: str = Form(
        min_length=2,
        max_length=50
    ),

    age: int = Form(
        ge=18,
        le=100
    ),

    email: EmailStr = Form(),

    course: str = Form(
        min_length=3,
        max_length=80
    ),

    phone: Optional[str] = Form(default=None),

    gender: Optional[str] = Form(default=None)
):

    return {
        "message": "Student registered using Form Data",
        "student": {
            "name": name,
            "age": age,
            "email": str(email),
            "course": course,
            "phone": phone,
            "gender": gender
        }
    }


@app.get("/model-tools/demo")
async def model_tools_demo():

    example_student = StudentBase(
        name="Amon Kiprop",
        age=21,
        email="amon@example.com",
        course="Computer Science",
        phone="0712345678"
    )

    # Convert model into a dictionary
    dumped_data = example_student.model_dump()

    # Create a copy with an updated course
    copied_student = example_student.model_copy(
        update={
            "course": "Software Engineering"
        }
    )

    # Exclude age from the dictionary
    data_without_age = example_student.model_dump(
        exclude={"age"}
    )

    return {
        "original_model": example_student,
        "model_dump": dumped_data,
        "model_copy": copied_student,
        "excluding_age": data_without_age
    }


@app.get("/about")
async def about():

    return {
        "project": "Day 3 FastAPI",
        "topics": [
            "Pydantic BaseModel",
            "Field validation",
            "Required and optional fields",
            "EmailStr validation",
            "Nested models",
            "Model inheritance",
            "Request models",
            "Response models",
            "model_dump()",
            "model_copy()",
            "Form Data",
            "CRUD operations",
            "HTTPException"
        ]
    }
