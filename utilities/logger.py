# utilities/logger.py
import logging
from logging.handlers import RotatingFileHandler
import os
from datetime import datetime

def setup_logger(name=None):
    """
    Configures and returns a configured logger instance with both file and console output.
    
    Features:
    - Creates a dedicated 'logs' directory if it doesn't exist
    - Rotating log files (5MB max, keeps 3 backups)
    - Timestamped log filenames
    - Standardized log format
    - Prevents duplicate handlers
    
    Args:
        name (str, optional): Logger name. Defaults to "guvi_automation".
        
    Returns:
        logging.Logger: Configured logger instance
    """
    
    # Create logs directory if it doesn't exist
    log_dir = os.path.join(os.getcwd(), "logs")
    os.makedirs(log_dir, exist_ok=True)  # exist_ok prevents errors if dir exists
    
    # Create or get logger instance
    logger = logging.getLogger(name or "guvi_automation")
    logger.setLevel(logging.INFO)  # Set minimum log level to INFO
    
    # Only add handlers if they haven't been added before
    # This prevents duplicate logs when setup_logger is called multiple times
    if not logger.handlers:
        # Create formatter with standardized format
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'  # Human-readable timestamp format
        )
        
        # Configure rotating file handler
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")  # For unique filenames
        log_file = os.path.join(log_dir, f"guvi_test_{timestamp}.log")
        
        file_handler = RotatingFileHandler(
            log_file, 
            maxBytes=5*1024*1024,  # Rotate after 5MB
            backupCount=3,          # Keep 3 backup logs
            encoding='utf-8'        # Ensure proper character encoding
        )
        file_handler.setFormatter(formatter)
        
        # Configure console output handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        
        # Add both handlers to the logger
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
    
    return logger

# Create and export a default logger instance
# This can be imported directly from other modules as 'from utilities.logger import logger'
logger = setup_logger()  # Instance with default name "guvi_automation"