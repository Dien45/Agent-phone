"""
Command execution router for Windows Server.
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import subprocess

router = APIRouter(prefix="/execute", tags=["Commands"])

class CommandRequest(BaseModel):
    command: str

class CommandResponse(BaseModel):
    result: str
    exit_code: int

ALLOWED_COMMANDS = {"dir", "notepad", "powershell", "cmd", "git", "pip", "python", "node", "npm"}

@router.post("", response_model=CommandResponse)
async def execute_command(req: CommandRequest):
    parts = req.command.strip().split()
    if not parts:
        raise HTTPException(status_code=400, detail="Empty command")
    
    subcommand = parts[0]
    if subcommand not in ALLOWED_COMMANDS:
        raise HTTPException(status_code=411, detail=f"Command '{subcommand}' not allowed")

    try:
        result = subprocess.run(
            req.command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30
        )
        return CommandResponse(
            result=result.stdout or result.stderr,
            exit_code=result.returncode
        )
    except subprocess.TimeoutExpired:
        raise HTTPException(status_code=408, detail="Command timeout")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))