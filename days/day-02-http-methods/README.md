# Day 2: Building a User Management API with FastAPI to learn more about HTTP Mothods and exception to handle errors

## 1. Introduction

The project demonstrates how to perform CRUD operations (Create, Read, Update, and Delete) on user records.

I also learned how to validate incoming data, handle errors, use HTTP status codes, and manage API responses.

### Technologies Used

- Python
- FastAPI
- Pydantic
- Uvicorn
- Visual Studio Code

---

## 2. Project Objectives

I learned how to:

1. Create a FastAPI application.
2. Define Pydantic models for data validation.
3. Create and retrieve user records.
4. Update existing records using PUT.
5. Partially update records using PATCH.
6. Delete records using DELETE.
7. Handle errors using `HTTPException`.
8. Use appropriate HTTP status codes.
9. Define response models using `response_model`.
10. Manage application data using a Python dictionary.

---

## 3. Installing Dependencies

First, install the required packages:

```bash
pip install fastapi uvicorn
```

To run the application:

```bash
uvicorn main:app --reload
```

Open the interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

---

## 4. Importing Required Modules

```python
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
```

### Explanation

- `FastAPI`: Creates the API application.
- `HTTPException`: Raises HTTP errors when something goes wrong.
- `status`: Provides readable HTTP status code constants.
- `BaseModel`: Creates Pydantic models.
- `Field`: Defines validation rules for model fields.

---

## 5. Creating the FastAPI Application

```python
app = FastAPI()
```

This creates an instance of the FastAPI application.

The `app` object is used to register API endpoints using decorators such as:

- `@app.get()`
- `@app.post()`
- `@app.put()`
- `@app.patch()`
- `@app.delete()`

---

## 6. Creating Pydantic Models

Pydantic models define the structure and validation rules for the data received by the API.

### 6.1 UserCreate Model

```python
class UserCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: str = Field(min_length=1)
    age: int = Field(ge=0, le=150)
    salary: float = Field(gt=0)
```

This model defines the information required when creating a new user.

**Validation rules:**

| Field | Validation |
|---|---|
| name | Minimum 1 and maximum 100 characters |
| email | Must not be empty |
| age | Must be between 0 and 150 |
| salary | Must be greater than 0 |

Pydantic automatically validates incoming request data against these rules.

### 6.2 UserUpdate Model

```python
class UserUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    email: str | None = Field(default=None, min_length=1)
    age: int | None = Field(default=None, ge=0, le=150)
    salary: float | None = Field(default=None, gt=0)
```

This model is used when performing partial updates with the PATCH method.

All fields are optional because the client may want to update only one or a few fields.

For example, a user can update their salary without changing their name, email, or age.

### 6.3 User Response Model

```python
class User(UserCreate):
    id: int
```

This model inherits all the fields from `UserCreate` and adds an `id`.

The ID uniquely identifies each user in the application.

---

## 7. Setting Up Temporary Data Storage

```python
users: dict[int, User] = {}
next_id = 1
```

### Explanation

- `users`: A Python dictionary that stores user records.
- `int`: Represents the dictionary key, which is the user ID.
- `User`: Represents the value stored for each user.
- `next_id`: Keeps track of the next available user ID.

Example:

```python
users = {
    1: {
        "id": 1,
        "name": "John",
        "email": "john@example.com",
        "age": 25,
        "salary": 35000
    }
}
```

**Important:** This application uses in-memory storage. The data disappears when the server restarts. A database will be introduced in a future learning stage.

---

## 8. GET Method – Retrieving Users

The GET method retrieves information from the API.

### 8.1 Retrieve All Users

```python
@app.get("/users", response_model=list[User])
def list_users():
    return list(users.values())
```

**Explanation:**

- `@app.get("/users")`: Defines the GET endpoint.
- `response_model=list[User]`: Specifies that the response should contain a list of users.
- `users.values()`: Retrieves all user records.
- `list()`: Converts the dictionary values into a list.

Endpoint:

```text
GET /users
```

### 8.2 Retrieve a Single User

```python
@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: int):
    if user_id not in users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return users[user_id]
```

**Explanation:**

- `{user_id}` is a path parameter.
- `user_id: int` ensures the parameter is an integer.
- The `if` statement checks whether the requested user exists.
- `HTTPException` returns an error if the user does not exist.
- `404 NOT FOUND` indicates that the requested resource could not be found.

Endpoint:

```text
GET /users/1
```

---

## 9. POST Method – Creating a User

The POST method creates a new user record.

```python
@app.post(
    "/users",
    response_model=User,
    status_code=status.HTTP_201_CREATED
)
def create_user(data: UserCreate):
    global next_id

    user = User(id=next_id, **data.model_dump())
    users[next_id] = user
    next_id += 1

    return user
```

### Explanation

1. `@app.post("/users")` defines the POST endpoint.
2. `data: UserCreate` receives and validates the request body.
3. `global next_id` allows the function to modify the global ID counter.
4. `data.model_dump()` converts the Pydantic model into a Python dictionary.
5. `**` unpacks the dictionary into the `User` model.
6. The new user is stored in the dictionary.
7. `next_id += 1` prepares the next ID.
8. The created user is returned.

The status code `201 CREATED` indicates successful resource creation.

Example JSON request:

```json
{
    "name": "John",
    "email": "john@example.com",
    "age": 25,
    "salary": 35000
}
```

Endpoint:

```text
POST /users
```

---

## 10. PUT Method – Replacing an Existing User

PUT replaces the existing user information with new information.

```python
@app.put("/users/{user_id}", response_model=User)
def replace_user(user_id: int, data: UserCreate):
    if user_id not in users:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    users[user_id] = User(id=user_id, **data.model_dump())

    return users[user_id]
```

### Explanation

- The user ID is received through a path parameter.
- The API checks whether the user exists.
- If the user does not exist, a `404 NOT FOUND` error is raised.
- If the user exists, all editable user information is replaced.
- The updated user is returned.

Example:

```text
PUT /users/1
```

Request body:

```json
{
    "name": "John Updated",
    "email": "johnupdated@example.com",
    "age": 27,
    "salary": 45000
}
```

**Important:** PUT requires the complete set of fields defined by `UserCreate` in this application.

---

## 11. PATCH Method – Updating Selected Fields

PATCH updates only the fields supplied by the client.

```python
@app.patch("/users/{user_id}", response_model=User)
def update_user(user_id: int, data: UserUpdate):
    if user_id not in users:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    changes = data.model_dump(exclude_unset=True)

    users[user_id] = users[user_id].model_copy(update=changes)

    return users[user_id]
```

### Explanation

**1. Check whether the user exists**

```python
if user_id not in users:
    raise HTTPException(status_code=404, detail="User not found")
```

**2. Extract only the supplied fields**

```python
changes = data.model_dump(exclude_unset=True)
```

`exclude_unset=True` ensures that fields the client did not provide are excluded from the update.

**3. Update the existing model**

```python
users[user_id] = users[user_id].model_copy(update=changes)
```

`model_copy(update=changes)` creates an updated copy of the existing Pydantic model.

### Example

```text
PATCH /users/1
```

Request body:

```json
{
    "salary": 50000
}
```

Only the salary changes. The other user details remain unchanged.

**PUT vs PATCH**

| PUT | PATCH |
|---|---|
| Replaces all editable fields | Updates selected fields |
| Requires complete request data here | Allows partial request data |
| Uses `UserCreate` | Uses `UserUpdate` |

---

## 12. DELETE Method – Removing a User

DELETE removes an existing user from the application.

```python
@app.delete(
    "/users/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_user(user_id: int):
    if user_id not in users:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    del users[user_id]
```

### Explanation

- The user ID identifies the record to delete.
- The API checks whether the user exists.
- If the user does not exist, a `404 NOT FOUND` error is raised.
- `del users[user_id]` removes the user from the dictionary.
- `204 NO CONTENT` indicates successful deletion without a response body.

Endpoint:

```text
DELETE /users/1
```

---

## 13. HTTP Status Codes Used

| Status Code | Meaning | Application |
|---|---|---|
| 200 | OK | Successful GET, PUT and PATCH |
| 201 | Created | Successful POST |
| 204 | No Content | Successful DELETE |
| 404 | Not Found | User does not exist |
| 422 | Unprocessable Entity | Invalid request data |

FastAPI automatically handles request validation errors and returns `422` when incoming data fails validation.

---

## 14. Understanding HTTPException

`HTTPException` allows an API to return meaningful errors.

Example:

```python
raise HTTPException(
    status_code=404,
    detail="User not found"
)
```

Instead of returning an ordinary dictionary that looks like a successful response, raising `HTTPException` tells FastAPI that the request has failed.

---

## 15. Testing the API

After starting the server, visit:

```text
http://127.0.0.1:8000/docs
```

Use Swagger UI to test the following endpoints:

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/users` | Retrieve all users |
| GET | `/users/{user_id}` | Retrieve one user |
| POST | `/users` | Create a user |
| PUT | `/users/{user_id}` | Replace a user |
| PATCH | `/users/{user_id}` | Partially update a user |
| DELETE | `/users/{user_id}` | Delete a user |

### Recommended Testing Order

1. Create a user using POST.
2. Retrieve all users using GET.
3. Retrieve the created user using its ID.
4. Replace the user using PUT.
5. Update one field using PATCH.
6. Delete the user using DELETE.
7. Try retrieving the deleted user to test the 404 error.

---

## 16. Key Lessons Learned

Through this project, I gained practical experience with:

- FastAPI application setup.
- Pydantic models and field validation.
- Request and response models.
- Path parameters.
- CRUD operations.
- HTTP methods and status codes.
- Error handling with `HTTPException`.
- Python dictionaries for temporary data storage.
- Pydantic methods such as `model_dump()` and `model_copy()`.
- The difference between PUT and PATCH.

---

## 17. Areas for Improvement

This project is a learning exercise. Future improvements include:

1. Connecting the application to a database such as PostgreSQL or SQLite.
2. Adding proper email validation using Pydantic's `EmailStr`.
3. Preventing duplicate email addresses.
4. Adding user authentication and authorization.
5. Adding automated tests using Pytest.
6. Organizing the application into separate modules.
7. Adding pagination and search functionality.

---

## 18. Conclusion

I can now create, retrieve, replace, partially update, and delete user records while validating incoming data and handling errors.

This project provides a foundation for building more advanced backend applications that use databases, authentication, and external APIs.


## Author
Amon Kiprop
akiprop.sw@gmail.com
---

