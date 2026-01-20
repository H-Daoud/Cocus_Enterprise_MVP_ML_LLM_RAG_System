"""
FastAPI main application
Enterprise-grade API with security, monitoring, and compliance
"""

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse
from prometheus_fastapi_instrumentator import Instrumentator
import time
from contextlib import asynccontextmanager

from src.api.routes import health, validation, rag
from src.api.middleware.error_handler import error_handler_middleware
from src.utils.logger import get_logger

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    logger.info("Starting COCUS MVP API...")
    yield
    # Shutdown
    logger.info("Shutting down COCUS MVP API...")


# Initialize FastAPI application
app = FastAPI(
    title="COCUS MVP ML/LLM RAG System",
    description="Enterprise-grade ML and RAG system with GDPR and EU AI Act compliance",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# GZip compression
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Request timing middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

# Error handler middleware
app.middleware("http")(error_handler_middleware)

# Prometheus metrics
Instrumentator().instrument(app).expose(app, endpoint="/metrics")

# Include routers
app.include_router(health.router, prefix="/api", tags=["Health"])
app.include_router(validation.router, prefix="/api/validation", tags=["Validation"])
app.include_router(rag.router, prefix="/api/rag", tags=["RAG"])

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": "COCUS MVP ML/LLM RAG System",
        "version": "1.0.0",
        "status": "operational",
        "docs": "/api/docs"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
