# FastAPI Day One — Getting Started

A beginner-friendly practice project covering FastAPI installation, path parameters, query parameters, combining path and query parameters, request bodies, and the `PUT` and `DELETE` methods.

## Learning objectives

By completing this project, you should be able to:

1. Install FastAPI and run an application with Uvicorn.
2. Create API routes using decorators such as `@app.get()` and `@router.post()`.
3. Read values from path parameters and query parameters.
4. Receive and validate JSON request bodies with Pydantic models.
5. Update existing data with `PUT`.
6. Delete data with `DELETE`.
7. Test endpoints using the automatic interactive API documentation.

## 1. Requirements

- Python 3.10 or newer
- VS Code or another code editor
- A terminal / command prompt
- Basic Python knowledge

Check your Python installation:

```bash
python --version
```

On some systems, use `python3 --version`.

## 2. Create and activate a virtual environment

Open a terminal in your project folder:

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

On Windows Command Prompt:

```cmd
.venv\Scripts\activate.bat
```

On macOS or Linux:

```bash
source .venv/bin/activate
```

A virtual environment keeps this project's Python packages separate from other projects.

## 3. Install FastAPI

Install FastAPI with its standard dependencies, including the development server:

```bash
pip install "fastapi[standard]"
```

You can confirm the installation with:

```bash
pip show fastapi
```

## 4. Project structure

Keep these four Python files in the same folder:

```text
fastapi-day-one/
├── main.py
├── schemas.py
├── item_routes.py
├── task_routes.py
└── README.md
```

- `main.py` — creates the FastAPI application and registers the routers.
- `schemas.py` — defines Pydantic models used to validate request data.
- `item_routes.py` — demonstrates path parameters, query parameters, combined parameters, request bodies, PUT and DELETE.
- `task_routes.py` — gives you another small example of creating, listing and deleting resources.

## 5. Run the application

From the project folder, run:

```bash
fastapi dev main.py
```

If that command is unavailable, try:

```bash
python -m uvicorn main:app --reload
```

The API should be available at:

- Base URL: http://127.0.0.1:8000
- Interactive documentation: http://127.0.0.1:8000/docs
- Alternative documentation: http://127.0.0.1:8000/redoc

Keep the terminal running while you test the API. Press `Ctrl + C` to stop it.

## 6. Understand the concepts

### A. Path parameters

A path parameter is part of the URL path and usually identifies one resource.

Example:

```text
GET /items/1
```

In the code:

```python
@router.get("/{item_id}")
def get_item(item_id: int):
    return items.get(item_id)
```

Here, `item_id` is taken from the URL. FastAPI converts it to an integer because of the `int` type hint and validates the input.

Try `/items/1` and `/items/2` in the browser or `/docs`.

### B. Query parameters

Query parameters appear after `?` in a URL. They are useful for filtering, searching, sorting or pagination.

Example:

```text
GET /items/search?keyword=mouse&max_price=1000
```

In the code:

```python
@router.get("/search")
def search_items(keyword: str | None = None, max_price: float | None = None):
    ...
```

Both values are optional because they have defaults of `None`. Try changing the keyword and maximum price.

### C. Combining path and query parameters

You can use both in one endpoint.

Example:

```text
GET /items/1/offers?currency=USD
```

- `item_id` comes from the path.
- `currency` comes from the query string.

FastAPI identifies them from the route and function signature.

### D. Request body

A request body carries data sent to the API, commonly as JSON. In this project, `ItemCreate` and `TaskCreate` are Pydantic models.

Example JSON for `POST /items/`:

```json
{
  "name": "Laptop Stand",
  "price": 1200,
  "description": "Adjustable stand"
}
```

FastAPI validates the submitted data against the model. For example, the item name must have at least two characters and the price must be greater than zero.

### E. PUT method

`PUT` is used to update an existing resource. This project's `PUT /items/{item_id}` accepts the fields you provide and keeps other existing fields unchanged for easier beginner practice.

Example JSON for `PUT /items/1`:

```json
{
  "price": 1750
}
```

The example uses `exclude_unset=True` so fields omitted from the request are not overwritten. In a larger API, decide clearly whether you want full replacement (`PUT`) or partial modification (`PATCH`).

### F. DELETE method

`DELETE` removes a resource.

Example:

```text
DELETE /items/1
```

The API returns a confirmation message. If the ID does not exist, it returns HTTP `404 Not Found`.

## 7. Test the endpoints

Open `http://127.0.0.1:8000/docs`. Expand an endpoint, click **Try it out**, enter the parameters or JSON body, and click **Execute**.

| Method | Endpoint | What to try |
|---|---|---|
| GET | `/` | Welcome message |
| GET | `/health` | Check API status |
| GET | `/items/` | List items |
| GET | `/items/1` | Path parameter |
| GET | `/items/search?keyword=mouse` | Query parameter |
| GET | `/items/1/offers?currency=USD` | Path + query |
| POST | `/items/` | Create item with JSON |
| PUT | `/items/1` | Update an item |
| DELETE | `/items/1` | Delete an item |
| POST | `/tasks/` | Create a task |
| GET | `/tasks/` | List tasks |
| DELETE | `/tasks/1` | Delete a task |

For POST, use the JSON examples above. For PUT, try changing only one field.

## 8. Important learning notes

- `GET` reads data; `POST` creates data; `PUT` updates data; `DELETE` removes data.
- A path parameter is part of the route path; a query parameter follows `?`.
- Pydantic models validate request-body data.
- `HTTPException` lets you return useful HTTP errors such as `404`.
- The sample data is stored in Python dictionaries, not a database. It resets when the server restarts.
- This is a learning project, not production-ready authentication, payment or database code.

## 9. Practice challenges

Try these without copying the existing functions:

1. Add `GET /items/category/{category}` and return items in a chosen category. You will need to add a category field to the sample data.
2. Add a `min_price` query parameter to the search endpoint.
3. Add a `PUT /tasks/{task_id}` endpoint to mark a task as completed.
4. Return a `404` error when a requested item or task does not exist.
5. Add at least three more sample items and test your search filters.

## 10. Suggested learning sequence

1. Run the project and visit `/docs`.
2. Read `main.py` and understand how the routers are connected.
3. Read `schemas.py` and understand the Pydantic fields.
4. Test each endpoint before changing the code.
5. Complete the practice challenges.
6. Make a Git commit after the project works.

**Day One goal:** Do not just run the code. Be able to explain where each URL value comes from, how JSON reaches a Python function, and what each HTTP method does.
