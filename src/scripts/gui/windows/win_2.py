import threading

from src.scripts.system.applogger import APPLOGGER
from src.scripts.gui.windows.win_utility import SHARE_DATA, BaseWindow

import time
import os
import tkinter as tk
class Window_2(BaseWindow):
    def __init__(self, root, manager, shared_data=None, relation=None, extra_width=0, extra_height=0):
        super().__init__(root, manager, shared_data, relation, extra_width, extra_height)
        self.T = "Window_2"
        self.title(self.T)
        self.extra_width = extra_width
        self.extra_height = extra_height

        # Schedule the design of the window in a background thread
        threading.Thread(target=self.design_window, daemon=True).start()
        APPLOGGER.info(f'The <{self.T}> which is created based on (BaseWindow class) with the relations:<{relation}> and Buttons.')
    def design_window(self):
        # Finalize the design in the main thread
        time.sleep(10)
        SHARE_DATA.TASK_QUEUE.put(self.finalize_window_design)
    def finalize_window_design(self):
        ### Design & Widgets
        self.label = tk.Label(self, text="This is Window 2")
        self.label.pack()
        self.update_button = tk.Button(self, text="Update Label", command=self.update_label_text)
        self.update_button.pack()
    @classmethod
    def create_activation_button(cls, root, command):
        image_path = os.path.join('src', 'media\\v12.png')
        # image_path = os.path.join('..', '..', 'media\\v12.png')
        return cls.create_image_button(root, command, image_path)
    def update_label_text(self):
        new_text = f"Updated at {time.strftime('%H:%M:%S')}"                                                            # Update the label text in Window 2
        self.label.config(text=new_text)
        self.shared_data.update_attribute(new_text)                                                                     # Update the shared data
        self.manager.hide_window('Window_2')                                                                            # Hide Window 2 AND
        self.manager.show_window('Window_1')                                                                            # Show Window 1
    def on_close(self):
        super().on_close()                                                                                              # If additional closing behavior specific to that window is necessary
        APPLOGGER.info(f'<{self.T}> closed!')                                                                           # The super().on_close() Call the base class's on_close method () from 'BaseWindow' class