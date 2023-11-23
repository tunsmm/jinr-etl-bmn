import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

log_file = "monitoring.log"

file_handler = logging.FileHandler(log_file)
file_handler.setLevel(logging.INFO)

formatter = logging.Formatter(
    fmt='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)
