# * ====== IMPORT ====== *
import logging
import sys

# * ====== LOGGER CREATION ====== *
def logger_initializer():   
    # doc: This function initializes the logger:
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s, %(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s",
                        datefmt='%m-%d %H:%M',
                        stream=sys.stdout)
    
    return logging.getLogger()