# Day 3 - FastAPI: Pydantic Models, Validation and Form Data

## Project Overview

Welcome to Day 3 of my 30 Days of FastAPI learning challenge.

Today, I explored Pydantic models, data validation, nested models, model inheritance, request and response models, and Form Data.

I also developed a practical Student Registration API to demonstrate how these concepts work together in a real backend application.

## Learning Objectives

By completing this project, I learned how to:

1. Understand Pydantic and `BaseModel`.
2. Create and validate Pydantic models.
3. Use `Field()` to define validation rules.
4. Work with required and optional fields.
5. Create nested Pydantic models.
6. Implement model inheritance.
7. Separate request models from response models.
8. Convert models into dictionaries using `model_dump()`.
9. Copy and update models using `model_copy()`.
10. Receive Form Data using `Form()`.
11. Handle errors using `HTTPException`.
12. Implement CRUD operations in FastAPI.

## Technologies Used

- Python
- FastAPI
- Pydantic
- Uvicorn
- Email Validator
- Python Multipart
- Swagger UI

## Project Structure

```text
Day-03-FastAPI-Pydantic-Forms/
│
├── main.py
├── README.md
├── requirements.txt
└── .gitignore
```

## Installation

### 1. Clone the repository

```bash
git clone YOUR_REPOSITORY_URL
```

### 2. Navigate into the project folder

```bash
cd Day-03-FastAPI-Pydantic-Forms
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Start the FastAPI server

```bash
uvicorn main:app --reload
```

### 6. Open Swagger documentation

```text
http://127.0.0.1:8000/docs
```

## Pydantic Models

Pydantic is used to validate and structure incoming data.

The project implements:

- `StudentBase`: Contains common student information.
- `StudentCreate`: Defines the information required to register a student.
- `StudentUpdate`: Defines optional fields for updating a student.
- `StudentResponse`: Defines the structure of API responses.
- `Address`: Demonstrates nested models.
- `Guardian`: Demonstrates another nested model.

## Data Validation

The project uses `Field()` to enforce validation rules.

Examples:

```python
name: str = Field(min_length=2, max_length=50)

age: int = Field(ge=18, le=100)
```

It also uses `EmailStr` to validate email addresses.

Optional fields are implemented using:

```python
phone: str | None = None
```

## Model Inheritance

The `StudentCreate` and `StudentResponse` models inherit common fields from `StudentBase`.

This reduces code repetition and makes the application easier to maintain.

## Model Operations

### model_dump()

Converts a Pydantic model into a Python dictionary.

```python
student_data = student.model_dump()
```

### model_copy()

Creates a copy of an existing model.

```python
new_student = student.model_copy(
    update={"course": "Software Engineering"}
)
```

Note: Updates passed to `model_copy()` are not validated automatically.

## Form Data

The project implements a Form Data endpoint using FastAPI's `Form()`.

Example:

```python
@app.post("/register-form")
async def register_student(
    name: str = Form(),
    age: int = Form()
):
    return {
        "name": name,
        "age": age
    }
```

The required `python-multipart` package enables form parsing.

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Welcome message |
| GET | `/health` | Check API status |
| POST | `/students` | Register a student |
| GET | `/students` | Retrieve all students |
| GET | `/students/{student_id}` | Retrieve one student |
| PATCH | `/students/{student_id}` | Update student information |
| DELETE | `/students/{student_id}` | Delete a student |
| POST | `/register-form` | Register using Form Data |
| GET | `/model-tools/demo` | Demonstrate model operations |
| GET | `/about` | Display project information |

## Example JSON Request

POST `/students`

```json
{
    "name": "Amon Kiprop",
    "age": 21,
    "email": "amon@example.com",
    "phone": "0712345678",
    "course": "Computer Science",
    "gender": "Male",
    "address": {
        "county": "Nairobi",
        "town": "Westlands"
    },
    "guardian": {
        "name": "John Kiprop",
        "phone": "0712345678"
    }
}
```

## Testing

The API can be tested using Swagger UI.

Recommended testing:

1. Register multiple students.
2. Retrieve all registered students.
3. Retrieve a student using their ID.
4. Update student information.
5. Delete a student.
6. Submit invalid student data.
7. Test optional fields.
8. Test nested models.
9. Submit information using Form Data.
10. Explore the model tools demonstration.

## Important Note

This project currently uses Python dictionaries as in-memory storage.

Student records are lost when the server restarts.

A database will be introduced in a later stage of the learning challenge.

## What I Learned

Day 3 strengthened my understanding of data validation and structured API development.

I learned that Pydantic models help ensure that incoming data follows predefined rules, while request and response models help control how data enters and leaves an API.

I also learned how FastAPI handles Form Data and how nested models and inheritance make backend applications more organized.

## Next Step

**Day 4: Form Data, Form Models and File Uploads.**

---

*30 Days of FastAPI - Learning by Building, Practicing and Improving.*
