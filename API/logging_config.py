import logging
from logging.handlers import RotatingFileHandler

# Configure logging
log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

logging.basicConfig(
    level=logging.INFO,
    format=log_format,
    handlers=[
        RotatingFileHandler("app.log", maxBytes=5*1024*1024, backupCount=3),  # rotating logs
        logging.StreamHandler()  # console output
    ]
)

# Create a logger instance
logger = logging.getLogger("fastapi_app")
