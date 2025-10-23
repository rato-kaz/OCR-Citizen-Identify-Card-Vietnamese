"""
Mock FastAPI endpoints for testing structure
"""
import os
import time
import logging
from typing import Optional
from fastapi import APIRouter, File, UploadFile, HTTPException, Depends
from fastapi.responses import JSONResponse
from app.models.schemas import OCRResponse, ErrorResponse, HealthResponse
from app.services.mock_pipeline import MockOCRPipeline
from app.core.config import settings

logger = logging.getLogger("api")
router = APIRouter()

# Global pipeline instance
pipeline: Optional[MockOCRPipeline] = None


def get_pipeline() -> MockOCRPipeline:
    """Get or initialize mock OCR pipeline"""
    global pipeline
    if pipeline is None:
        try:
            pipeline = MockOCRPipeline()
        except Exception as e:
            logger.error(f"Failed to initialize mock pipeline: {e}")
            raise HTTPException(status_code=500, detail="Failed to initialize mock OCR pipeline")
    return pipeline


@router.post("/detect", response_model=OCRResponse)
async def detect_text(
    file: UploadFile = File(...),
    ocr_pipeline: MockOCRPipeline = Depends(get_pipeline)
):
    """
    Mock detect and extract text from uploaded image
    
    Args:
        file: Uploaded image file
        
    Returns:
        OCRResponse with detected texts and metadata
    """
    logger.info(f"Received file: {file.filename}")
    
    # Validate file
    if not file.filename:
        raise HTTPException(status_code=400, detail="No filename provided")
    
    # Check file extension
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in settings.ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400, 
            detail=f"File type {file_ext} not allowed. Allowed types: {settings.ALLOWED_EXTENSIONS}"
        )
    
    # Check file size
    file_content = await file.read()
    if len(file_content) > settings.MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"File too large. Max size: {settings.MAX_FILE_SIZE} bytes"
        )
    
    try:
        # Save uploaded file temporarily
        temp_filename = f"temp_{int(time.time())}_{file.filename}"
        temp_path = os.path.join(settings.OUTPUT_DIR, temp_filename)
        
        with open(temp_path, "wb") as buffer:
            buffer.write(file_content)
        
        logger.info(f"Saved temporary file: {temp_path}")
        
        # Process image with mock pipeline
        result = ocr_pipeline.process_image(temp_path)
        
        # Clean up temporary file
        try:
            os.remove(temp_path)
            logger.info(f"Cleaned up temporary file: {temp_path}")
        except Exception as e:
            logger.warning(f"Failed to clean up temporary file: {e}")
        
        return result
        
    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Processing failed: {e}")
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")


@router.get("/health", response_model=HealthResponse)
async def health_check(ocr_pipeline: MockOCRPipeline = Depends(get_pipeline)):
    """
    Health check endpoint
    
    Returns:
        HealthResponse with service status
    """
    try:
        service_info = ocr_pipeline.get_service_info()
        is_ready = ocr_pipeline.is_ready()
        
        return HealthResponse(
            status="healthy" if is_ready else "unhealthy",
            version=settings.VERSION,
            models_loaded=is_ready,
            uptime=service_info.get("uptime", 0)
        )
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return HealthResponse(
            status="unhealthy",
            version=settings.VERSION,
            models_loaded=False,
            uptime=0
        )


@router.get("/info")
async def get_service_info(ocr_pipeline: MockOCRPipeline = Depends(get_pipeline)):
    """
    Get detailed service information
    
    Returns:
        Service information including model details
    """
    try:
        return ocr_pipeline.get_service_info()
    except Exception as e:
        logger.error(f"Failed to get service info: {e}")
        raise HTTPException(status_code=500, detail="Failed to get service information")

