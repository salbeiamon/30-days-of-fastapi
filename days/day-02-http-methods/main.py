from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI()

# pydantic models for request and response bodies


class UserCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: str = Field(min_length=1)
    age: int = Field(ge=0, le=150)
    salary: float = Field(gt=0)


class UserUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    email: str | None = Field(default=None, min_length=1)
    age: int | None = Field(default=None, ge=0, le=150)
    salary: float | None = Field(default=None, gt=0)


class User(UserCreate):
    id: int


users: dict[int, User] = {}
next_id = 1

# Get - retrieve


@app.get("/users", response_model=list[User])
def list_users():
    return list(users.values())


@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: int):
    if user_id not in users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return users[user_id]

# POST - create


@app.post("/users", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(data: UserCreate):
    global next_id
    user = User(id=next_id, **data.model_dump())
    users[next_id] = user
    next_id += 1
    return user

# PUT - replace existing


@app.put("/users/{user_id}", response_model=User)
def replace_user(user_id: int, data: UserCreate):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    users[user_id] = User(id=user_id, **data.model_dump())
    return users[user_id]

# --- PATCH: update only some fields ---


@app.patch("/users/{user_id}", response_model=User)
def update_user(user_id: int, data: UserUpdate):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    # only fields the client sent
    changes = data.model_dump(exclude_unset=True)
    users[user_id] = users[user_id].model_copy(update=changes)
    return users[user_id]

# Delete - Remove user


@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    del users[user_id]
