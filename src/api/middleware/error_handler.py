"""
Error handler middleware
"""

import traceback

from fastapi import Request, status
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from src.utils.logger import get_logger

logger = get_logger(__name__)


async def error_handler_middleware(request: Request, call_next):
    """
    Global error handler middleware
    Catches and logs all exceptions, returns appropriate responses
    """
    try:
        response = await call_next(request)
        return response
    except ValidationError as e:
        logger.warning(f"Validation error: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"error": "Validation Error", "detail": e.errors()},
        )
    except Exception as e:
        logger.error(f"Unhandled exception: {str(e)}\n{traceback.format_exc()}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": "Internal Server Error", "message": "An unexpected error occurred"},
        )
