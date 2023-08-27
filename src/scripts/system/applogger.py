from src.scripts.system.config import DMD
from datetime import datetime as dt
import logging
import os
########################################################################################################################
########## Logger ######################################################################################################
def func_remove_symbols(input_string):
    return ''.join(char.lower() for char in input_string if char.isalnum())
class CustomFormatter(logging.Formatter):
    def format(self, record):
        record.asctime = self.formatTime(record, self.datefmt)
        record.message = record.getMessage()
        record.message = record.message.replace(',', '').replace('"', '""')
        record.location = f"{record.filename}:{record.lineno}"
        s = '"%(asctime)s", "%(levelname)s", "%(location)s", "%(message)s"' % record.__dict__
        return s
def func_main_logger():
    if not os.path.exists(DMD.LOCAL_METADATA["LOG_PATH_FULL"]):
        os.makedirs(DMD.LOCAL_METADATA["LOG_PATH_FULL"])
    logger_name = f'{DMD.LOCAL_METADATA["LOG_PATH_FULL"]}\\{DMD.LOCAL_METADATA["LOG_PREFIX"]}{DMD.LOCAL_METADATA["LOCAL_MACHINE"]}__{dt.now().strftime(DMD.LOCAL_METADATA["LOG_YYYY_MM_DD__HH_MM"])}'
    formatter = CustomFormatter()                                                                                       # define a logging format
    myLogger = logging.getLogger(logger_name)                                                                           # Set up the myLogger
    myLogger.setLevel(logging.DEBUG)
    handler = logging.FileHandler(f'{logger_name}.csv')                                                                 # Create a file handler
    handler.setLevel(logging.NOTSET)                                                                                    # Define Handler level
    handler.setFormatter(formatter)
    myLogger.addHandler(handler)                                                                                        # Add the handlers to the myLogger
    return myLogger
APPLOGGER = func_main_logger()
