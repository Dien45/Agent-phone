"""
File manager router for Windows Server.
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from pathlib import Path
import os

router = APIRouter(prefix="/files", tags=["Files"])

class FileRequest(BaseModel):
    path: str

class FileResponse(BaseModel):
    name: str
    size: int
    is_dir: bool

@router.get("/list")
async def list_files(request: FileRequest):
    target = Path(request.path)
    if not target.exists() or not target.is_dir():
        raise HTTPException(status_code=404, detail="Path not found")

    entries = []
    for entry in target.iterdir():
        try:
            stat = entry.stat()
            entries.append(FileResponse(
                name=entry.name,
                size=stat.st_size,
                is_dir=entry.is_dir()
            ))
        except PermissionError:
            continue

    return {"path": str(target), "entries": entries}

@router.get("/download/{filename}")
async def download_file(filename: str, save_path: str = "."):
    target = Path(save_path) / filename
    if not target.exists():
        raise HTTPException(status_code=404, detail="File not found")

    return {
        "filename": filename,
        "path": str(target),
        "size": target.stat().st_size
    }

@router.post("/upload")
async def upload_file(filename: str, content: str):
    target = Path(filename)
    target.write_text(content)
    return {"filename": filename, "status": "uploaded"}

@router.delete("/delete/{filename}")
async def delete_file(filename: str):
    target = Path(filename)
    if not target.exists():
        raise HTTPException(status_code=404, detail="File not found")
    target.unlink()
    return {"filename": filename, "status": "deleted"}