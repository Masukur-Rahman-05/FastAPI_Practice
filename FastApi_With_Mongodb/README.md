# FastAPI Notes API with MongoDB

A RESTful API for managing notes built with FastAPI and MongoDB using async operations.

## Project Structure

```
FastApi_With_Mongodb/
├── app/
│   ├── main.py        # FastAPI application and route handlers
│   ├── database.py    # MongoDB connection setup
│   └── models.py      # Pydantic models for data validation
├── requirements.txt   # Python dependencies
└── README.md          # Project documentation
```

## File Descriptions

### `app/main.py`
This is the entry point of the FastAPI application. It contains:
- **Startup/Shutdown events**: Connect and disconnect from MongoDB on app lifecycle
- **Route Handlers**:
  - `POST /create` - Create a new note with title, content, and optional tags
  - `GET /notes` - Retrieve all notes sorted by creation date (newest first)
  - `GET /get/{note_id}` - Fetch a single note by its MongoDB ObjectId
  - `PUT /update/{note_id}` - Update an existing note (partial updates supported)
  - `DELETE /delete/{note_id}` - Remove a note from the database
- **Helper function**: `helper_note()` converts MongoDB documents to JSON-serializable dict format

### `app/database.py`
Handles MongoDB database connections:
- `connect_db()`: Creates an AsyncIOMotorClient connection to MongoDB at `localhost:27017`
- `close_db()`: Closes the database connection on app shutdown
- `get_database()`: Returns the `my_database` database instance for use in routes

### `app/models.py`
Defines Pydantic models for request/response validation:
- `NoteCreate`: Schema for creating notes (title, content, tags)
- `NoteResponse`: Schema for API responses with id and created_at timestamp
- `NoteUpdate`: Schema for partial updates (all fields optional)

### `requirements.txt`
Lists Python dependencies:
- `fastapi` - Web framework
- `uvicorn[standard]` - ASGI server
- `motor` - Async MongoDB driver
- `pymongo` - MongoDB driver
- `pydantic` - Data validation
- `python-dotenv` - Environment variable handling

## Tech Stack

- **FastAPI** - Modern Python web framework
- **Motor** - Asynchronous MongoDB driver
- **Pydantic** - Data validation using Python type hints
- **Uvicorn** - Lightning-fast ASGI server

## Installation

```bash
pip install -r requirements.txt
```

## Running the Application

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, access interactive documentation:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/create` | Create a new note |
| GET | `/notes` | Get all notes |
| GET | `/get/{note_id}` | Get a note by ID |
| PUT | `/update/{note_id}` | Update a note |
| DELETE | `/delete/{note_id}` | Delete a note |

## Example Request Body

```json
{
  "title": "MongoDB with FastAPI",
  "content": "This codebase demonstrates integrating MongoDB with FastAPI",
  "tags": ["python", "mongodb", "fastapi"]
}
```
