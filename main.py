from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Entry(BaseModel):
    author: str
    message: str

guestbook = []

@app.get("/entries")
async def get_entries():
    return {"entries": guestbook}

@app.post("/add_entry")
async def add_entry(entry: Entry):
    new_entry = {
        "author": entry.author,
        "message": entry.message,
        "timestamp": datetime.now().isoformat()
    }
    guestbook.append(new_entry)
    return {"success": True, "index": len(guestbook) - 1}

@app.delete("/entries/{index}")
async def delete_entry(index: int):
    if 0 <= index < len(guestbook):
        guestbook.pop(index)
        return {"success": True}
    raise HTTPException(status_code=404, detail="Entry not found")

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, debug=True)
