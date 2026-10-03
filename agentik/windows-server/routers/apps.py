"""
Application launcher router for Windows Server.
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/apps", tags=["Applications"])

class AppRequest(BaseModel):
    app_id: str

class AppResponse(BaseModel):
    app_id: str
    status: str

# Application registry (Windows)
APP_REGISTRY = {
    "chrome": "chrome.exe",
    "firefox": "firefox.exe",
    "notepad": "notepad.exe",
    "vscode": "code.exe",
    "explorer": "explorer.exe",
    "spotify": "spotify.exe",
    "steam": "steam.exe",
    "discord": "discord.exe",
}

@router.post("/launch")
async def launch_app(request: AppRequest):
    executable = APP_REGISTRY.get(request.app_id)
    if not executable:
        raise HTTPException(status_code=404, detail=f"App '{request.app_id}' not found")

    try:
        import subprocess
        subprocess.Popen(executable)
        return AppResponse(app_id=request.app_id, status="launched")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/close/{app_id}")
async def close_app(app_id: str):
    executable = APP_REGISTRY.get(app_id)
    if not executable:
        raise HTTPException(status_code=404, detail=f"App '{app_id}' not found")

    try:
        import subprocess
        subprocess.run(["taskkill", "/F", "/IM", executable], check=True)
        return {"app_id": app_id, "status": "closed"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))