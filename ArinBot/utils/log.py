import logging

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s', 
    handlers=[logging.FileHandler("log.txt"), logging.StreamHandler()],
    level=logging.INFO
    )

logger = logging.getLogger(__name__)
