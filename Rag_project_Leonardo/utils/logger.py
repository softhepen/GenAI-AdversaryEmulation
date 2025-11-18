import logging  
import os       

def get_logger(name="RAGLogger", log_dir="logs", log_file="rag.log"):
    # Create the log directory if it doesn't exist
    os.makedirs(log_dir, exist_ok=True)
    log_path = os.path.join(log_dir, log_file)  

    # Get or create a logger with the specified name
    logger = logging.getLogger(name)

    # Set the logging level to INFO
    logger.setLevel(logging.INFO)  

    # Define the format for log messages
    formatter = logging.Formatter("[%(asctime)s] %(levelname)s - %(message)s")

    # Create a console handler and apply the formatter
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # Create a file handler and apply the formatter
    file_handler = logging.FileHandler(log_path)
    file_handler.setFormatter(formatter)

    # Add handlers only if they haven't been added already
    if not logger.handlers:
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    return logger 
