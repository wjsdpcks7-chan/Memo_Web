from fastapi import FastAPI, HTTPException
from pathlib import Path
from pydantic import BaseModel
from fastapi.responses import FileResponse

app = FastAPI()
folder = Path("memo")

class Memo(BaseModel):
    content: str

@app.get("/")
async def root():
    return FileResponse("index.html")

@app.get("/list")
async def list():
    return FileResponse("list.html")

@app.post("/memos", status_code=201)
async def save(memo: Memo):
    new_id = len(list(folder.glob("*.txt"))) +1
    file_path = folder/f"{new_id}.txt"
    file_path.write_text(memo.content, encoding="utf-8")
    return { "id" : new_id }

@app.get("/memos/{id}")
async def get_content(id: int):
    file_path = folder/f"{id}.txt"
    if not file_path.exists():
        raise HTTPException(status_code=404)
    else:
        content = file_path.read_text(encoding="utf-8")
    return { "id" : id, "content" : content}

@app.get("/memos")
async def get_list():

    files = []
    for f in folder.glob("*.txt"):
        files.append(int(f.stem))

    return sorted(files)