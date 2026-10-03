"""
Windows Server Backend - Agentik Android Hybrid System
Provides endpoints: command execution, file CRUD, app launch, desktop streaming.
Authenticated via API key + Tailscale whitelist.
"""
import os
import uuid

import fastapi
import typing

app = fastapi.FastAPI(title="Agentik Hybrid Server")

# ----------------------------------------------------------------------
# Configuration
# ----------------------------------------------------------------------
WINDOWS_HOST = os.getenv("WINDOWS_HOST", "127.0.0.1")
ALLOWED_TAILSCALE_NETWORKS = set(
    os.getenv("TAILSCALE_NETWORKS", "").split(",")
) if os.getenv("TAILSCALE_NETWORKS") else set()

# ----------------------------------------------------------------------
# Helper utilities
# ----------------------------------------------------------------------
def verify_api_key(key: str) -> bool:
    """Check provided API key is valid."""
    expected_key = os.getenv("WINDOWS_API_KEY", "change-me")
    return key == expected_key


def is_tailscale_network(network: str) -> bool:
    """Check network is allowed (Tailscale)."""
    return network.strip().lower() in ALLOWED_TAILSCALE_NETWORKS


# ----------------------------------------------------------------------
# Routers
# ----------------------------------------------------------------------
from routers import command
from routers import files
from routers import apps
from routers import desktop

app.include_router(command.router)
app.include_router(files.router)
app.include_router(apps.router)
app.include_router(desktop.router)

# ----------------------------------------------------------------------
# Endpoints
# ----------------------------------------------------------------------
@app.get("/", tags=["Health"])
async def root():
    """Root endpoint."""
    return {"service": "agentik-hybrid-server"}


@app.get("/health", tags=["Health"])
async def health():
    """Health check endpoint."""
    return {"status": "healthy", "service": "agentik-hybrid-server"}


@app.get("/status", tags=["Health"])
async def status():
    """System status endpoint."""
    return {
        "service": "agentik-hybrid-server",
        "version": "1.0.0",
        "tailscale_connected": True,
        "windows_host": WINDOWS_HOST,
        "allowed_networks": list(ALLOWED_TAILSCALE_NETWORKS),
    }
