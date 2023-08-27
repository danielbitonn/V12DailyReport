# TODO: 2023-08-23
#       TRY & EXCEPT Implementation
#       SUPPORTER GUI & Functionality
#                                   * Open supporter GUI & Loading Animation                                            DONE
#                                   * Design widgets and text size (relatively - not manually)                          DONE & ON-GOING
#                                   * Background - Downloading Data                                                     WIP
#                                   * Background - Data Exploration                                                     WIP
#                                   * User inputs handling                                                              WIP (VALIDATION)
#                                   * Create graphs & widgets (Using HTML as a structure for outputs)                   NEXT
#                                   * Implement graphs & widgets (Using HTML as a structure for outputs)                NEXT
#       Press-PC GUI & Functionality
#                                   * Open PRESS_PC GUI & Loading Animation                                             NEXT
#                                   * Press exExporter logics issue
### Internal Imports ###
from src.scripts.system.applogger import APPLOGGER
from src.scripts.system.config import DMD, azure_initialization
from src.scripts.gui.windows.win_utility import SHARE_DATA, WindowManager, register_thread, check_queue
from src.scripts.gui.windows.win_1 import Window_1
from src.scripts.gui.windows.win_2 import Window_2
from src.scripts.gui.windows.win_3 import Window_3
from src.scripts.gui.windows.win_4 import Window_4
from src.scripts.gui.windows.win_supporter import Window_SUPPORTER
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
def daniel(_val=None, _name=None, level=1):
    """level [0 == the current func, 1 == the previous func (default), 2 == the previous previous func, ...., -1 == the root func]"""
    p = f'{_name}:{_val} # File:{inspect.getouterframes(inspect.currentframe())[level].filename} # Line:{inspect.getouterframes(inspect.currentframe())[level].lineno}'
    print("############################################################################################################")
    print(p)
    return p
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
    pre_req_tr.tr.join()
    daniel(pre_req_tr.tr_name, "pre_req_tr.tr_name")
    manager.register_window(Window_SUPPORTER, shared_data=SHARE_DATA, extra_width=1, extra_height=1)                    # passing the shared data object and extra width&height
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
    ### Start the RECURRING check ###
    root.after(SHARE_DATA.CHECK_QUEUE_FREQ, check_queue)
    # # TODO: background SUPPORTER GUI building and withdraw()
    tr_background_SUPPORTER = threading.Thread(name="background_SUPPORTER", target=background_SUPPORTER, args=(manager, SHARE_DATA.THREADS_DICT["azure_initialization_thread"]), daemon=True)
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
    SHARE_DATA.WINDOWS_CLASSES["Window_SUPPORTER"] = Window_SUPPORTER
    # Automatically open Window_4
    manager.show_window("Window_4")
    ### Start root_window_definition subprocess ###
    root_window_definition(root, 100, 100)
    ### Start Main Loop ###
    root.mainloop()
