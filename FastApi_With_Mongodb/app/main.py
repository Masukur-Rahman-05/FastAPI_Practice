
from fastapi import FastAPI,HTTPException,status
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


@app.get("/notes",response_model=list[NoteResponse])
async def get_all_notes():
    db = get_database()
    collection = db.notes

    notes = await collection.find({}).sort("created_at",-1).to_list(length=100)
    return [helper_note(note) for note in notes]


@app.put("/update/{note_id}",response_model=NoteResponse)
async def update_note(note_id:str,note:NoteUpdate):

    if not ObjectId.is_valid(note_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid ID Formate"
        )
    
    db = get_database()
    collection = db.notes

    update_data = note.model_dump(exclude_unset=True)

    if not update_data:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "No data has to be updated"
        )
    
    result = await collection.update_one(
        {"_id":ObjectId(note_id)},
        {"$set":update_data}
    )

    if result.matched_count == 0:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Note not found"
        )
    
    updated_note = await collection.find_one({"_id":ObjectId(note_id)})

    return helper_note(updated_note)


