import logging
import urllib3
from urllib3.exceptions import InsecureRequestWarning

logger = logging.getLogger()
urllib3.disable_warnings(InsecureRequestWarning)

if not logger.hasHandlers():
    logger.setLevel(logging.DEBUG)

logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("filelock").setLevel(logging.WARNING)
