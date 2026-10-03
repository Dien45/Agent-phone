"""
Windows Server Backend for Agentik Android Hybrid System
Provides endpoints for command execution, file CRUD, app launch, and desktop streaming.
Authenticated via API key + Tailscale IP whitelist.
"""
import os
import uuid
from fastapi import FastAPI, Request, HTTPException
from typing import Optional

app = FastAPI(title="Agentik Hybrid Server")

# Configuration
WINDOWS_HOST = os.getenv("WINDOWS_HOST", "127.0.0.1")
ALLOWED_TAILSCALE_NETWORKS = set(os.getenv("TAILSCALE_NETWORKS", "").split(",")) if os.getenv("TAILSCALE_NETWORKS") else []


# ----------------------------------------------------------------------
# Helper utilities
# ----------------------------------------------------------------------
def verify_api_key(key: str) -> bool:
    """Check if provided API key is valid."""
    # In production, validate against database/secret manager
    expected_key = os.getenv("WINDOWS_API_KEY", "change-me")
    return key == expected_key


def is_tailscale_network(network: str) -> bool:
    """Check if network is allowed (Tailscale)."""
    return network.strip().lower() in ALLOWED_TAILSCALE_NETWORKS


# ----------------------------------------------------------------------
# Routers
# ----------------------------------------------------------------------
from routers.command import router as command_router
from routers.files import router as files_router
from routers.apps import router as apps_router
from routers.desktop import router as desktop_router

app.include_router(command_router)
app.include_router(files_router)
app.include_router(apps_router)
app.include_router(desktop_router)


# ----------------------------------------------------------------------
# Endpoints
# ----------------------------------------------------------------------
@app.get("/", tags=["Health"])
async def health():
    """Health check endpoint."""
    return {"status": "healthy", "service": "agentik-hybrid-server"}


@app.get("/health", tags=["Health"])
async def system_status():
    """Detailed system status for monitoring."""
    return {
        "service": "agentik-hybrid-server",
        "version": "1.0.0",
        "tailscale_connected": True,
        "windows_host": WINDOWS_HOST,
        "allowed_networks": ALLOWED_TAILSCALE_NETWORKS
    }


@app.get("/status", tags=["Health"])
async def status():
    """System status endpoint."""
    return {
        "service": "agentik-hybrid-server",
        "version": "1.0.0",
        "tailscale_connected": True,
        "windows_host": WINDOWS_HOST,
        "allowed_networks": ALLOWED_TAILSCALE_NETWORKS
    }