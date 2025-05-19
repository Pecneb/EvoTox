import logging
import os

def get_evotox_logger(log_file='evotox.log', log_level=logging.INFO):
    """
    Returns a logger configured for the EvoTox repository.
    Logs messages to the specified file with a standard format.
    """
    logger = logging.getLogger('EvoToxLogger')
    logger.setLevel(log_level)
    if not logger.handlers:
        # Ensure the log directory exists
        log_dir = os.path.dirname(log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)
        # File handler
        fh = logging.FileHandler(log_file)
        fh.setLevel(log_level)
        formatter = logging.Formatter(
            '[%(asctime)s] %(levelname)s %(name)s: %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        fh.setFormatter(formatter)
        logger.addHandler(fh)
    return logger

# Example usage:
# logger = get_evotox_logger()
# logger.info("EvoTox logger initialized.")