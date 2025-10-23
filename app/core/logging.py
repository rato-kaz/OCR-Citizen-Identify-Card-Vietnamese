"""
Logging configuration for the application
"""
import logging
import sys
from pathlib import Path
from app.core.config import settings


def setup_logging():
    """Setup application logging"""
    
    # Create logs directory
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # Configure root logger
    logging.basicConfig(
        level=getattr(logging, settings.LOG_LEVEL),
        format=settings.LOG_FORMAT,
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(log_dir / "app.log"),
        ]
    )
    
    # Create specific loggers
    api_logger = logging.getLogger("api")
    api_logger.setLevel(logging.INFO)
    
    model_logger = logging.getLogger("models")
    model_logger.setLevel(logging.INFO)
    
    ocr_logger = logging.getLogger("ocr")
    ocr_logger.setLevel(logging.INFO)
    
    return {
        "api": api_logger,
        "models": model_logger,
        "ocr": ocr_logger
    }


# Initialize loggers
loggers = setup_logging()

