# FastAPI Practice Project

> A lightweight FastAPI application demonstrating core features including request validation, Pydantic models, forms, file uploads, and SQLAlchemy ORM with SQLite.

## Tech Stack

| Component       | Library                          |
|----------------|----------------------------------|
| Framework       | FastAPI                          |
| Server          | Uvicorn                          |
| ORM             | SQLAlchemy 2.0                   |
| Validation      | Pydantic                         |
| Database        | SQLite (`test.db`)               |

## Quick Start

```bash
# Create virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate    # Linux/macOS

# Install dependencies
pip install -r requirements.txt

# Run the server
uvicorn app.main:app --reload --port 8000 --host 0.0.0.0
```

**API Documentation**
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## Project Structure

```
.
├── app/
│   ├── main.py       # FastAPI instance & all route handlers
│   ├── schemas.py    # Pydantic models (request/response)
│   ├── database.py   # SQLAlchemy engine & session setup
│   └── model.py      # ORM model definitions (User)
└── requirements.txt  # Project dependencies
```

## Endpoints

### General

| Method | Path                    | Description                        |
|--------|-------------------------|------------------------------------|
| GET    | `/`                     | Hello message                      |
| GET    | `/products/{product_id}`| Echo `product_id`                  |
| GET    | `/product_status/{status}` | Enum status (pending/shipped/etc) |
| GET    | `/users`                | Pagination (`skip`, `limit`)       |

### Request Body & Validation

| Method | Path                        | Description                          |
|--------|-----------------------------|--------------------------------------|
| POST   | `/api/v1/json`              | JSON body (`UserData`)               |
| POST   | `/api/v1/form`              | Form data (`name`, `age`, `hobby`)   |
| POST   | `/api/v1/upload`            | File upload (returns filename, type) |
| POST   | `/api/v1/product1`          | Nested body with set-based `tags`    |
| POST   | `/api/v1/user1`             | Model with optional nested object   |
| POST   | `/api/v1/user2`             | Model with nested list              |
| POST   | `/items/`                   | Create item (price + tax calculation)|
| PUT    | `/items/{item_id}`          | Update item (path + body)           |
| PUT    | `/items/{id}`               | Update item (path + body + query)   |
| POST   | `/api/v1/multiple_body`     | Multiple body models with `Body()`   |

### Query & Path Validation

| Method | Path                          | Description                            |
|--------|-------------------------------|----------------------------------------|
| GET    | `/api/v1/query`               | Query param with `ge`/`le` constraints|
| GET    | `/api/v1/path/{path_id}`      | Path param with annotation             |
| GET    | `/api/v1/query_model`         | Query params via Pydantic model        |

### Database CRUD

| Method | Path                       | Description           |
|--------|----------------------------|-----------------------|
| POST   | `/api/v2/signup`           | Create user           |
| GET    | `/api/v2/get`              | List all users        |
| PUT    | `/api/v2/update/{user_id}` | Update user           |
| DELETE | `/api/v2/delete/{user_id}` | Delete user           |

## Database

- **File**: `test.db` (SQLite, created automatically in project root)
- **Tables**: `users` (defined in `app/model.py`)
- Tables are created at startup via `Base.metadata.create_all(bind=engine)`

## Suggested Next Steps

- Add `pytest` tests using `TestClient`
- Integrate Alembic for migration management
- Move config to `.env` and add a `.gitignore`
- Improve error handling and validation coverage
