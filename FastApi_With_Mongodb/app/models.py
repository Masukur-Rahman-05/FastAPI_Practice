from pydantic import BaseModel,Field
from typing import Optional
from datetime import datetime

class NoteCreate(BaseModel):
    title : str =Field(...,min_length = 1,max_length=200,description="This will contain the title of the Note")
    content: str = Field(..., min_length = 1, description="This will contain the content of the Note")
    tags: Optional[list[str]] = Field(default=[], description="This will contain tags related to the Note")

    class Config:
        json_schema_extra={
            "example":{
                "title":"MongoDB with Fastapi",
                "content":"This Codebase is showing the way to integrate Mongodb with Fastapi",
                "tags":["python","mongodb","fastapi"]
            }
        }

class NoteResponse(BaseModel):
    id: str = Field(..., description="Mongodb ObjectId")
    title: str
    content: str
    tags : list[str]
    created_at: datetime = Field(..., description="Timestamp when the note has been created")

    class Config:
        json_schema_extra={
            "example":{
                "id": "507f1f77bcf86cd799439011",
                "title":"MongoDB with Fastapi",
                "content":"This Codebase is showing the way to integrate Mongodb with Fastapi",
                "tags":["python","mongodb","fastapi"],
                "created_at": "2024-01-15T10:30:00Z"
            }
        }
    
class NoteUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    content: Optional[str] = Field(None, min_length=1)
    tags: Optional[list[str]] = None

    class Config:
        json_schema_extra = {
            "example":{
                "title":"Update Title",
                "tags":["python","Fastapi","Mongodb","Motor"]
            }
        }
