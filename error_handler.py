import logging
import sys
from functools import wraps

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("wake_word_app.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger("WakeWordApp")

class AppError(Exception):
    """Base class for application-specific errors."""
    pass

class ModelError(AppError):
    """Raised when there's an error with the wake word model."""
    pass

class AudioError(AppError):
    """Raised when there's an error with audio processing."""
    pass

def log_error(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {str(e)}", exc_info=True)
            raise
    return wrapper

def handle_error(error_type, message):
    """Handle errors by logging them and optionally performing additional actions."""
    logger.error(f"{error_type}: {message}")
    # Add any additional error handling logic here, such as showing an error dialog

def log_info(message):
    """Log an info message."""
    logger.info(message)

def log_warning(message):
    """Log a warning message."""
    logger.warning(message)