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

import threading
import time
from src.scripts.system.config import DMDD
from src.scripts.system.applogger import APPLOGGER
from src.scripts.gui.gui_manager import main_gui_start
from src.scripts.gui.web_gui import start_web_server, get_default_browser_windows,terminate_process_by_port, should_shutdown
import requests


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
            requests.post(f'http://127.0.0.1:{PORT}/shutdown_check')  # Shut down the server
            if driver:
                driver.quit()  # Close the browser
            break


PORT = 6005

if __name__ == '__main__':

    try:
        result = terminate_process_by_port(PORT)
        print(result)
    except Exception as e:
        print(e)

    # # TODO: web_gui execution
    web_server_thread = threading.Thread(target=start_web_server, args=(PORT,), daemon=True)
    web_server_thread.start()

    # TODO: open browser
    driver = get_default_browser_windows()
    driver.get(f"http://127.0.0.1:{PORT}")

    # TODO: METADATA thread
    print(f'fdsfsdf:{DMDD}')
    APPLOGGER.info(f'DONE # <read_or_write_meta_data_json()> has been completed')

    # Wait for the dtr_meta_data to be set
    # META_DATA = qtr_meta_data.get()
    # print(META_DATA)


    print("THE")
    monitor_thread = threading.Thread(target=monitor_browser, args=(driver, should_shutdown), daemon=True)
    monitor_thread.start()

    # TODO: Main Gui Thread
    main_gui_start()

    requests.post(f'http://127.0.0.1:{PORT}/shutdown_check')  # Shut down the server
    if driver:
        driver.quit()  # Close the browser
    print("END")
