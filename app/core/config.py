"""
Application configuration settings
"""
import os
from pathlib import Path
from typing import List


class Settings:
    """Application settings"""
    
    # API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Vietnamese OCR Service"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "YOLO + VietOCR pipeline for Vietnamese ID card text extraction"
    
    # Model paths
    YOLO_MODEL_PATH: str = "models/Text_Detection/YOLO/ID_CARD_2.pt"
    VIETOCR_MODEL_NAME: str = "vgg_transformer"
    VIETOCR_WEIGHTS_PATH: str = f"models/Text_Recognition/Vietocr/{VIETOCR_MODEL_NAME}.pth"
    
    # Device settings
    DEVICE: str = "cuda:0"  # or "cpu"
    
    # Text labels to process
    TEXT_LABELS: List[str] = [
        "dob", "gender", "id", "name", "nationality", 
        "current_place1", "current_place2", "expire_date", 
        "issue_date", "origin_place1", "origin_place2", "personal_identifi"
    ]
    
    # File settings
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS: List[str] = [".jpg", ".jpeg", ".png", ".bmp", ".tiff"]
    OUTPUT_DIR: str = "output"
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Performance
    MAX_CONCURRENT_REQUESTS: int = 5
    REQUEST_TIMEOUT: int = 30  # seconds
    
    def __init__(self):
        """Initialize settings and create necessary directories"""
        self._create_directories()
    
    def _create_directories(self):
        """Create necessary directories if they don't exist"""
        Path(self.OUTPUT_DIR).mkdir(exist_ok=True)
        Path("logs").mkdir(exist_ok=True)


# Global settings instance
settings = Settings()

