from datetime import datetime as dt
import logging
import os
from src.scripts.system.config import DMDD
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
# def auto_func_delete_old_files(directory, days):
#     cutoff = dt.now() - td(days=days)
#     log_files = glob.glob(f"{directory}\\{DMDD['LOG_PREFIX']}*")
#     try:
#         for log_file in log_files:
#             date_str = log_file.split('__')[2]                                                                          # Extract date from filename
#             file_date = dt.strptime(date_str, DMDD['DT_FORMAT'])
#             if file_date < cutoff:                                                                                      # If file is older than X days, delete it
#                 os.remove(log_file)
#                 deleted_logs.append(log_file)
#         return deleted_logs
#     except:
#         print(f'No files to delete: {deleted_logs}')
#         1*1
#         return []
def func_main_logger():
    local_machine = DMDD["LOCAL_MACHINE"]
    if not os.path.exists(DMDD["LOG_PATH_FULL"]):
        os.makedirs(DMDD["LOG_PATH_FULL"])
    # else:
        # deleted_log_files = auto_func_delete_old_files(directory=DMDD["LOG_PATH_FULL"], days=DMDD["LOG_DAYS_TO_DELETE"])
    logger_name = f'{DMDD["LOG_PATH_FULL"]}\\{DMDD["LOG_PREFIX"]}{local_machine}__{dt.now().strftime(DMDD["LOG_YYYY_MM_DD__HH_MM"])}'
    formatter = CustomFormatter()                                                                                       # define a logging format
    myLogger = logging.getLogger(logger_name)                                                                           # Set up the myLogger
    myLogger.setLevel(logging.DEBUG)
    handler = logging.FileHandler(f'{logger_name}.csv')                                                                 # Create a file handler
    handler.setLevel(logging.NOTSET)                                                                                    # Define Handler level
    handler.setFormatter(formatter)
    myLogger.addHandler(handler)                                                                                        # Add the handlers to the myLogger
    # if len(deleted_logs) > 0:
    #     myLogger.debug(f"Debugging Actions: the following logs files were deleted >>> {deleted_logs}")
    return myLogger

APPLOGGER = func_main_logger()
