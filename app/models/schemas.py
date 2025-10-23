"""
Pydantic models for API request/response schemas
"""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime


class BoundingBox(BaseModel):
    """Bounding box coordinates"""
    x1: int = Field(..., description="Top-left x coordinate")
    y1: int = Field(..., description="Top-left y coordinate") 
    x2: int = Field(..., description="Bottom-right x coordinate")
    y2: int = Field(..., description="Bottom-right y coordinate")


class DetectedText(BaseModel):
    """Detected text information"""
    class_name: str = Field(..., description="Class name (e.g., 'name', 'id', 'dob')")
    extracted_text: str = Field(..., description="Extracted text content")
    bbox: BoundingBox = Field(..., description="Bounding box coordinates")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Detection confidence score")
    class_id: int = Field(..., description="Class ID")


class ProcessingTiming(BaseModel):
    """Processing timing information"""
    detection_time: float = Field(..., description="YOLO detection time in seconds")
    ocr_time: float = Field(..., description="OCR processing time in seconds")
    total_time: float = Field(..., description="Total processing time in seconds")


class OCRResponse(BaseModel):
    """Main API response"""
    success: bool = Field(..., description="Whether processing was successful")
    image_path: str = Field(..., description="Path to processed image")
    total_regions: int = Field(..., description="Total number of detected regions")
    detected_texts: List[DetectedText] = Field(..., description="List of detected texts")
    timing: ProcessingTiming = Field(..., description="Processing timing information")
    timestamp: datetime = Field(default_factory=datetime.now, description="Processing timestamp")
    message: Optional[str] = Field(None, description="Additional message or error info")


class ErrorResponse(BaseModel):
    """Error response schema"""
    success: bool = Field(False, description="Always false for errors")
    error: str = Field(..., description="Error message")
    error_code: str = Field(..., description="Error code")
    timestamp: datetime = Field(default_factory=datetime.now, description="Error timestamp")


class HealthResponse(BaseModel):
    """Health check response"""
    status: str = Field(..., description="Service status")
    version: str = Field(..., description="API version")
    models_loaded: bool = Field(..., description="Whether AI models are loaded")
    timestamp: datetime = Field(default_factory=datetime.now, description="Check timestamp")
    uptime: float = Field(..., description="Service uptime in seconds")

