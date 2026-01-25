"""
Health check endpoints
"""

from fastapi import APIRouter, status
from pydantic import BaseModel
from datetime import datetime
import psutil
import platform

router = APIRouter()


class HealthResponse(BaseModel):
    """Health check response model"""

    status: str
    timestamp: datetime
    version: str
    system: dict


@router.get("/health", response_model=HealthResponse, status_code=status.HTTP_200_OK)
async def health_check():
    """
    Health check endpoint
    Returns system health status and metrics
    """
    return HealthResponse(
        status="healthy",
        timestamp=datetime.utcnow(),
        version="1.0.0",
        system={
            "cpu_percent": psutil.cpu_percent(),
            "memory_percent": psutil.virtual_memory().percent,
            "platform": platform.system(),
            "python_version": platform.python_version(),
        },
    )


@router.get("/health/ready", status_code=status.HTTP_200_OK)
async def readiness_check():
    """
    Readiness check for Kubernetes
    Returns 200 if service is ready to accept traffic
    """
    # Add checks for database, Redis, etc.
    return {"status": "ready"}


@router.get("/health/live", status_code=status.HTTP_200_OK)
async def liveness_check():
    """
    Liveness check for Kubernetes
    Returns 200 if service is alive
    """
    return {"status": "alive"}
