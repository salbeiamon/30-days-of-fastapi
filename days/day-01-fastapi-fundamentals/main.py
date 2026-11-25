from fastapi import FastAPI
from pydantic import BaseModel, EmailStr, Field
app = FastAPI()

# Put request body - updates existing data


class Create_User(BaseModel):
    name: str = Field(description="Enter your name",
                      min_length=2, max_length=50)
    email: EmailStr = Field(description="example@example.com")
    age: int = Field(description="Enter your age", ge=18, le=100)
    course: str | None = Field(None, description="Enter your course")

# Response model - used to define the structure of response body


class Create_UserResponse(BaseModel):
    name: str
    course: str | None = Field(None, description="The user's course")


@app.post("/create_user", response_model=Create_UserResponse)
def create_user(user: Create_User):
    return {
        "message": "User created successfully",
        "name": user.name,
        "email": user.email,
        "age": user.age,
        "course": user.course
    }
