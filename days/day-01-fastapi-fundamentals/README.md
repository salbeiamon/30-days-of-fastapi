# Day 1: Introduction to FastAPI, API Fundamentals & Data Validation

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pydantic](https://img.shields.io/badge/Pydantic-E92063?style=for-the-badge)

## 1. Introduction to FastAPI

FastAPI is a modern Python web framework used to build APIs quickly and efficiently.

It allows developers to create RESTful APIs, handle HTTP requests, validate incoming data and return structured responses.

### Why FastAPI?

- High performance.
- Automatic API documentation.
- Built-in request validation.
- Easy integration with Pydantic.
- Supports asynchronous programming.
- Simple and readable syntax.

## 2. Installation and Setup

### Requirements

- Python 3.10 or later.
- Visual Studio Code.
- Python extension.
- Basic Python knowledge.

### Create a project folder

```bash
mkdir day-01-fastapi-fundamentals
cd day-01-fastapi-fundamentals
```

### Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### Install FastAPI

```bash
pip install "fastapi[standard]"
```

### Run the application

```bash
fastapi dev main.py
```

Open the interactive documentation:

http://127.0.0.1:8000/docs

## 3. Creating Your First FastAPI Application

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Welcome to FastAPI"}
```

### Explanation

- `FastAPI()` creates the application.
- `@app.get("/")` defines a GET endpoint.
- `def home()` defines the function executed when the endpoint is accessed.
- `return` sends a JSON response.

## 4. Understanding API Endpoints

An endpoint is a URL through which a client communicates with an API.

Examples:

| HTTP Method | Purpose |
|---|---|
| GET | Retrieve information |
| POST | Create new information |
| PUT | Replace or update existing information |
| PATCH | Partially update information |
| DELETE | Remove information |

## 5. Path Parameters

Path parameters are values passed directly through the URL.

Example:

```python
@app.get("/items/{item_id}")
def get_item(item_id: int):
    return {
        "item_id": item_id,
        "message": "Item retrieved successfully"
    }
```

Example URL:

```text
http://127.0.0.1:8000/items/10
```

The value `10` is passed into the `item_id` parameter.

### Important points

- Path parameters are part of the URL.
- They are useful when identifying a particular resource.
- Python type hints help FastAPI validate their values.

## 6. Query Parameters

Query parameters are additional values passed after a question mark (`?`) in a URL.

Example:

```python
@app.get("/items/")
def search_items(keyword: str, limit: int = 10):
    return {
        "keyword": keyword,
        "limit": limit
    }
```

Example URL:

```text
http://127.0.0.1:8000/items/?keyword=mouse&limit=5
```

### Important points

- Query parameters are separated using `&`.
- They are useful for searching, filtering and pagination.
- They can have default values.

## 7. Combining Path and Query Parameters

FastAPI allows developers to combine both parameters in one endpoint.

Example:

```python
@app.get("/items/{item_id}/offers")
def get_offers(item_id: int, currency: str = "USD"):
    return {
        "item_id": item_id,
        "currency": currency
    }
```

Example URL:

```text
http://127.0.0.1:8000/items/5/offers?currency=KES
```

Here:

- `item_id` is a path parameter.
- `currency` is a query parameter.

## 8. Request Bodies Using Pydantic

A request body contains information sent by a client to an API.

FastAPI commonly uses Pydantic models to define and validate incoming JSON data.

First, import BaseModel:

```python
from pydantic import BaseModel
```

Create a model:

```python
class Item(BaseModel):
    name: str
    price: float
    quantity: int
```

Use the model in a POST endpoint:

```python
@app.post("/items/")
def create_item(item: Item):
    return {
        "message": "Item created successfully",
        "item": item
    }
```

Example JSON request:

```json
{
    "name": "Laptop",
    "price": 45000,
    "quantity": 2
}
```

Pydantic checks whether the submitted information matches the expected structure and types.

## 9. HTTP Methods: POST, PUT and DELETE

### POST Method

POST is used to create new resources.

```python
@app.post("/items/")
def create_item(item: Item):
    return {
        "message": "Item created successfully",
        "item": item
    }
```

### PUT Method

PUT is commonly used to replace an existing resource with updated information.

```python
@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {
        "message": "Item updated successfully",
        "item_id": item_id,
        "updated_item": item
    }
```

### DELETE Method

DELETE is used to remove an existing resource.

```python
@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    return {
        "message": "Item deleted successfully",
        "item_id": item_id
    }
```

Note: These examples demonstrate endpoint behaviour. Actual data persistence requires a database or another storage mechanism.

## 10. Advanced Pydantic Models and Data Validation

Pydantic helps ensure that data submitted to an API follows specific rules.

### BaseModel

`BaseModel` is the foundation for creating data models.

Example:

```python
from pydantic import BaseModel

class User(BaseModel):
    name: str
    age: int
```

The model expects a name and an integer age.

### Field()

`Field()` allows developers to define additional validation rules and descriptions.

Example:

```python
from pydantic import BaseModel, Field

class User(BaseModel):
    name: str = Field(
        description="Enter your name",
        min_length=2,
        max_length=50
    )

    age: int = Field(
        description="Enter your age",
        ge=18,
        le=100
    )
```

Common Field validation arguments:

| Argument | Meaning |
|---|---|
| min_length | Minimum number of characters |
| max_length | Maximum number of characters |
| ge | Greater than or equal to |
| le | Less than or equal to |
| gt | Greater than |
| lt | Less than |
| description | Explains the field |

### EmailStr

`EmailStr` validates email address formats.

```python
from pydantic import EmailStr

class User(BaseModel):
    email: EmailStr
```

Install the required dependency:

```bash
pip install "pydantic[email]"
```

### Optional Fields

An optional field allows a user to submit data without providing that particular value.

Example:

```python
course: str | None = None
```

This means the course can contain a string or `None`.

Using Field():

```python
course: str | None = Field(
    None,
    description="Enter your course"
)
```

## 11. Response Models

A response model defines the structure of data that an API sends back to the client.

It is created using Pydantic's `BaseModel`.

Example:

```python
class UserResponse(BaseModel):
    name: str
    course: str | None = None
```

To use it, specify `response_model` in your endpoint:

```python
@app.post("/create_user", response_model=UserResponse)
def create_user(user: User):
    return {
        "message": "User created successfully",
        "name": user.name,
        "email": user.email,
        "age": user.age,
        "course": user.course
    }
```

### Understanding Response Filtering

Suppose your function returns:

```python
{
    "message": "User created successfully",
    "name": "Amon",
    "email": "amon@example.com",
    "age": 22,
    "course": "Computer Science"
}
```

But your response model contains only:

```python
class UserResponse(BaseModel):
    name: str
    course: str | None = None
```

The actual API response becomes:

```json
{
    "name": "Amon",
    "course": "Computer Science"
}
```

FastAPI filters out fields that are not defined in the response model.

This is useful when controlling which information is exposed to API clients.

## 12. Complete Practical Project: User Registration API

This project combines the concepts learned throughout the lesson.

```python
from fastapi import FastAPI
from pydantic import BaseModel, EmailStr, Field

app = FastAPI()


# Request model
class Create_User(BaseModel):
    name: str = Field(
        description="Enter your name",
        min_length=2,
        max_length=50
    )

    email: EmailStr

    age: int = Field(
        description="Enter your age",
        ge=18,
        le=100
    )

    course: str | None = Field(
        None,
        description="Enter your course"
    )


# Response model
class Create_UserResponse(BaseModel):
    name: str
    course: str | None = None


# POST endpoint
@app.post("/create_user", response_model=Create_UserResponse)
def create_user(user: Create_User):

    return {
        "message": "User created successfully",
        "name": user.name,
        "email": user.email,
        "age": user.age,
        "course": user.course
    }
```

### Example Request

```json
{
    "name": "Amon Kiprop",
    "email": "amon@example.com",
    "age": 22,
    "course": "Computer Science"
}
```

### Expected Response

```json
{
    "name": "Amon Kiprop",
    "course": "Computer Science"
}
```

### What this project demonstrates

1. Creating a FastAPI application.
2. Defining request models.
3. Validating names and ages.
4. Validating email addresses.
5. Creating optional fields.
6. Defining response models.
7. Filtering API responses.

## 13. Testing Your API

FastAPI automatically generates interactive documentation.

Start the server:

```bash
fastapi dev main.py
```

Visit:

http://127.0.0.1:8000/docs

You can use Swagger UI to:

- View available endpoints.
- Submit JSON request bodies.
- Test path and query parameters.
- Test POST, PUT and DELETE methods.
- Inspect API responses.
- Observe validation errors.

## 14. Practical Exercises

Try completing these exercises without copying the examples.

**Exercise 1: Product API**

Create a product model containing:
- Product name.
- Price.
- Quantity.
- Category.

**Exercise 2: User Registration**

Create a registration endpoint with:
- Username.
- Email.
- Age.
- Course.
- Phone number.

Apply appropriate validation rules.

**Exercise 3: Response Models**

Create a response model that returns only:
- Username.
- Email.
- Course.

**Exercise 4: Update API**

Create a PUT endpoint that accepts an existing user's ID and updated information.

**Exercise 5: Delete API**

Create a DELETE endpoint that accepts a user ID and returns a success message.

## 15. Key Lessons Learned

By completing this lesson, I have learned:

- What FastAPI is and why it is useful.
- How to install and configure FastAPI.
- How to create API endpoints.
- How to use path parameters.
- How to use query parameters.
- How to combine path and query parameters.
- How to receive JSON request bodies.
- How to use POST, PUT and DELETE.
- How to create Pydantic models.
- How to validate data using Field().
- How to validate email addresses using EmailStr.
- How to define required and optional fields.
- How to create response models.
- How FastAPI filters response data.
- How to test APIs using Swagger UI.

## 16. Completion Checklist

- [x] FastAPI installation and setup.
- [x] First FastAPI application.
- [x] Path parameters.
- [x] Query parameters.
- [x] Combining path and query parameters.
- [x] Request bodies.
- [x] POST method.
- [x] PUT method.
- [x] DELETE method.
- [x] Pydantic BaseModel.
- [x] Field validation.
- [x] EmailStr.
- [x] Optional fields.
- [x] Response models.
- [x] Response filtering.
- [x] Swagger UI testing.

---

**Day 1 Completed!**

*Learning FastAPI one concept and one practical project at a time.*

**Next Learning Goal:** Continue exploring request handling, data validation, database integration and building functional REST APIs.
