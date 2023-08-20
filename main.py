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
import os
import sys
import threading
import time
import traceback
import inspect
### EXTERNAL IMPORT ###
from src.scripts.system.applogger import APPLOGGER
from src.scripts.system.config import folders_handler, auto_func_delete_old_files
from src.scripts.gui.gui_handling_system import MAIN_GUI_HANDLING_SYS                                                # from src.scripts.gui.gui_manager import main_gui_start
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
def files_n_folders():
    folders_handler(path=os.path.join('output', 'data', 'jsons'))

########################################################################################################################
########################################################################################################################
########################################################################################################################
if __name__ == '__main__':
    st = time.time()
    threading.Thread(target=files_n_folders, daemon=True).start()
    threading.Thread(target=auto_func_delete_old_files, daemon=True).start()
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
    ### Main Gui Thread ###
    MAIN_GUI_HANDLING_SYS()                                                                                          # main_gui_start()
    if ACT['WEB_GUI_FLAG']:
        requests.post(f'http://127.0.0.1:{ACT["PORT"]}/shutdown_check')                                                 # Shut down the server
        try:
            driver.quit()                                                                                               # Close the browser
        except Exception as e:
            APPLOGGER.error(f'{logger_explain_template(func="Close_browser", err=e)}')
    print("END")
