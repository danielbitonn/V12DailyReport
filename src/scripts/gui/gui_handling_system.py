# TODO: 2023-08-17
#       TRY & EXCEPT Implementation
#       SUPPORTER GUI & Functionality
#                                   * Open supporter GUI & Loading Animation
#                                   * Background - Downloading Data
#                                   * Background - Data Exploration
#                                   * User inputs
#                                   * Create graphs & widgets
#                                   * Implement graphs & widgets
#                                   * Design widgets and text size (relatively - not manually)
#       Press-PC GUI & Functionality
#                                   * Open supporter GUI & Loading Animation
#       Remove prints & todos debugging notes
########################################################################################################################
########################################################################################################################
########################################################################################################################
### Internal Imports ###
from src.scripts.system.applogger import APPLOGGER
from src.scripts.system.config import azure_initialization
from src.scripts.gui.windows.win_utility import SHARE_DATA, WindowManager, register_thread, background_thread_checker, check_queue
from src.scripts.gui.windows.win_1 import Window_1
from src.scripts.gui.windows.win_2 import Window_2
from src.scripts.gui.windows.win_3 import Window_3
from src.scripts.gui.windows.win_4 import Window_4
from src.scripts.gui.windows.win_supporter import Window_Supporter
### External Imports ###
import threading
import time
import inspect
import sys
import traceback
import tkinter as tk
########################################################################################################################
########################################################################################################################
########################################################################################################################
def logger_explain_template(func=None, err=None):                                                                       # func # _ = {inspect.currentframe().f_code.co_name}
    return f'The <{func}> has been failed! ### Error: <{err}> ### {sys.exc_info()[0]} >>> {sys.exc_info()[1]} >>> {traceback.extract_tb(list(sys.exc_info())[2])} ###'                                                                                         # Sleep for a short duration before checking again
def root_window_definition(root, extra_width=0, extra_height=0):
    APPLOGGER.info(f'The <{inspect.currentframe().f_code.co_name}> has been activated.')
    root.attributes('-alpha', 1.0)                                                                                      # This will make the root window fully opaque
    root.protocol("WM_DELETE_WINDOW", root.destroy)
    root.update_idletasks()                                                                                             # Get the current width and height of the root window
    width = root.winfo_width() + extra_width
    height = root.winfo_height() + extra_height
    root.geometry(f"{width}x{height}")                                                                                  # Set the new size
    root.withdraw()
def background_SUPPORTER(manager, pre_req_tr):
    pre_req_tr.join()
    while SHARE_DATA.DICT_SHIFT_OPTIONS is None or SHARE_DATA.DICT_PRESS_STATUS_OPTIONS_n_COLORS is None:
        time.sleep(1)
    manager.register_window(Window_Supporter, shared_data=SHARE_DATA, extra_width=1, extra_height=1)                            # passing the shared data object and extra width&height
def background_PRESS(manager):
    for x in range(100):
        print(x+100)
        time.sleep(5)
def MAIN_GUI_HANDLING_SYS():
    root = tk.Tk()
    root.name = "root_window"
    root.attributes('-alpha', 0.0)                                                                                      # This will make the root window fully transparent
    manager = WindowManager(root)                                                                                       # Define the Manager for the root
    manager.window_history.append(root.name)
    SHARE_DATA.MANAGER = manager
    SHARE_DATA.ROOT = root

    root.after(SHARE_DATA.CHECK_QUEUE_FREQ, check_queue)                                                                # Start the RECURRING check

    ### Start the background checker in a separate thread ###
    checker_thread = threading.Thread(target=background_thread_checker, daemon=True)
    checker_thread.start()
    ### Start azure_initialization subprocess from config.py ###
    azure_initialization_thread = threading.Thread(name="azure_initialization_thread", target=azure_initialization, args=(APPLOGGER, SHARE_DATA), daemon=True)
    azure_initialization_thread.start()
    register_thread(azure_initialization_thread)

    # # TODO: background SUPPORTER GUI building and withdraw()
    tr_background_SUPPORTER = threading.Thread(name="background_SUPPORTER", target=background_SUPPORTER, args=(manager, azure_initialization_thread))
    tr_background_SUPPORTER.start()
    register_thread(tr_background_SUPPORTER)

    # TODO: background Press-PC GUI building and withdraw()
    tr_background_PRESS = threading.Thread(name="background_PRESS", target=background_PRESS, args=(manager,), daemon=True)
    tr_background_PRESS.start()
    register_thread(tr_background_PRESS)

    ## Register windows
    manager.register_window(Window_1, shared_data=SHARE_DATA, extra_width=50, extra_height=100)                         # passing the shared data object and extra width&height
    manager.register_window(Window_2, shared_data=SHARE_DATA, extra_width=20, extra_height=10)                          # passing the shared data object and extra width&height
    manager.register_window(Window_3, shared_data=SHARE_DATA, extra_width=100, extra_height=100)                        # passing the shared data object and extra width&height
    manager.register_window(Window_4, shared_data=SHARE_DATA, extra_width=1, extra_height=1)                            # passing the shared data object and extra width&height

    # manager.register_window(Window_Supporter, shared_data=SHARE_DATA, extra_width=100, extra_height=100)  # adjust extra_width and extra_height as needed

    # manager.register_window(Window_5, shared_data=SHARE_DATA, extra_width=1, extra_height=1)                            # passing the shared data object and extra width&height
    # SHARE_DATA.WINDOWS_CLASSES["Window_5"] = Window_5
    SHARE_DATA.WINDOWS_CLASSES["Window_Supporter"] = Window_Supporter




    # Automatically open Window_4
    manager.show_window("Window_4")
    ### Start root_window_definition subprocess ###
    root_window_definition(root, 100, 100)                                                                              # tr_root_window_definition = threading.Thread(name="tr_root_window_definition", target=root_window_definition, args=(root, 100, 100), daemon=True) # tr_root_window_definition.start() # register_thread(tr_root_window_definition)
    ### Start Main Loop ###
    root.mainloop()
