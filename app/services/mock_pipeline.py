"""
Mock OCR pipeline for testing FastAPI structure
"""
import os
import time
import logging
from typing import Dict, Any, Optional
from datetime import datetime
from app.services.mock_services import MockYOLOService, MockOCRService
from app.models.schemas import OCRResponse, DetectedText, BoundingBox, ProcessingTiming
from app.core.config import settings

logger = logging.getLogger("api")


class MockOCRPipeline:
    """Mock OCR pipeline for testing"""
    
    def __init__(self):
        self.yolo_service = None
        self.ocr_service = None
        self.start_time = time.time()
        self._initialize_services()
    
    def _initialize_services(self):
        """Initialize mock services"""
        try:
            logger.info("Initializing mock OCR pipeline services...")
            self.yolo_service = MockYOLOService()
            self.ocr_service = MockOCRService()
            logger.info("Mock OCR pipeline services initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize mock OCR pipeline: {e}")
            raise
    
    def process_image(self, image_path: str) -> OCRResponse:
        """Mock image processing"""
        logger.info(f"Mock processing image: {image_path}")
        
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image not found: {image_path}")
        
        try:
            # Step 1: Mock YOLO Detection
            text_regions, detection_time, all_regions = self.yolo_service.detect_text_regions(image_path)
            
            if not text_regions:
                logger.warning("No text regions detected for OCR")
                return OCRResponse(
                    success=True,
                    image_path=image_path,
                    total_regions=len(all_regions),
                    detected_texts=[],
                    timing=ProcessingTiming(
                        detection_time=detection_time,
                        ocr_time=0.0,
                        total_time=detection_time
                    ),
                    message="No text regions detected"
                )
            
            # Step 2: Mock OCR Text Extraction
            extracted_results, ocr_time = self.ocr_service.extract_text_from_regions(
                image_path, text_regions
            )
            
            total_time = detection_time + ocr_time
            
            # Step 3: Convert to response format
            detected_texts = []
            for result in extracted_results:
                bbox = BoundingBox(
                    x1=result['bbox'][0],
                    y1=result['bbox'][1], 
                    x2=result['bbox'][2],
                    y2=result['bbox'][3]
                )
                
                detected_text = DetectedText(
                    class_name=result['class_name'],
                    extracted_text=result['extracted_text'],
                    bbox=bbox,
                    confidence=result['yolo_confidence'],
                    class_id=result['class_id']
                )
                detected_texts.append(detected_text)
            
            logger.info(f"Mock pipeline completed successfully:")
            logger.info(f"  - Total regions: {len(all_regions)}")
            logger.info(f"  - Text regions: {len(text_regions)}")
            logger.info(f"  - Extracted texts: {len(extracted_results)}")
            logger.info(f"  - Detection time: {detection_time:.3f}s")
            logger.info(f"  - OCR time: {ocr_time:.3f}s")
            logger.info(f"  - Total time: {total_time:.3f}s")
            
            return OCRResponse(
                success=True,
                image_path=image_path,
                total_regions=len(all_regions),
                detected_texts=detected_texts,
                timing=ProcessingTiming(
                    detection_time=detection_time,
                    ocr_time=ocr_time,
                    total_time=total_time
                )
            )
            
        except Exception as e:
            logger.error(f"Mock pipeline processing failed: {e}")
            raise
    
    def get_service_info(self) -> Dict[str, Any]:
        """Get information about loaded services"""
        return {
            "yolo": self.yolo_service.get_model_info() if self.yolo_service else None,
            "ocr": self.ocr_service.get_model_info() if self.ocr_service else None,
            "uptime": time.time() - self.start_time
        }
    
    def is_ready(self) -> bool:
        """Check if pipeline is ready for processing"""
        return self.yolo_service is not None and self.ocr_service is not None

