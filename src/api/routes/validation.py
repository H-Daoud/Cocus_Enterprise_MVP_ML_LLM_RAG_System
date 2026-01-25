"""
Data validation API endpoints
"""

import json
from typing import List

from fastapi import APIRouter, File, HTTPException, UploadFile, status
from pydantic import BaseModel, ValidationError

from src.models.order import Order
from src.utils.logger import get_logger

logger = get_logger(__name__)
router = APIRouter()


class ValidationResult(BaseModel):
    """Validation result model"""

    total: int
    valid: int
    invalid: int
    errors: List[dict]


@router.post("/validate", response_model=ValidationResult)
async def validate_orders(file: UploadFile = File(...)):
    """
    Validate order data file

    Accepts NDJSON file with order data and validates each record
    Returns validation statistics and error details
    """
    if not file.filename.endswith(".ndjson"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Only NDJSON files are supported"
        )

    content = await file.read()
    lines = content.decode("utf-8").strip().split("\n")

    valid_count = 0
    invalid_count = 0
    errors = []

    for idx, line in enumerate(lines, 1):
        try:
            data = json.loads(line)
            order = Order(**data)
            valid_count += 1
            logger.debug(f"Line {idx}: Valid order {order.order_id}")
        except (json.JSONDecodeError, ValidationError) as e:
            invalid_count += 1
            errors.append({"line": idx, "error": str(e), "data": line[:100]})  # First 100 chars
            logger.warning(f"Line {idx}: Validation error - {str(e)}")

    result = ValidationResult(
        total=len(lines),
        valid=valid_count,
        invalid=invalid_count,
        errors=errors[:10],  # Return first 10 errors
    )

    logger.info(f"Validation completed: {valid_count} valid, {invalid_count} invalid")

    return result
