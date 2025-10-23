"""
VietOCR text recognition service
"""
import time
import logging
from typing import List, Dict, Any, Tuple
import cv2
from PIL import Image
from vietocr.tool.predictor import Predictor
from vietocr.tool.config import Cfg
from app.core.config import settings

logger = logging.getLogger("ocr")


class OCRService:
    """VietOCR text recognition service"""
    
    def __init__(self):
        self.ocr = None
        self._load_model()
    
    def _load_model(self):
        """Load VietOCR model"""
        try:
            logger.info(f"Loading VietOCR model: {settings.VIETOCR_MODEL_NAME}")
            config = Cfg.load_config_from_name(settings.VIETOCR_MODEL_NAME)
            config['weights'] = settings.VIETOCR_WEIGHTS_PATH
            config['device'] = settings.DEVICE
            self.ocr = Predictor(config)
            logger.info("VietOCR model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load VietOCR model: {e}")
            raise
    
    def extract_text_from_regions(self, image_path: str, text_regions: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], float]:
        """
        Extract text from detected regions
        
        Args:
            image_path: Path to input image
            text_regions: List of text regions from YOLO
            
        Returns:
            Tuple of (extracted_results, extraction_time)
        """
        logger.info(f"Extracting text from {len(text_regions)} regions")
        start_time = time.time()
        extracted_results = []
        
        # Load original image
        image = cv2.imread(image_path)
        if image is None:
            logger.error(f"Cannot read image: {image_path}")
            raise ValueError(f"Cannot read image: {image_path}")
        
        for region in text_regions:
            try:
                x1, y1, x2, y2 = region['bbox']
                cropped_image = image[y1:y2, x1:x2]
                
                # Convert OpenCV image to PIL Image for VietOCR
                cropped_pil = Image.fromarray(cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB))
                
                # Extract text
                text = self.ocr.predict(cropped_pil)
                
                extracted_results.append({
                    'bbox': region['bbox'],
                    'extracted_text': text,
                    'yolo_confidence': region['confidence'],
                    'ocr_confidence': 1.0,  # VietOCR doesn't return confidence
                    'class_id': region['class_id'],
                    'class_name': region['class_name']
                })
                
                logger.debug(f"Extracted text from {region['class_name']}: '{text}'")
                
            except Exception as e:
                logger.warning(f"OCR failed for region {region['id']} ({region['class_name']}): {e}")
                extracted_results.append({
                    'bbox': region['bbox'],
                    'extracted_text': '',
                    'yolo_confidence': region['confidence'],
                    'ocr_confidence': 0.0,
                    'class_id': region['class_id'],
                    'class_name': region['class_name']
                })
        
        extraction_time = time.time() - start_time
        logger.info(f"OCR completed: {len(extracted_results)} texts extracted in {extraction_time:.3f}s")
        
        return extracted_results, extraction_time
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get model information"""
        return {
            "model_name": settings.VIETOCR_MODEL_NAME,
            "weights_path": settings.VIETOCR_WEIGHTS_PATH,
            "device": settings.DEVICE
        }

