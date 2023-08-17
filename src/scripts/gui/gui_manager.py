import sys
# TODO:
#          REQUIREMENTS:
#                       IMPORTS
#          SYSTEM:
#                       GUI MANAGER
#                       app LOGGER
#                       BKG # AZURE INTERFACE
#                       DATE & TIME PICKER [time-dimmed]
#


########################################################################################################################
### REQUIREMENTS #######################################################################################################
########################################################################################################################
########################################################################################################################
########## IMPORTS #####################################################################################################
import tkinter as tk
from tkinter import messagebox
from tkinter.ttk import Progressbar
from tkcalendar import DateEntry, Calendar

import threading
import time
from src.scripts.system.config import DMD, DMDD
# from src.scripts.system import config

########################################################################################################################
########## GUI MANAGER #################################################################################################

class WindowManager:
    """""
    WindowManager Class: This class acts as a manager for all the windows in your application.
    It keeps a dictionary of window objects and provides methods to show, hide, close, and manipulate them
    """
    def __init__(self, root):
        self.windows = {}
        self.root = root
        self.current_process = None  # No process is running initially
    def create_window(self, window_class, relation=None):
        name = window_class.__name__                        # Get the class name
        window = window_class(self.root, self, relation)    # Pass the manager as an argument
        window.withdraw()
        window.protocol("WM_DELETE_WINDOW", window.on_close)
        self.windows[name] = window
        return window
    def show_window(self, name):
        for window_name, window in self.windows.items():
            if window_name == name:
                window.deiconify()
            else:
                window.withdraw()
        self.root.withdraw()
    def show_window_sa(self, name):
        for window_name, window in self.windows.items():
            if window_name == name:
                window.deiconify()
    def hide_window(self, name):
        self.windows[name].withdraw()
        if all(window.winfo_viewable() == 0 for window in self.windows.values()):
            self.root.deiconify()
    def close_window(self, name):
        for window_name, window in self.windows.items():
            if window_name == name:
                window.destroy()
            else:
                window.withdraw()
        self.root.deiconify()
    def show_all(self):
        for window in self.windows.values():
            window.deiconify()
    def hide_all(self):
        for window in self.windows.values():
            window.withdraw()

class PopupWindow(tk.Toplevel):
    def __init__(self, root, message, title, meth_type=0):
        super().__init__(root)
        self.title(title)
        self.protocol('WM_DELETE_WINDOW', self.on_close_window)  # Define what should happen when 'X' is clicked

        if meth_type == 0:
            tk.messagebox.showerror(title, message)  # Open the main error pop-up - Exit immediately.
        elif meth_type == 1:
            tk.Label(self, text=message).pack()
            # Add buttons
            tk.Button(self, text="OK", command=self.on_ok_click).pack()
            # tk.Button(self, text="Retry", command=self.on_retry_click).pack()
            # tk.Button(self, text="Close", command=self.on_close_click).pack()
    def on_close_window(self):
        self.withdraw()
        return
    def on_ok_click(self):
        self.withdraw()
        return
    # def on_retry_click(self):
    #     self.withdraw()
    # def on_close_click(self):
    #     self.withdraw()

class LoadingBarWindow(tk.Toplevel):
    """
    LoadingBarWindow: This class represents a loading bar window, which can be shown while a process is running.
    It includes a method to handle the closing event and stop the current process if needed.
    """
    def __init__(self, root, manager, relation=None):
        super().__init__(root)
        self.manager = manager
        self.title("Loading...")
        self.progress = Progressbar(self, length=200, mode='indeterminate')
        self.progress.pack(pady=10)
        self.bind("<Map>", self.on_show)  # Bind the show event
    def on_close(self):
        if self.manager.current_process:
            self.manager.current_process.stop()  # Stop the current process
        self.progress.stop()  # Stop the progress bar
        self.withdraw()  # Hide the window

    def on_show(self, event):
        self.progress.stop()  # Stop the progress bar (if it's running)
        self.progress.start()  # Restart the progress bar

class Window_1(tk.Toplevel):
    def __init__(self, root, manager, relation=None):
        super().__init__(root)
        # Design & Widgets
        self.label = tk.Label(self, text="This is Window 1")
        self.label.pack()
        self.start_button = tk.Button(self, text="Start Processing", command=self.start_processing)
        self.start_button.pack()

        # Objects
        self.manager = manager
        self.relation = relation
        self.processing_done = threading.Event()  # Event to signal when processing is done
        self.stop_event = threading.Event()  # Event to signal to stop processing

    def start_processing(self):
        self.processing_done.clear()  # Clear the event
        self.stop_event.clear()  # Clear the stop event
        self.start_button.config(state='disabled')  # Disable the button
        self.manager.current_process = self  # This process is now the current process
        self.manager.show_window('LoadingBarWindow')  # Show the loading bar
        threading.Thread(target=self.processing, daemon=True).start()
    def stop(self):
        self.stop_event.set()  # Signal to stop processing
    def processing(self):
        for i in range(20):
            if self.stop_event.is_set():
                break  # If stop_event is set, break out of the loop
            self.manager.show_window_sa(self.relation)
            self.manager.windows[self.relation].update_label(f"{i}")
            time.sleep(1)  # Simulate a time-consuming task
            print(i, DMD.REF_META["LOG_DAYS_TO_DELETE"])
            i += 1
        self.on_reset()

        if self.stop_event.is_set():
            self.on_reset()
    def on_reset(self):
        i = 0
        self.processing_done.clear()  # Set the event when processing is done
        self.stop_event.clear()  # Clear the stop_event for the next process
        self.start_button.config(state='normal')  # Enable the button
        self.manager.hide_window('LoadingBarWindow')
        self.manager.windows[self.relation].update_label(f"{i}")
    def on_close(self):
        self.manager.hide_window(self.__class__.__name__)  # Use the class name as the window name
class Window_2(tk.Toplevel):
    def __init__(self, root, manager, relation=None):
        super().__init__(root)
        # Design & Widgets
        self.label = tk.Label(self, text="This is Window 2")
        self.label.pack(padx=10, pady=5)
        # Objects
        self.manager = manager
        self.relation = relation
        self.processing_done = threading.Event()  # Event to signal when processing is done
        self.stop_event = threading.Event()  # Event to signal to stop processing

    def update_label(self, text):
        self.label.config(text=text)
    def on_close(self):
        self.manager.hide_window(self.__class__.__name__)  # Use the class name as the window name
class Window_3(tk.Toplevel):
    def __init__(self, root, manager, relation=None):
        super().__init__(root)
        # Design & Widgets
        self.title("Date Selection Window")
        self.label = tk.Label(self, text="Select a date:")
        self.label.pack(padx=10, pady=5)
        # Objects
        self.manager = manager
        self.relation = relation
        self.selected_date = tk.StringVar()
        ## DateEntry widget
        self.date_entry = DateEntry(self, width=40, date_pattern='Y-m-d')
        self.date_entry.pack(padx=15, pady=10)
        self.date_entry.bind("<FocusOut>", self.update_calendar)  # Bind event to update calendar
        ## Calendar widget
        self.calendar = Calendar(self, selectmode="day")
        self.calendar.pack(padx=15, pady=10)
        self.calendar.bind("<<CalendarSelected>>", self.update_date_entry)  # Bind event to update date entry
        ## Buttons
        self.confirm_butt = tk.Button(self, text="Confirm", command=self.confirm_date)
        self.confirm_butt.pack(padx=10, pady=5)

    def confirm_date(self):
        self.selected_date = self.calendar.selection_get()

        print(f"Selected date: {self.selected_date}")
    def update_date_entry(self, event):
        selected_date = self.calendar.selection_get()
        self.date_entry.set_date(selected_date)
    def update_calendar(self, event):
        selected_date = self.date_entry.get_date()
        self.calendar.selection_set(selected_date)
    def on_close(self):
        self.manager.hide_window(self.__class__.__name__)  # Use the class name as the window name
def func_main_window_creator(manager, root):
    width = 300; high = 200
    root.geometry(f"{width}x{high}")
    # TODO: Sub-windows Creation
    button1wind = manager.create_window(Window_1, relation='Window_2')
    button2wind = manager.create_window(Window_2, relation=None)
    button3wind = manager.create_window(Window_3, relation=None)
    LoadingBarWindow_wind = manager.create_window(LoadingBarWindow)

    BUTTONS_LIST = [Window_1, Window_2, Window_3]
    for window_class in BUTTONS_LIST:
        window_name = window_class.__name__
        tk.Button(root, text=f"Show {window_name}", command=lambda name=window_name: manager.show_window(name)).pack()

def check_processing_done(manager, root):
    """
    Process Management: You have implemented threading to run processes in the background,
    along with events to signal when processing is done or stopped.
    The WindowManager class keeps track of the current process,
    and a separate function (check_processing_done) is used to monitor the processing status.
    :return:
    """
    if manager.current_process is not None:
        if manager.current_process.processing_done.is_set() and not manager.current_process.stop_event.is_set():
            print( manager.current_process)
            print("Processing is done!")
            manager.current_process.processing_done.clear()
            root.after(1000, lambda: check_processing_done(manager, root))
        elif manager.current_process.stop_event.is_set():
            print(manager.current_process)
            print("Processing Stopped by the user!")
            manager.current_process.processing_done.clear()
            root.after(1000, lambda: check_processing_done(manager, root))
        else:
            # Check again in 1 second
            root.after(1000, lambda: check_processing_done(manager, root))
    else:
        # If there is no current process, check again in 1 second
        root.after(1000, lambda: check_processing_done(manager, root))
        # root.after(1000, check_processing_done(manager, root))
def main_func():
    for x in range(10):
        print("daniel1")
        print(DMDD["LOG_DAYS_TO_DELETE"])
        DMD.set_attribute("LOG_DAYS_TO_DELETE", DMDD["LOG_DAYS_TO_DELETE"]+x)
        print(DMDD["LOG_DAYS_TO_DELETE"])
        time.sleep(1)

def main_func2():
    for x in range(100):
        print("daniel2")
        time.sleep(1)
'''
###########################################    MAIN HERE     ########################################################### 
'''
def main_gui_start():
    root = tk.Tk()
    manager = WindowManager(root)
    func_main_window_creator(manager, root)
    root.protocol("WM_DELETE_WINDOW", root.destroy) 

    # Start checking
    # threading.Thread(target=check_processing_done(manager=manager, root=root), daemon=True).start()
    tr_check_processing_done = threading.Thread(target=check_processing_done, args=(manager, root), daemon=True)
    tr_check_processing_done.start()

    # check_processing_done()
    t1 = threading.Thread(target=main_func, daemon=True)
    t1.start()
    root.mainloop()



###########################################    START HERE     ##########################################################
# main_gui_start()
# t2= threading.Thread(target=main_func2, daemon=True)
# t2.start()
# main_gui_start()
#ref#
# manager.show_window("Window 3")
