# TODO:
#  ################################################## Program Design ###################################################
#          REQUIREMENTS:
#                       IMPORTS
#          SYSTEM:
#                       GUI MANAGER
#                       app LOGGER
#                       BKG # AZURE INTERFACE
#                       DATE & TIME PICKER [time-dimmed]
#  #####################################################################################################################
### General Imports ###
# from termcolor import colored
# import colorama
# colorama.init()

_temp = False
if _temp:
    from temp import *

import os
import sys
import threading
import time
import traceback
import inspect
### EXTERNAL IMPORT ###
from src.scripts.system.config import azure_initialization, DMD, files_n_folders, old_logs_deletion_files_automation
from src.scripts.system.applogger import APPLOGGER
from src.scripts.gui.windows.win_utility import SHARE_DATA, register_thread, background_thread_checker
from src.scripts.gui.gui_handling_system import MAIN_GUI_HANDLING_SYS                                                   # from src.scripts.gui.gui_manager import main_gui_start
###### WEB GUI
from src.scripts.gui.web_gui import start_web_server, get_default_browser_windows, terminate_process_by_port, should_shutdown, ACT
import requests
def logger_explain_template(func=None, err=None):
    return f'The <{func}> has been failed! ### Error: <{err}> ### {sys.exc_info()[0]} >>> {sys.exc_info()[1]} >>> {traceback.extract_tb(list(sys.exc_info())[2])} ###'
def is_browser_open(driver):
    _ = {inspect.currentframe().f_code.co_name}
    try:
        driver.current_window_handle
        return True
    except Exception as e:
        APPLOGGER.error(f'{logger_explain_template(func=_, err=e)}')
        return False
def monitor_browser(driver, should_shutdown):
    while True:
        time.sleep(1)
        if not is_browser_open(driver):
            print("Browser window was closed by the user.")
            should_shutdown = True
            requests.post(f'http://127.0.0.1:{ACT["PORT"]}/shutdown_check')                                             # Shut down the server
            if driver:
                driver.quit()                                                                                           # Close the browser
            break
########################################################################################################################
########################################################################################################################
########################################################################################################################
if __name__ == '__main__':
    if not _temp:
        print("\033[94mThis is blue text!\033[0m")
        print("\033[41mThis is red background!\033[0m")
        print("\033[92mThis is green text with \033[45ma magenta background\033[0m!")
        st = time.time()
        threading.Thread(target=files_n_folders, daemon=True).start()
        threading.Thread(target=old_logs_deletion_files_automation, daemon=True).start()
        ### Start the background checker in a separate thread ###
        checker_thread = threading.Thread(target=background_thread_checker, daemon=True)
        checker_thread.start()
        ### Start azure_initialization subprocess from config.py ###
        azure_initialization_thread = threading.Thread(name="azure_initialization_thread", target=azure_initialization, args=(APPLOGGER, SHARE_DATA), daemon=True)
        azure_initialization_thread.start()
        register_thread(azure_initialization_thread)

        if ACT['WEB_GUI_FLAG']:
            try:
                result = terminate_process_by_port(ACT["PORT"])
                APPLOGGER.info(f'The <terminate_process_by_port> function is done! # <{result}> #')
            except Exception as e:
                APPLOGGER.error(f'{logger_explain_template(func=__name__, err=e)}')

            web_server_thread = threading.Thread(target=start_web_server, args=(ACT["PORT"],), daemon=True)                 # TODO: web_gui execution
            web_server_thread.start()
            driver = get_default_browser_windows()                                                                          # TODO: open browser
            APPLOGGER.info(f'Web started by <start_web_server()>')
            driver.get(f'http://127.0.0.1:{ACT["PORT"]}')
            APPLOGGER.info(f'Web started by <start_web_server()>')

            monitor_thread = threading.Thread(target=monitor_browser, args=(driver, should_shutdown), daemon=True)
            monitor_thread.start()
        ################################################################################################################
        ################################################## Main GUI ####################################################
        ################################################################################################################
        MAIN_GUI_HANDLING_SYS()                                                                                         # main_gui_start()
        ################################################################################################################
        ################################################################################################################
        ################################################################################################################
        if ACT['WEB_GUI_FLAG']:
            requests.post(f'http://127.0.0.1:{ACT["PORT"]}/shutdown_check')                                                 # Shut down the server
            try:
                driver.quit()                                                                                               # Close the browser
            except Exception as e:
                APPLOGGER.error(f'{logger_explain_template(func="Close_browser", err=e)}')
        print("END")
