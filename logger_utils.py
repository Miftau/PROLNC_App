# logger_utils.py
import logging
from datetime import datetime

logging.basicConfig(
    filename='chat_logs.txt',
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
)

def log_message(message: str):
    logging.info(message)
