from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

app = FastAPI()

# CORS (Cross-Origin Resource Sharing) middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],  # Replace with your frontend URL during development
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
    allow_headers=["*"],
)

# Temporary in-memory storage for notes
notes = []

# Model for Note schema
class Note(BaseModel):
    id: int
    title: str
    content: str

# Model for Note schema without ID (for creation)
class NoteCreate(BaseModel):
    title: str
    content: str

# CRUD operations

# Create a new note
@app.post("/notes/", response_model=Note)
async def create_note(note: NoteCreate):
    new_id = len(notes) + 1
    new_note = Note(**note.dict(), id=new_id)
    notes.append(new_note)
    return new_note

# Read all notes
@app.get("/notes/", response_model=List[Note])
async def read_notes():
    return notes

# Read a single note by ID
@app.get("/notes/{note_id}", response_model=Note)
async def read_note(note_id: int):
    for note in notes:
        if note.id == note_id:
            return note
    raise HTTPException(status_code=404, detail="Note not found")

# Update a note by ID
@app.put("/notes/{note_id}", response_model=Note)
async def update_note(note_id: int, note: NoteCreate):
    for existing_note in notes:
        if existing_note.id == note_id:
            existing_note.title = note.title
            existing_note.content = note.content
            return existing_note
    raise HTTPException(status_code=404, detail="Note not found")

# Delete a note by ID
@app.delete("/notes/{note_id}", response_model=Note)
async def delete_note(note_id: int):
    for index, note in enumerate(notes):
        if note.id == note_id:
            notes.pop(index)
            return note
    raise HTTPException(status_code=404, detail="Note not found")

# Additional CRUD operations

# Search notes by title (substring match)
@app.get("/notes/search/", response_model=List[Note])
async def search_notes_by_title(query: str):
    matching_notes = []
    for note in notes:
        if query.lower() in note.title.lower():
            matching_notes.append(note)
    return matching_notes

# Batch create notes
@app.post("/notes/batch/", response_model=List[Note])
async def create_batch_notes(notes_to_create: List[NoteCreate]):
    created_notes = []
    for note_data in notes_to_create:
        new_id = len(notes) + 1
        new_note = Note(**note_data.dict(), id=new_id)
        notes.append(new_note)
        created_notes.append(new_note)
    return created_notes

# Update note title only (partial update)
@app.patch("/notes/{note_id}/title/", response_model=Note)
async def update_note_title(note_id: int, new_title: str):
    for existing_note in notes:
        if existing_note.id == note_id:
            existing_note.title = new_title
            return existing_note
    raise HTTPException(status_code=404, detail="Note not found")

# Archive note (soft delete)
@app.put("/notes/{note_id}/archive/", response_model=Note)
async def archive_note(note_id: int):
    for existing_note in notes:
        if existing_note.id == note_id:
            existing_note.archived = True  # Assuming an archived field is added dynamically
            return existing_note
    raise HTTPException(status_code=404, detail="Note not found")
