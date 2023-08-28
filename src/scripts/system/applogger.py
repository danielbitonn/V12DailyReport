from src.scripts.system.config import DMD
from datetime import datetime as dt
import logging
import os
########################################################################################################################
########## Logger ######################################################################################################
print_colors = {
    "text_color": {
        "Black": "\033[90m",
        "Red": "\033[91m",
        "Green": "\033[92m",
        "Yellow": "\033[93m",
        "Blue": "\033[94m",
        "Magenta": "\033[95m",
        "Cyan": "\033[96m",
        "White": "\033[97m"
    },
    "background_color": {
        "Black": "\033[40m",
        "Red": "\033[41m",
        "Green": "\033[42m",
        "Yellow": "\033[43m",
        "Blue": "\033[44m",
        "Magenta": "\033[45m",
        "Cyan": "\033[46m",
        "White": "\033[47m"
    }
    # \033[ starts the escape sequence.
    # 9Xm where X is the color code (0 to 7 for the above colors).
    # The 9 here makes the color bright. For standard (non-bright) colors, you can use 3Xm instead.
    # print("\033[94mThis is blue text!\033[0m")
    # print("\033[41mThis is red background!\033[0m")
    # print("\033[92mThis is green text with \033[45ma magenta background\033[0m!")
}
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
