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

import json
import threading
import time
### WEB GUI ###
from src.scripts.gui.web_gui import start_web_server, get_default_browser_windows, terminate_process_by_port, should_shutdown
import requests
PORT = 6005
ACT = {"web_gui": 0, }
### EXTERNAL IMPORT ###
from src.scripts.system.config import DMDD, azure_initialization
from src.scripts.system.applogger import APPLOGGER
from src.scripts.gui.gui_handling_system import main_gui_handling_system                                                # from src.scripts.gui.gui_manager import main_gui_start

# def azure_main_initialization(result_holder):
#     MAINAGENT, AZURECONNECT, METADATA, CONFIG = azure_initialization(applogger=APPLOGGER)
#     result_holder['MAINAGENT'] = MAINAGENT
#     result_holder['AZURECONNECT'] = AZURECONNECT
#     result_holder['METADATA'] = METADATA
#     result_holder['CONFIG'] = CONFIG
#     result_holder['completed'] = True
# def write_metadata_to_json(res):
#     while not res["completed"]:
#         if 'METADATA' in res:
#             with open('metadata.json', 'w') as json_file:
#                 json.dump(res['METADATA'], json_file)
# # Create a dictionary to hold the results
# result_dict = {'completed': False}

def is_browser_open(driver):
    try:
        driver.current_window_handle
        return True
    except:
        return False
def monitor_browser(driver, should_shutdown):
    while True:
        time.sleep(1)
        if not is_browser_open(driver):
            print("Browser window was closed by the user.")
            should_shutdown = True
            requests.post(f'http://127.0.0.1:{PORT}/shutdown_check')                                                    # Shut down the server
            if driver:
                driver.quit()                                                                                           # Close the browser
            break

if __name__ == '__main__':
    if ACT['web_gui']:
        try:
            result = terminate_process_by_port(PORT)
            print(result)                                                                                               # TODO: print Replacement
        except Exception as e:
            print(e)                                                                                                    # TODO: print Replacement
        web_server_thread = threading.Thread(target=start_web_server, args=(PORT,), daemon=True)                        # TODO: web_gui execution
        web_server_thread.start()
        driver = get_default_browser_windows()                                                                          # TODO: open browser
        driver.get(f"http://127.0.0.1:{PORT}")

    # azure_initialization_thread = threading.Thread(target=azure_main_initialization, args=(result_dict,), daemon=True)  # Start the azure_main_initialization subprocess
    # azure_initialization_thread.start()
    # write_metadata_thread = threading.Thread(target=write_metadata_to_json, args=(result_dict,))                        # Create a background thread to write metadata to a JSON file
    # write_metadata_thread.start()

    # print(f'Main: {DMDD}')
    APPLOGGER.info(f'DONE # <write_metadata_to_json()> has been completed')

    print("THE")

    if ACT['web_gui']:
        monitor_thread = threading.Thread(target=monitor_browser, args=(driver, should_shutdown), daemon=True)
        monitor_thread.start()

    ### Main Gui Thread ###
    main_gui_handling_system()                                                                                          # main_gui_start()
    print("END")

    if ACT['web_gui']:
        requests.post(f'http://127.0.0.1:{PORT}/shutdown_check')  # Shut down the server
        if driver:
            driver.quit()  # Close the browser



