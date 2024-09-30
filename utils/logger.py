import logging
import sys

def setup_logger():
    logger = logging.getLogger('crawler')
    logger.setLevel(logging.DEBUG)  # DEBUG 레벨로 변경
    
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)  # DEBUG 레벨로 변경
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    
    logger.addHandler(handler)
    return logger