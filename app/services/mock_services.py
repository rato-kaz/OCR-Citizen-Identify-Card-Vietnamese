"""
Mock services for testing FastAPI structure without AI dependencies
"""
import time
import logging
from typing import Dict, Any, List, Tuple
from app.core.config import settings

logger = logging.getLogger("models")


class MockYOLOService:
    """Mock YOLO service for testing"""
    
    def __init__(self):
        self.class_names = {
            0: "bhyt", 1: "cccd", 2: "current_place1", 3: "current_place2",
            4: "dob", 5: "expire_date", 6: "gender", 7: "id", 8: "id_",
            9: "ihos", 10: "iplace", 11: "issue_date", 12: "name",
            13: "nationality", 14: "origin_place1", 15: "origin_place2", 16: "personal_identifi"
        }
        self.text_class_ids = [2, 3, 4, 6, 7, 12, 13]
        logger.info("Mock YOLO service initialized")
    
    def detect_text_regions(self, image_path: str) -> Tuple[List[Dict[str, Any]], float, List[Dict[str, Any]]]:
        """Mock text detection"""
        logger.info(f"Mock YOLO detecting text regions in {image_path}")
        time.sleep(0.1)  # Simulate processing time
        
        # Mock detected regions
        mock_regions = [
            {
                'id': 1,
                'bbox': [100, 50, 300, 80],
                'confidence': 0.95,
                'class_id': 12,
                'class_name': 'name'
            },
            {
                'id': 2,
                'bbox': [100, 100, 200, 130],
                'confidence': 0.90,
                'class_id': 7,
                'class_name': 'id'
            }
        ]
        
        return mock_regions, 0.1, mock_regions
    
    def get_model_info(self) -> Dict[str, Any]:
        return {
            "model_path": "mock_yolo_model.pt",
            "num_classes": len(self.class_names),
            "class_names": self.class_names,
            "text_class_ids": self.text_class_ids,
            "text_labels": settings.TEXT_LABELS
        }


class MockOCRService:
    """Mock OCR service for testing"""
    
    def __init__(self):
        logger.info("Mock OCR service initialized")
    
    def extract_text_from_regions(self, image_path: str, text_regions: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], float]:
        """Mock text extraction"""
        logger.info(f"Mock OCR extracting text from {len(text_regions)} regions")
        time.sleep(0.2)  # Simulate processing time
        
        # Mock extracted results
        mock_results = []
        for region in text_regions:
            mock_text = f"Mock text for {region['class_name']}"
            mock_results.append({
                'bbox': region['bbox'],
                'extracted_text': mock_text,
                'yolo_confidence': region['confidence'],
                'ocr_confidence': 0.95,
                'class_id': region['class_id'],
                'class_name': region['class_name']
            })
        
        return mock_results, 0.2
    
    def get_model_info(self) -> Dict[str, Any]:
        return {
            "model_name": "mock_vietocr",
            "weights_path": "mock_weights.pth",
            "device": "cpu"
        }

