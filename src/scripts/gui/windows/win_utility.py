from src.scripts.system.applogger import APPLOGGER
import threading
import queue
import time
import inspect
import sys
import traceback
from PIL import Image, ImageTk
import tkinter as tk
from tkinter.ttk import Progressbar
from src.scripts.system.config import DMDD, DMD, azure_initialization, colors_dict_to_tuples
from tkinter import messagebox                                                                                          # messagebox.showerror(title="Error", message=f'Processing step {i}')
# from tkcalendar import DateEntry, Calendar
# import datetime
# import os
# import json

PAUSE_ALL_THREADS_EVENT = threading.Event()
PAUSE_CONDITION = threading.Condition()
def logger_explain_template(func=None, err=None):
    return f'The <{func}> has been failed! ### Error: <{err}> ### {sys.exc_info()[0]} >>> {sys.exc_info()[1]} >>> {traceback.extract_tb(list(sys.exc_info())[2])} ###'
def check_queue():
    while not SHARE_DATA.TASK_QUEUE.empty():
        # if SHARE_DATA.PAUSE_ALL_THREADS_EVENT.is_set():
        #     while SHARE_DATA.ERROR_MESSAGE_FLAG == "ok":
        #         time.sleep(1)  # Sleep until the event is cleared
        #     SHARE_DATA.ERROR_MESSAGE_FLAG = ""
        #     continue
        try:
            task, origin = SHARE_DATA.TASK_QUEUE.get()
        except:
            origin = "unknown"
            task = SHARE_DATA.TASK_QUEUE.get()
        res = task()                                                                                                    # Execute the task
        SHARE_DATA.TASK_RESULT[origin] = res
        print(SHARE_DATA.TASK_RESULT[origin])
    SHARE_DATA.ROOT.after(SHARE_DATA.CHECK_QUEUE_FREQ, check_queue)                                                     # Check the queue again after 100ms
def register_thread(thread):
    outer_frame   = inspect.getouterframes(inspect.currentframe())
    creation_file = outer_frame[1].filename
    creation_line = outer_frame[1].lineno
    print(f'{thread} # {creation_file} # {creation_line}')
    with SHARE_DATA.THREADS_LIST_LOCK:
        SHARE_DATA.THREADS_LIST.append(thread)
        SHARE_DATA.THREADS_LIST_n_LOCATIONS[thread.name] = f'{thread} # {creation_file} # {creation_line}'
def handle_thread_completion(thread, st):                                                                               # Custom logic for handling thread completion
    if thread.name=="tr_root_window_definition":
        pass
    elif thread.name=="azure_initialization_thread":                                                                    # Updating From Azure Data
        # TODO: verify if the Azure connection Succeed or we are locally >>>> If Locally treat the SHARE_DATA.MANAGER.windows["Window_4"].update_press_sn_dropdown(SHARE_DATA.PRESS_SN)
        SHARE_DATA.PRESS_SN.extend(list(SHARE_DATA.CONFIG["conf.json"]["presses"]))
        SHARE_DATA.DICT_PRESS_STATUS_OPTIONS_n_COLORS = colors_dict_to_tuples(SHARE_DATA.CONFIG["conf.json"]["design"]["press_status_colors"])
        SHARE_DATA.DICT_SHIFT_OPTIONS = tuple(SHARE_DATA.CONFIG["conf.json"]["design"]["shift_options"].keys())
        SHARE_DATA.MANAGER.windows["Window_4"].update_press_sn_dropdown(SHARE_DATA.PRESS_SN)                            # updating dropdown list when the thread is done
        # SHARE_DATA.MANAGER.register_window(SHARE_DATA.WINDOWS_CLASSES["Window_Supporter"], shared_data=SHARE_DATA, extra_width=1, extra_height=1)  # passing the shared data object and extra width&height
        if DMDD["METADATA_FLAG"]:
            try:
                SHARE_DATA.PRESS_LIST_OF_BLOBS = SHARE_DATA.METADATA[DMDD["PRESS_DICT_SN"]]
            except Exception as e:
                # TODO USING OPEN JSON FUNC FROM OLDER VERSION - Remember to update (SHARE_DATA.MANAGER.windows["Window_4"].update_press_sn_dropdown(SHARE_DATA.PRESS_SN))!
                APPLOGGER.error(logger_explain_template(func={inspect.currentframe().f_code.co_name}, err=e))
    elif thread.name=="background_tasks_window_5":
        try:
            SHARE_DATA.MANAGER.windows["Window_Supporter"].stop_loading_animation()
        except Exception as e:
            # TODO: Error handling system regarding missing rowData!
            APPLOGGER.error(logger_explain_template(func={inspect.currentframe().f_code.co_name}, err=e))
    else:
        pass
    print(f"Thread {thread.name} has completed # Duration {time.time() - st}")
    APPLOGGER.debug(f"Thread {thread.name} has completed # Duration {time.time() - st}")
    return None
def background_thread_checker():
    st = time.time()
    while True:
        with SHARE_DATA.THREADS_LIST_LOCK:
            print(SHARE_DATA.THREADS_LIST)
            APPLOGGER.debug(f"Threads <{SHARE_DATA.THREADS_LIST}> are running.")
            for thread in SHARE_DATA.THREADS_LIST:
                if not thread.is_alive():
                    handle_thread_completion(thread, st)                                                                # Handle thread completion (e.g., fetch results, perform cleanup)
                    SHARE_DATA.THREADS_LIST.remove(thread)
        time.sleep(1)
class SharedData:
    def __init__(self):
        self.some_attribute = 0
        ### power-up variables ###
        self.TASK_QUEUE = queue.Queue()
        self.PRESS_SN = ["Choose Press Serial Number"]
        self.PRESS = None
        self.ROOT  = None
        self.MANAGER = None
        self.MAINAGENT = None
        self.AZURECONNECT = None
        self.METADATA = None
        self.CONFIG = None                                                                                              # This is the whole configuration azure SHARE_DATA.CONFIG["conf.json"]["presses"] or SHARE_DATA.CONFIG[""]["presses"]!
        self.CHECK_QUEUE_FREQ = DMDD["CHECK_QUEUE_FREQ"]
        self.TASK_RESULT = {}
        self.THREADS_LIST = []
        self.THREADS_LIST_n_LOCATIONS = {}
        self.THREADS_LIST_LOCK = threading.Lock()
        ### runtime variables ###
        self.PAUSE_ALL_THREADS_EVENT = threading.Event()
        self.WINDOWS_CLASSES = {}
        self.PRESS_LIST_OF_BLOBS = None
        self.DICT_PRESS_STATUS_OPTIONS_n_COLORS = None
        self.DICT_SHIFT_OPTIONS = None
        self.START_DATE = None
        self.START_TIME = None
        self.END_DATE = None
        self.END_TIME = None
        self.ERROR_MESSAGE_FLAG = ""
    def update_attribute(self, value):
        with self.THREADS_LIST_LOCK:
            self.some_attribute = value
    def get_attribute(self):
        with self.THREADS_LIST_LOCK:
            return self.some_attribute

SHARE_DATA = SharedData()
class ToolTip(object):
    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.text = None
        self.x = self.y = 0
    def showtip(self, text):                                                                                            # Display text in tooltip window
        self.text = text
        if self.tipwindow or not self.text:
            return
        x, y, _, _ = self.widget.bbox("insert")                                                                         # Get location of the widget as a reference
        x = x + self.widget.winfo_rootx() - 10
        y = y + self.widget.winfo_rooty() - 10
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(tw, text=self.text, justify=tk.LEFT, background="#e0efff", relief=tk.SOLID, borderwidth=1, font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)
    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()
def create_tooltip(widget, text):
    tool_tip = ToolTip(widget)
    def enter(event):
        tool_tip.showtip(text)
    def leave(event):
        tool_tip.hidetip()
    widget.bind('<Enter>', enter)
    widget.bind('<Leave>', leave)
class LoadingBarWindow(tk.Toplevel):                                                                                    # LoadingBarWindow: This class represents a loading bar window, which can be shown while a process is running. It includes a method to handle the closing event and stop the current process if needed.
    def __init__(self, root, manager, stop_function=None):
        super().__init__(root)
        self.manager = manager
        self.stop_function = stop_function
        self.T = "Loading..."
        self.title(self.T)
        self.progress = Progressbar(self, length=200, mode='indeterminate')
        self.progress.pack(pady=10)
        self.bind("<Map>", self.on_show)                                                                                # Bind the show event
        self.protocol('WM_DELETE_WINDOW', self.on_close)                                                                # Override close behavior
        APPLOGGER.info(f'The <{self.T}> which is created based on (tk.TopLevel)')
    def on_close(self):
        if self.stop_function:
            self.stop_function()                                                                                        # Stop the current process
        self.progress.stop()                                                                                            # Stop the progress bar
        self.withdraw()                                                                                                 # Hide the window
        APPLOGGER.info(f'<{self.T}> closed!')
    def on_show(self, event):
        self.progress.stop()                                                                                            # Stop the progress bar (if it's running)
        self.progress.start()                                                                                           # Restart the progress bar
        APPLOGGER.info(f'<{self.T}> show-up!')
class WindowManager:                                                                                                    # Factory or Registry Pattern Create a factory or registry class to manage window creation dynamically
    def __init__(self, root):
        self.windows = {}
        self.root = root
        self.window_history = []                                                                                        # Stack to keep track of window history.
        self.last_window = root.name
        APPLOGGER.info(f'The <{inspect.currentframe().f_code.co_name}> of <WindowManager CLASS> has been created.')
    def open_loading_bar(self, stop_function=None):
        return LoadingBarWindow(self.root, self, stop_function)
    def register_window(self, window_class, shared_data=None, relation=None, extra_width=0, extra_height=0):
        window = window_class(self.root, self, shared_data, relation, extra_width, extra_height)
        window.withdraw()
        name = window.T
        print(name)
        self.windows[name] = window
        button = window_class.create_activation_button(self.root, lambda: self.show_window(name))                       # Create and pack the activation button for this window
        button.pack()
        APPLOGGER.info(f'The <{name}> has been registered [window:<{window}>]. with his activate button <{button}>.')
    def show_window(self, name):
        if name != "root_window":
            self.windows[name].show()
            # self.windows[name].update_idletasks()                                                                     # Update layout calculations
            self.windows[name].adjust_size(self.windows[name].extra_width, self.windows[name].extra_height)             # Adjust the window size
            self.root.withdraw()
        else:
            self.root.deiconify()
            self.root.update_idletasks()
        self.windows_history_update(current_window_name=name)
        APPLOGGER.info(f'Window <{name}> has been show-up.')
    def windows_history_update(self, current_window_name):
        print(f"Last: {self.last_window}")
        print(f"Current: {current_window_name}")
        if current_window_name != self.window_history[-1]:
            self.window_history.append(current_window_name)
        self.last_window = current_window_name
        print(f"Last: {self.last_window}")
        print(f"Windows History: {self.window_history}")
        APPLOGGER.info(f'Windows History: <{self.window_history}>')
    def hide_window(self, name):
        self.windows[name].hide()
    def close_window(self, current_window_name):
        self.hide_window(current_window_name)
        if self.window_history:
            previous_window_name = self.window_history[-2] if self.window_history else "root_window"
            self.show_window(previous_window_name)
            APPLOGGER.info(f'The <{current_window_name}> window has been closed. The <{previous_window_name}> has show-up.')
        else:
            self.root.deiconify()
            APPLOGGER.info(f'The <{current_window_name}> window has been closed. The <{self.root}> has show-up.')
    def close_and_return_to_root(self, name):
        window = self.windows.pop(name, None)
        if window:
            window.destroy()
        self.root.deiconify()                                                                                           # Show the root window
    def show_all(self):
        for window in self.windows.values():
            window.show()
    def hide_all(self):
        for window in self.windows.values():
            window.hide()
    def show_related_window(self, current_window_name, related_window_name):
        current_window = self.windows[current_window_name]
        related_window = self.windows[related_window_name]
        current_window.hide()                                                                                           # Logic to manage the relationship between windows, e.g., close one, open another, etc.
        related_window.show()                                                                                           # Logic to manage the relationship between windows, e.g., close one, open another, etc.
        APPLOGGER.info(f'Window <{current_window_name}> hide and window <{related_window_name}> show-up.')
class BaseWindow(tk.Toplevel):                                                                                          # Create a base class that will contain common functionalities like closing, showing, hiding, etc.
    def __init__(self, root, manager, shared_data=None, relation=None, extra_width=0, extra_height=0, adjust_size=True):
        super().__init__(root)
        self.root = root                                                                                                # Explicitly set the root attribute
        self.withdraw()
        self.manager = manager
        self.shared_data = shared_data
        self.relation = relation
        self.protocol('WM_DELETE_WINDOW', self.on_close)
        if adjust_size:
            self.adjust_size(extra_width, extra_height)
        APPLOGGER.info(f'The BaseWindow class has been created.')
    @classmethod
    def create_image_button(cls, root, command, image_path):
        image = Image.open(image_path)
        photo_image = ImageTk.PhotoImage(image)
        button = tk.Button(root, image=photo_image, command=command)
        button.image = photo_image
        APPLOGGER.info(f'The image_button <{button}> has been created with the image from <{image_path}>.')
        return button
    @classmethod
    def create_text_button(cls, root, command, text):
        button = tk.Button(root, text=text, command=command)
        APPLOGGER.info(f'The <{text}> text_button <{button}> has been created with the command <{command}>.')
        return button
    @classmethod
    def create_toggle_button(cls, root, command, text):
        button = tk.Checkbutton(root, text=text, command=command)
        APPLOGGER.info(f'The <{text}> checkbox_button <{button}> has been created with the command <{command}>.')
        return button
    def adjust_size(self, extra_width=0, extra_height=0):
        self.update_idletasks()                                                                                         # Update layout calculations
        width = self.winfo_reqwidth() + extra_width
        height = self.winfo_reqheight() + extra_height
        self.geometry(f"{width}x{height}")                                                                              # Set the size
    def on_close(self):
        current_window_name = self.__class__.__name__
        self.manager.close_window(current_window_name)
    def show(self):
        self.deiconify()
    def hide(self):
        self.withdraw()
