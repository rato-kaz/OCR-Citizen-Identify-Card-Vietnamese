"""
YOLO detection service
"""
import time
import logging
from typing import List, Tuple, Dict, Any
from ultralytics import YOLO
from app.core.config import settings

logger = logging.getLogger("models")


class YOLOService:
    """YOLO text detection service"""
    
    def __init__(self):
        self.model = None
        self.class_names = {}
        self.text_class_ids = []
        self._load_model()
        self._setup_text_labels()
    
    def _load_model(self):
        """Load YOLO model"""
        try:
            logger.info(f"Loading YOLO model from {settings.YOLO_MODEL_PATH}")
            self.model = YOLO(settings.YOLO_MODEL_PATH)
            self.class_names = self.model.names
            logger.info(f"YOLO model loaded successfully with {len(self.class_names)} classes")
        except Exception as e:
            logger.error(f"Failed to load YOLO model: {e}")
            raise
    
    def _setup_text_labels(self):
        """Setup text labels to process"""
        if not self.class_names:
            return
            
        for class_id, class_name in self.class_names.items():
            if class_name in settings.TEXT_LABELS:
                self.text_class_ids.append(int(class_id))
        
        logger.info(f"Text labels to process: {settings.TEXT_LABELS}")
        logger.info(f"Class IDs for text processing: {self.text_class_ids}")
    
    def detect_text_regions(self, image_path: str) -> Tuple[List[Dict[str, Any]], float, List[Dict[str, Any]]]:
        """
        Detect text regions in image
        
        Args:
            image_path: Path to input image
            
        Returns:
            Tuple of (text_regions, detection_time, all_regions)
        """
        logger.info(f"Detecting text regions in {image_path}")
        start_time = time.time()
        
        try:
            results = self.model(image_path)
            detection_time = time.time() - start_time
            
            text_regions = []
            all_regions = []
            
            for result in results:
                if result.boxes is not None:
                    boxes = result.boxes.xyxy.cpu().numpy()
                    confidences = result.boxes.conf.cpu().numpy()
                    classes = result.boxes.cls.cpu().numpy()
                    
                    for i, (box, conf, cls) in enumerate(zip(boxes, confidences, classes)):
                        x1, y1, x2, y2 = box.astype(int)
                        class_id = int(cls)
                        class_name = self.class_names.get(class_id, f"class_{class_id}")
                        
                        region_info = {
                            'id': i + 1,
                            'bbox': [int(x1), int(y1), int(x2), int(y2)],
                            'confidence': float(conf),
                            'class_id': class_id,
                            'class_name': class_name
                        }
                        
                        all_regions.append(region_info)
                        
                        # Only add text regions that we want to OCR
                        if class_id in self.text_class_ids:
                            text_regions.append(region_info)
            
            logger.info(f"YOLO detected {len(all_regions)} total regions")
            logger.info(f"Text regions for OCR: {len(text_regions)}")
            logger.info(f"Detection completed in {detection_time:.3f}s")
            
            return text_regions, detection_time, all_regions
            
        except Exception as e:
            logger.error(f"YOLO detection failed: {e}")
            raise
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get model information"""
        return {
            "model_path": settings.YOLO_MODEL_PATH,
            "num_classes": len(self.class_names),
            "class_names": self.class_names,
            "text_class_ids": self.text_class_ids,
            "text_labels": settings.TEXT_LABELS
        }

