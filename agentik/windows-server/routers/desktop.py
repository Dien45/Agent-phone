"""
Desktop streaming router for Windows Server.
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/desktop", tags=["Desktop"])

class DesktopResponse(BaseModel):
    stream_url: str
    status: str

@router.get("/vnc-stream")
async def get_desktop_stream():
    # In production, integrate with noVNC, x11vnc, or Windows RDP
    return DesktopResponse(
        stream_url="https://tailscale.io/vnc/windows",
        status="ready"
    )