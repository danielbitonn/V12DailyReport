from src.scripts.system.config import DMDD, DMD
from src.scripts.system.applogger import APPLOGGER
from src.scripts.gui.windows.win_utility import SHARE_DATA, BaseWindow, logger_explain_template, create_tooltip

import time
import os
import threading
import tkinter as tk
from tkinter import messagebox
class Window_1(BaseWindow):
    def __init__(self, root, manager, shared_data=None, relation=None, extra_width=0, extra_height=0):
        super().__init__(root, manager, shared_data, relation, extra_width, extra_height)
        self.T = "Window_1"
        self.title(self.T)
        self.extra_width = extra_width
        self.extra_height = extra_height
        self.loading_bar_window = None
        ### Threading events
        self.processing_done = threading.Event()
        self.stop_event = threading.Event()
        # Schedule the design of the window in a background thread
        threading.Thread(target=self.design_window, daemon=True).start()
        APPLOGGER.info(f'The <{self.T}> which is created based on (BaseWindow class) with the relations:<{relation}> and Buttons.')

    def design_window(self):
        # Finalize the design in the main thread
        time.sleep(10)
        SHARE_DATA.TASK_QUEUE.put(self.finalize_window_design)
    def finalize_window_design(self):
        ### Design & Widgets
        self.label = tk.Label(self, text="This is Window 1")
        self.label.pack()
        self.update_label_from_shared_data()                                                                            # Start the label updates
        self.start_button = tk.Button(self, text="Start Processing", command=self.start_processing)
        self.start_button.pack()
        self.open_window_2_button = tk.Button(self, text="Open Window 2", command=self.open_window_2)
        self.open_window_2_button.pack()

    @classmethod
    def create_activation_button(cls, root, command):
        image_path = os.path.join('src', 'media\\supporter.png')
        # image_path = os.path.join('..', '..', 'media\\supporter.png')
        return cls.create_image_button(root, command, image_path)
    def open_window_2(self):
        self.manager.show_window('Window_2')                                                                            # Show Window 2
        self.manager.hide_all()                                                                                         # Hide all other windows, including Window 1
        self.manager.show_window('Window_2')                                                                            # Show Window 2 again to make sure it's visible
    def update_label_from_shared_data(self):
        new_text = self.shared_data.get_attribute()
        self.label.config(text=new_text)
        self.after(200, self.update_label_from_shared_data)                                                             # Schedule this method to run again after 1 second
        APPLOGGER.info(f'The Shared data <{new_text}> has been updated.')
    def start_processing(self):
        APPLOGGER.debug(f'Starting processing...')
        self.processing_done.clear()
        self.stop_event.clear()
        self.start_button.config(state='disabled')
        self.loading_bar_window = self.manager.open_loading_bar(stop_function=self.stop_processing)
        self.loading_bar_window.deiconify()                                                                             # Show the loading bar window
        threading.Thread(target=self.processing, daemon=True).start()
    def stop_processing(self):
        APPLOGGER.debug(f'Stop processing...')
        self.stop_event.set()
        self.loading_bar_window.progress.stop()                                                                         # Stop the progress bar
        self.loading_bar_window.withdraw()                                                                              # Hide the loading bar window
    def processing(self):
        for i in range(10):                                                                                             # TODO: Example processing logic - replace with real program activation
            if self.stop_event.is_set():
                APPLOGGER.debug(f'Stop event detected, breaking the loop ### {logger_explain_template()} ###')
                break
            time.sleep(1)
            print("Processing step", i)                                                                                 # TODO: Remove Print
            messagebox.showerror(title="Error", message=f'Processing step {i}')                                         # Messagebox example.
        APPLOGGER.debug(f'Processing ended!')
        self.on_reset()
    def on_reset(self):
        self.processing_done.set()
        self.stop_event.clear()
        self.start_button.config(state='normal')
        self.loading_bar_window.on_close()                                                                              # Close the loading bar window
        APPLOGGER.info(f'<{self.T}> initialization_win_supporter.')
    def on_close(self):
        super().on_close()                                                                                              # If additional closing behavior specific to that window is necessary
        APPLOGGER.info(f'<{self.T}> closed!')                                                                           # The super().on_close() Call the base class's on_close method () from 'BaseWindow' class
