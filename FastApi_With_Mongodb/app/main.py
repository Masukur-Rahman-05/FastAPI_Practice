
from fastapi import FastAPI,HttpException,status
from fastapi.responses import JSONResponse
from bson import ObjectId
from datetime import datetime

from .database import connect_db,close_db,get_database
from .models import NoteCreate,NoteResponse,NoteUpdate


app = FastAPI()

@app.on_event("startup")
async def startup():
    await connect_db()

@app.on_event("shutdown")
async def shutdown():
    await close_db()


def helper_note(note) -> dict:
    return{
        "id":str(note["_id"]),
        "title":note["title"],
        "content":note["content"],
        "tags": note.get("tags",[]),
        "created_at": note["created_at"]
    }


@app.post("/create", response_model=NoteResponse, status_code=status.HTTP_201_CREATED)
async def create_note(note:NoteCreate):
    db = get_database()
    collection = db.notes

    note_dict = note.model_dump()
    note_dict["created_at"] = datetime.utcnow()

    result = await collection.insert_one(note_dict)

    created_note = await collection.find_one({"_id":result.inserted_id})
    return helper_note(created_note)
