from fastapi import FastAPI, HTTPException, status
import os
from dotenv import load_dotenv
from bson import ObjectId
from datetime import datetime, timezone

from .database import connect_db, close_db, get_database
from .models import NoteCreate, NoteResponse, NoteUpdate

load_dotenv()

app = FastAPI(
    title=os.getenv("APP_NAME", "FastAPI Lab 3"),
    description="Async MongoDB Integration with FastAPI",
    version="1.0.0"
)

# -------------------- EVENTS --------------------

@app.on_event("startup")
async def connect():
    await connect_db()

@app.on_event("shutdown")
async def close():
    await close_db()


# -------------------- HELPER --------------------

def helper(note) -> dict:
    return {
        "id": str(note["_id"]),
        "title": note["title"],
        "content": note["content"],
        "tags": note.get("tags", []),
        "created_at": note["created_at"]
    }


# -------------------- CREATE --------------------

@app.post("/create", response_model=NoteResponse, status_code=status.HTTP_201_CREATED)
async def create_note(payload: NoteCreate):
    db = await get_database()
    collection = db["notes"]

    note = payload.model_dump()
    note["created_at"] = datetime.now(timezone.utc)

    result = await collection.insert_one(note)

    created_note = await collection.find_one({"_id": result.inserted_id})

    return helper(created_note)


# -------------------- READ ALL --------------------

@app.get("/notes", response_model=list[NoteResponse])
async def get_all():
    db = await get_database()
    collection = db["notes"]

    notes = await collection.find({}).sort("created_at", -1).to_list(length=100)

    return [helper(note) for note in notes]


# -------------------- READ ONE --------------------

@app.get("/notes/{note_id}", response_model=NoteResponse)
async def get_note(note_id: str):

    if not ObjectId.is_valid(note_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid id format"
        )

    db = await get_database()
    collection = db["notes"]

    note = await collection.find_one({"_id": ObjectId(note_id)})

    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found"
        )

    return helper(note)


# -------------------- UPDATE --------------------

@app.put("/update/{note_id}", response_model=NoteResponse)
async def update_note(note_id: str, payload: NoteUpdate):

    if not ObjectId.is_valid(note_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid id format"
        )

    data = payload.model_dump(exclude_unset=True)

    if not data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Nothing to update"
        )

    db = await get_database()
    collection = db["notes"]

    result = await collection.update_one(
        {"_id": ObjectId(note_id)},
        {"$set": data}
    )

    if result.matched_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Note with id {note_id} not found"
        )

    updated_note = await collection.find_one({"_id": ObjectId(note_id)})

    return helper(updated_note)


# -------------------- DELETE ONE --------------------

@app.delete("/notes/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_note(note_id: str):

    if not ObjectId.is_valid(note_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid note ID format"
        )

    db = await get_database()
    collection = db["notes"]

    result = await collection.delete_one({"_id": ObjectId(note_id)})

    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Note with id {note_id} not found"
        )

    return None


# -------------------- DELETE MANY (NEW) --------------------

@app.delete("/notes", status_code=status.HTTP_200_OK)
async def delete_many_notes(delete_bad_only: bool = True):
    """
    Delete multiple notes.

    Query param:
    - delete_bad_only=true  → deletes only bad data (string dates)
    - delete_bad_only=false → deletes ALL notes
    """

    db = await get_database()
    collection = db["notes"]

    if delete_bad_only:
        result = await collection.delete_many({
            "created_at": {"$type": "string"}
        })
        return {
            "message": "Deleted notes with invalid datetime format",
            "deleted_count": result.deleted_count
        }

    else:
        result = await collection.delete_many({})
        return {
            "message": "Deleted ALL notes",
            "deleted_count": result.deleted_count
        }