from fastapi import FastAPI
from pydantic import BaseModel, EmailStr, Field

# BaseModel - Defines the structure and validation rules of incoming data
# Field - Used to define additional metadata and validation rules for individual fields in the model, controls data entering your system


class Create_User(BaseModel):
    name: str = Field(..., description="The user's name",
                      min_length=2, max_length=50)
    email: EmailStr = Field(..., description="The user's email address", )
    age: int = Field(..., description="The user's age")
    password: str = Field(..., description="The user's password",
                          ge=6, max_length=20)
    course: str | None = Field(None, description="The user's course")

# Request body with PUT - upates existing data


class Create_UserResponse(BaseModel):
    name: str
    course: str | None = Field(None, description="The user's course")


class Update_User(BaseModel):
    name: str | None = Field(
        None, description="The user's name", min_length=2, max_length=50)
    email: EmailStr | None = Field(
        None, description="The user's email address")
    age: int | None = Field(None, description="The user's age")

# patch request body - updates existing data partially


class Patch_User(BaseModel):
    name: str | None = Field(
        None, description="The user's name", min_length=2, max_length=50)
    email: EmailStr | None = Field(
        None, description="The user's email address")
    age: int | None = Field(None, description="The user's age")


app = FastAPI()

# path parameter - Identifies a specific resource


@app.get("/item/{item_id}")
def get_item(item_id: int):
    return {"item ID": item_id}

# query parameter - Used to filter or sort resources


@app.get("/music")
def get_music(genre: str = None, artist: str = None):
    return {"genre": genre, "artist": artist}

# combining both query and path parameters


@app.get("/stream/{stream_id}/song_type")
def get_item_music(stream_id: int, song_type: str, lyricist: str = None):
    return {"stream ID": stream_id, "song type": song_type, "lyricist": lyricist}

# Request Body - Used to send data to the server by the client in the body of the request
# we use Pydantic models to define the structure of the request body
# we use the BaseModel class from Pydantic to create a model for the request body
# we use Post method to send data to the server
# we use the Body class from FastAPI to define the request body
# Request Body sends structured data to the server unlike the path and query parameters which send unstructured data to the server

# Response Model - used to define the structure of response body


@app.post("/create_user", response_model=Create_UserResponse)
def create_user(user: Create_User):
    return {
        "message": "User created successfully",
        "name": user.name,
        "email": user.email,
        "age": user.age,
        "password": user.password,
        "course": user.course
    }


@app.put("/update_user/{user_id}")
def update_user(user_id: int, user: Update_User):
    return {
        "message": "User updated successfully",
        "user ID": user_id,
        "name": user.name,
        "email": user.email,
        "age": user.age
    }


@app.patch("/patch_user/{user_id}")
def patch_user(user_id: int, user: Patch_User):
    return {
        "message": "User patched successfully",
        "user ID": user_id,
        "name": user.name,
        "email": user.email,
        "age": user.age
    }

# nested request body - Used to send nested data to the server by the client in the body of the request
# response body - Used to send data from the server to the client in the body of the response
# response model - Used to define the structure of the response body


class Admin(BaseModel):
    name: str = Field(description="Administator's name",
                      min_length=2, max_length=50)
    email: EmailStr = Field(description="Admins email address")


class Create_Admin(BaseModel):
    admin: Admin = Field(description="Administator's details")
    password: str = Field(
        description="Enter your password", ge=8, max_length=20)


@app.post("/create_admin")
def create_admin(new_admin: Create_Admin):
    return {
        "message": "Admin created successfully",
        "admin name": new_admin.admin.name,
        "admin email": new_admin.admin.email,
        "password": new_admin.password
    }
