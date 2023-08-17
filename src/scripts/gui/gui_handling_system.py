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
ANIMATION_OR_PICTURE_FLAG = True                                                                                        # Animation or picture
########################################################################################################################
########################################################################################################################
########################################################################################################################
### Internal Imports ###
from src.scripts.system.applogger import APPLOGGER
from src.scripts.system.config import DMDD, DMD, azure_initialization
### External Imports ###
import threading
import time
import datetime
import os
import json
import inspect
import sys
import traceback
from PIL import Image, ImageTk
import tkinter as tk
from tkinter.ttk import Progressbar
from tkcalendar import DateEntry, Calendar
class SharedData:
    def __init__(self):
        self.some_attribute = 0
        ### power-up variables ###
        self.PRESS_SN = ["Choose Press Serial Number"]
        self.PRESS = None
        self.MANAGER = None
        self.MAINAGENT = None
        self.AZURECONNECT = None
        self.METADATA = None
        self.CONFIG = None                                                                                              # This is the whole configuration azure SHARE_DATA.CONFIG["conf.json"]["presses"] or SHARE_DATA.CONFIG[""]["presses"]!
        self.THREADS_LIST = []
        self.THREADS_LIST_LOCK = threading.Lock()
        ### runtime variables ###
        self.PRESS_LIST_OF_BLOBS = None
    def update_attribute(self, value):
        with self.THREADS_LIST_LOCK:
            self.some_attribute = value
    def get_attribute(self):
        with self.THREADS_LIST_LOCK:
            return self.some_attribute

SHARE_DATA = SharedData()
def logger_explain_template(func=None, err=None):
    return f'The <{func}> has been failed! ### Error: <{err}> ### {sys.exc_info()[0]} >>> {sys.exc_info()[1]} >>> {traceback.extract_tb(list(sys.exc_info())[2])} ###'
def register_thread(thread):
    with SHARE_DATA.THREADS_LIST_LOCK:
        SHARE_DATA.THREADS_LIST.append(thread)
def handle_thread_completion(thread):                                                                                   # Custom logic for handling thread completion
    if thread.name=="tr_root_window_definition":
        APPLOGGER.debug(f"Thread {thread.name} has completed.")
    elif thread.name=="azure_initialization_thread":
        SHARE_DATA.PRESS_SN.extend(list(SHARE_DATA.CONFIG["conf.json"]["presses"]))
        SHARE_DATA.MANAGER.windows["Window_4"].update_press_sn_dropdown(SHARE_DATA.PRESS_SN)
        if DMDD["METADATA_FLAG"]:
            SHARE_DATA.PRESS_LIST_OF_BLOBS = SHARE_DATA.METADATA[DMDD["PRESS_DICT_SN"]]
        APPLOGGER.debug(f"Thread {thread.name} has completed.")
        print(SHARE_DATA.METADATA)                                                                                      # TODO: Drop print statement
        print(json.dumps(SHARE_DATA.CONFIG, indent=4))                                                                  # TODO: Drop print statement
    else:
        pass
    return None
def background_thread_checker():
    while True:
        with SHARE_DATA.THREADS_LIST_LOCK:
            for thread in SHARE_DATA.THREADS_LIST:
                if not thread.is_alive():
                    handle_thread_completion(thread)                                                                    # Handle thread completion (e.g., fetch results, perform cleanup)
                    SHARE_DATA.THREADS_LIST.remove(thread)
        time.sleep(1)                                                                                                   # Sleep for a short duration before checking again
class ToolTip(object):
    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0
    def showtip(self, text):
        """Display text in tooltip window"""
        self.text = text
        if self.tipwindow or not self.text:
            return
        x, y, _, _ = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 25
        y = y + self.widget.winfo_rooty() + 25
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
class WindowManager:                                                                                                    # Factory or Registry Pattern Create a factory or registry class to manage window creation dynamically
    def __init__(self, root):
        self.windows = {}
        self.root = root
        self.window_history = []                                                                                        # Stack to keep track of window history
        APPLOGGER.info(f'The <{inspect.currentframe().f_code.co_name}> of <WindowManager CLASS> has been created.')
    def open_loading_bar(self, stop_function=None):
        return LoadingBarWindow(self.root, self, stop_function)
    def register_window(self, window_class, shared_data=None, relation=None, extra_width=0, extra_height=0):
        name = window_class.__name__
        window = window_class(self.root, self, shared_data, relation, extra_width, extra_height)
        window.withdraw()
        self.windows[name] = window
        button = window_class.create_activation_button(self.root, lambda: self.show_window(name))                       # Create and pack the activation button for this window
        button.pack()
        APPLOGGER.info(f'The <{name}> has been registered [window:<{window}>]. with his activate button <{button}>.')
    def show_window(self, name):
        current_window_name = next((key for key, win in self.windows.items() if win.winfo_viewable()), None)
        if current_window_name and current_window_name != name:
            if current_window_name not in self.window_history:
                self.window_history.append(current_window_name)
        self.windows[name].show()
        self.root.withdraw()
        APPLOGGER.info(f'Window <{name}> has been show-up.')
    def hide_window(self, name):
        self.windows[name].hide()
    def close_window(self, name):
        window = self.windows.pop(name, None)
        if window:
            window.destroy()
        APPLOGGER.info(f'Window <{name}> has been closed.')
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
class LoadingBarWindow(tk.Toplevel):
    """ LoadingBarWindow: This class represents a loading bar window, which can be shown while a process is running.
        It includes a method to handle the closing event and stop the current process if needed. """
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
class BaseWindow(tk.Toplevel):
    """ Create a base class that will contain common functionalities like closing, showing, hiding, etc. """
    def __init__(self, root, manager, shared_data=None, relation=None, extra_width=0, extra_height=0):
        super().__init__(root)
        self.withdraw()
        self.manager = manager
        self.shared_data = shared_data
        self.relation = relation
        self.protocol('WM_DELETE_WINDOW', self.on_close)
        self.adjust_size(extra_width, extra_height)                                                                     # Call the method to adjust the size based on contents
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
        self.manager.hide_window(current_window_name)
        if self.manager.window_history:
            previous_window_name = self.manager.window_history.pop()
            self.manager.show_window(previous_window_name)
            APPLOGGER.info(f'The <{current_window_name}> window has been closed. The <{previous_window_name}> has show-up.')
        else:
            self.manager.root.deiconify()
            APPLOGGER.info(f'The <{current_window_name}> window has been closed. The <{self.manager.root}> has show-up.')
    def show(self):
        self.deiconify()
    def hide(self):
        self.withdraw()
class Window_1(BaseWindow):
    def __init__(self, root, manager, shared_data=None, relation=None, extra_width=0, extra_height=0):
        super().__init__(root, manager, shared_data, relation, extra_width, extra_height)
        self.T = "Window 1"
        self.title(self.T)
        ### Design & Widgets
        self.label = tk.Label(self, text="This is Window 1")
        self.label.pack()
        self.update_label_from_shared_data()                                                                            # Start the label updates
        self.start_button = tk.Button(self, text="Start Processing", command=self.start_processing)
        self.start_button.pack()
        self.open_window_2_button = tk.Button(self, text="Open Window 2", command=self.open_window_2)
        self.open_window_2_button.pack()
        ### Threading events
        self.processing_done = threading.Event()
        self.stop_event = threading.Event()
        APPLOGGER.info(f'The <{self.T}> which is created based on (BaseWindow class) with the relations:<{relation}> and Buttons.')
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
        APPLOGGER.debug(f'Processing ended!')
        self.on_reset()
    def on_reset(self):
        self.processing_done.set()
        self.stop_event.clear()
        self.start_button.config(state='normal')
        self.loading_bar_window.on_close()                                                                              # Close the loading bar window
        APPLOGGER.info(f'<{self.T}> reset.')
    def on_close(self):
        super().on_close()                                                                                              # If additional closing behavior specific to that window is necessary
        APPLOGGER.info(f'<{self.T}> closed!')                                                                           # The super().on_close() Call the base class's on_close method () from 'BaseWindow' class
class Window_2(BaseWindow):
    def __init__(self, root, manager, shared_data=None, relation=None, extra_width=0, extra_height=0):
        super().__init__(root, manager, shared_data, relation, extra_width, extra_height)
        self.T = "Window 2"
        self.title(self.T)
        ### Design & Widgets
        self.label = tk.Label(self, text="This is Window 2")
        self.label.pack()
        self.update_button = tk.Button(self, text="Update Label", command=self.update_label_text)
        self.update_button.pack()
        APPLOGGER.info(f'The <{self.T}> which is created based on (BaseWindow class) with the relations:<{relation}> and Buttons.')
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
class Window_3(BaseWindow):
    def __init__(self, root, manager, shared_data=None, relation=None, extra_width=0, extra_height=0):
        super().__init__(root, manager, shared_data, relation, extra_width, extra_height)
        self.T = "Date Selection Window"
        self.title(self.T)
        self.label = tk.Label(self, text="Select a date:")
        self.label.pack(padx=10, pady=5)
        ### Objects
        self.selected_date = tk.StringVar()
        ### DateEntry widget
        self.date_entry = DateEntry(self, width=40, date_pattern='Y-m-d')
        self.date_entry.pack(padx=15, pady=10)
        self.date_entry.bind("<FocusOut>", self.update_calendar)                                                        # Bind event to update calendar
        ### Calendar widget
        self.calendar = Calendar(self, selectmode="day")
        self.calendar.pack(padx=15, pady=10)
        self.calendar.bind("<<CalendarSelected>>", self.update_date_entry)                                              # Bind event to update date entry
        ### Buttons
        self.confirm_butt = tk.Button(self, text="Confirm", command=self.confirm_date)
        self.confirm_butt.pack(padx=10, pady=5)
        ### Layout ###
        self.update_idletasks()                                                                                         # Update layout calculations
        self.adjust_size(extra_width, extra_height)                                                                     # Adjust the window size
        APPLOGGER.info(f'The <{self.T}> which is created based on (BaseWindow class) with the relations:<{relation}> and Buttons.')
    @classmethod
    def create_activation_button(cls, root, command):
        text = "Activate " + cls.__name__
        APPLOGGER.info(f'The <{text}> text_button has been created with the command <{command}>.')
        return cls.create_text_button(root, command, text=text)
    def confirm_date(self):
        self.selected_date = self.calendar.selection_get()
        APPLOGGER.info(f'The "Confirm" button has been triggered and <{self.selected_date}> has been selected.')
        print(f"Selected date: {self.selected_date}")                                                                   # TODO: Remove Print
    def update_date_entry(self, event):
        selected_date = self.calendar.selection_get()
        self.date_entry.set_date(selected_date)
        APPLOGGER.info(f'The "DateEntry" has been triggered and <{selected_date}> has been selected.')
    def update_calendar(self, event):
        selected_date = self.date_entry.get_date()
        self.calendar.selection_set(selected_date)
        APPLOGGER.info(f'The "Calendar" has been triggered and <{selected_date}> has been selected.')
    def on_close(self):
        super().on_close()                                                                                              # If additional closing behavior specific to that window is necessary
        APPLOGGER.info(f'<{self.T}> closed!')                                                                           # The super().on_close() Call the base class's on_close method () from 'BaseWindow' class
class Window_4(BaseWindow):
    def __init__(self, root, manager, shared_data=None, relation=None, extra_width=0, extra_height=0):
        super().__init__(root, manager, shared_data, relation, extra_width, extra_height)
        self.T = "DATE&TIME_WINDOW"
        self.title(self.T)
        ### Create the Frames ###
        self.f0 = None
        self.create_frame_0()
        self.f1 = None
        self.create_frame_1()
        self.loading_label = None
        self.animate_flag = None
        self.loading_frame_index = None
        self.loading_frames = None
        self.loading_gif = None
        self.f2 = None
        self.create_frame_2()
        self.f3 = None
        self.create_frame_3()
        self.start_loading_animation()                                                                                  # Start Animation
        self.initialize_tooltips()                                                                                      # Initialize the ability for toolkit
        self.update_idletasks()                                                                                         # Update layout calculations
        self.adjust_size(extra_width, extra_height)                                                                     # Adjust the window size
        APPLOGGER.info(f'The <{self.T}> which is created based on (BaseWindow class) with the relations:<{relation}>, Frames and Buttons.')
    def animate_loading(self):
        if self.animate_flag and hasattr(self, 'loading_label'):                                                        # Check if the loading label still exists AND the Flag
            self.loading_frame_index = (self.loading_frame_index + 1) % len(self.loading_frames)                        # Update the image to the next frame
            self.loading_label.config(image=self.loading_frames[self.loading_frame_index])
            self.loading_label.image = self.loading_frames[self.loading_frame_index]
            self.after(50, self.animate_loading)                                                                        # Call this function again after a delay to get the next frame # 100ms delay, adjust as needed
    def start_loading_animation(self):
        resize_w = 60
        resize_h = 40
        self.animate_flag = True                                                                                        # Logic to stop the loop
        if ANIMATION_OR_PICTURE_FLAG:
            self.loading_frame_index = 0
            self.loading_frames = []  # List to hold each frame
            frames_folder = os.path.join('src', 'media', 'loading_frames')
            for frame_file in sorted(os.listdir(frames_folder)):                                                        # Load each frame into the list
                frame_path = os.path.join(frames_folder, frame_file)
                frame_image = Image.open(frame_path)
                frame_image_resized = frame_image.resize((resize_w, resize_h), Image.ANTIALIAS)
                photo_frame = ImageTk.PhotoImage(frame_image_resized)
                self.loading_frames.append(photo_frame)
            self.loading_label = tk.Label(self.f1, image=self.loading_frames[self.loading_frame_index])                 # Create the label to display the frame
            self.loading_label.pack(side="right")                                                                       # Start the animation loop
            self.animate_loading()
        else:
            gif_image = Image.open(os.path.join('src', 'media', 'loading_frames.gif'))                                  # Load the gif using PIL
            gif_image_resized = gif_image.resize((resize_w, resize_h), Image.ANTIALIAS)                                 # Resize the gif
            self.loading_gif = ImageTk.PhotoImage(gif_image_resized)                                                    # Convert the resized gif to a PhotoImage for use in Tkinter
            self.loading_label = tk.Label(self.f1, image=self.loading_gif)                                              # Create a label to display the gif
            self.loading_label.image = self.loading_gif                                                                 # Keep a reference to prevent garbage collection
            self.loading_label.pack(side="right")
    def stop_loading_animation(self):
        _ = {inspect.currentframe().f_code.co_name}
        self.animate_flag = False
        try:
            self.loading_label.destroy()
        except Exception as e:
            APPLOGGER.error(f'{logger_explain_template(func=_, err=e)}')
    def create_frame_0(self):                                                                                           # Frame 0 (F0): "Control"
        self.f0 = tk.Frame(self)
        self.f0.pack(anchor="n", padx=10, pady=5, fill='x')                                                             # I added fill='x' to ensure the frame expands horizontally
        self.left_frame = tk.Frame(self.f0)                                                                             # This frame will hold the left-aligned buttons
        self.left_frame.pack(side="left", anchor="nw")                                                                  # Anchored to the northwest (top-left)
        self.return_button = tk.Button(self.left_frame, text="Return", command=self.on_close)                           # The return button
        self.return_button.pack(side="left")
        self.reset_button = tk.Button(self.left_frame, text="Reset", command=self.reset_fields)                         # The reset button
        self.reset_button.pack(side="left", padx=10)
        self.right_frame = tk.Frame(self.f0)                                                                            # This frame will hold the right-aligned checkbox
        self.right_frame.pack(side="right", anchor="ne")                                                                # Anchored to the northeast (top-right)
        self.dev_var = tk.BooleanVar()                                                                                  # Variable to track the state of the checkbox
        self.dev_checkbox = tk.Checkbutton(self.right_frame, text="Dev", variable=self.dev_var, command=self.dev_checkbox_changed)
        self.dev_checkbox.pack(anchor="ne")
        APPLOGGER.info(f'The Frame <{inspect.currentframe().f_code.co_name}> has been created.')
    def create_frame_1(self):                                                                                           # Frame 1 (F1): "Config"
        self.f1 = tk.Frame(self)
        self.f1.pack(anchor="n", padx=10, pady=5)
        self.press_sn_values = self.get_press_sn_values()                                                               # TODO: Placeholder function to get dropdown values
        self.press_sn_default_value = self.get_default_press_sn()
        self.press_sn_var = tk.StringVar(value=self.press_sn_default_value)                                             # TODO: Placeholder function to get default value
        self.press_sn_dropdown = tk.OptionMenu(self.f1, self.press_sn_var, *self.press_sn_values)                       # Define DROPDOWN widget - if I want to show up the dropdown list before Azure loading data - Unnecessary [self.press_sn_dropdown.pack(anchor="n", side="left")]
        APPLOGGER.info(f'The Frame <{inspect.currentframe().f_code.co_name}> has been created.')
    def create_frame_2(self):                                                                                           # Frame 2 (F2): "dateNtime"
        self.f2 = tk.Frame(self)
        self.f2.pack(anchor="n", padx=10, pady=5)
        ### Large Calendar widget ###
        self.calendar = Calendar(self.f2, selectmode="day", font="Arial 21")
        self.calendar.pack(side="top", padx=5, pady=10, fill=tk.BOTH, expand=True)
        ### Time Picker using Spinbox ###
        self.time_frame = tk.Frame(self.f2)
        self.time_frame.pack(side="top", pady=5)
        current_time = datetime.datetime.now().time()
        self.hour_var = tk.StringVar(value=current_time.strftime("%H"))                                                 # HOUR spinbox
        self.hour_spin = tk.Spinbox(self.time_frame, from_=0, to=23, textvariable=self.hour_var, command=self.coerce_hour, width=10, format="%02.0f", font="Arial 10", justify='center')
        self.hour_spin.pack(side="left", padx=2)
        self.minute_var = tk.StringVar(value=current_time.strftime("%M"))                                               # MINUTE spinbox
        self.minute_spin = tk.Spinbox(self.time_frame, from_=0, to=59, textvariable=self.minute_var, command=self.coerce_minute, width=10, format="%02.0f", font="Arial 10",justify='center')
        self.minute_spin.pack(side="left", padx=2)
        self.second_var = tk.StringVar(value="00")                                                                      # SECOND spinbox
        self.second_spin = tk.Spinbox(self.time_frame, from_=0, to=59, textvariable=self.second_var, command=self.coerce_second, width=10, format="%02.0f", font="Arial 10", justify='center')
        self.second_spin.pack(side="left", padx=5)
        ### Right Frame containing both Start and End sections ###
        self.right_frame = tk.Frame(self.f2)
        self.right_frame.pack(side="top", padx=5, pady=10)
        ### Left side: Start section ###
        self.start_frame = tk.Frame(self.right_frame)
        self.start_frame.pack(side="left", padx=10, pady=5)
        self.set_start_button = tk.Button(self.start_frame, text="Click to set Start Date & Time", command=self.set_start, font=("Arial", 10, "bold"))
        self.set_start_button.pack(anchor="n")
        self.start_date_var = tk.StringVar(value=self.get_current_date())
        self.start_date_entry = tk.Entry(self.start_frame, textvariable=self.start_date_var, justify='center', width=30)
        self.start_date_entry.pack(anchor="n", pady=5)
        self.start_time_var = tk.StringVar(value="00:01")
        self.start_time_entry = tk.Entry(self.start_frame, textvariable=self.start_time_var, justify='center', width=30)
        self.start_time_entry.pack(anchor="n")
        ### Right side: End section ###
        self.end_frame = tk.Frame(self.right_frame)
        self.end_frame.pack(side="left", padx=10, pady=5)
        self.set_end_button = tk.Button(self.end_frame, text="Click to set End Date&Time", command=self.set_end, font=("Arial", 10, "bold"))
        self.set_end_button.pack(anchor="n")
        self.end_date_var = tk.StringVar(value=self.get_current_date())
        self.end_date_entry = tk.Entry(self.end_frame, textvariable=self.end_date_var, justify='center',  width=30)
        self.end_date_entry.pack(anchor="n", pady=5)
        self.end_time_var = tk.StringVar(value=self.get_current_time())
        self.end_time_entry = tk.Entry(self.end_frame, textvariable=self.end_time_var, justify='center',  width=30)
        self.end_time_entry.pack(anchor="n")
        APPLOGGER.info(f'The Frame <{inspect.currentframe().f_code.co_name}> has been created.')
    def create_frame_3(self):                                                                                           # Frame 3 (F3): "confirm"
        self.f3 = tk.Frame(self)
        self.f3.pack(anchor="n", padx=10, pady=5)
        image = Image.open(os.path.join('src', 'media\\supporter.png'))
        self.supporter_image = ImageTk.PhotoImage(image)
        image = Image.open(os.path.join('src', 'media\\v12.png'))
        self.press_pc_image = ImageTk.PhotoImage(image)
        self.supporter_button = tk.Button(self.f3, image=self.supporter_image, text="Proceed as Supporter", font=("Arial", 10, "bold"), compound=tk.BOTTOM, command=self.supporter_action)
        self.press_pc_button = tk.Button(self.f3, image=self.press_pc_image, text="Proceed as Press-PC", font=("Arial", 10, "bold"), compound=tk.BOTTOM, command=self.press_pc_action)
        self.supporter_button.pack(side="left", padx=10)
        self.press_pc_button.pack(side="left", padx=10)
        APPLOGGER.info(f'The Frame <{inspect.currentframe().f_code.co_name}> has been created.')
    @classmethod
    def create_activation_button(cls, root, command):
        text = "Activate " + cls.__name__
        return cls.create_text_button(root, command, text=text)
    def reset_fields(self):
        APPLOGGER.info(f'The <{inspect.currentframe().f_code.co_name}> has been activated.')
        ### Resetting DateEntry and Calendar ###
        current_date = self.get_current_date()
        year, month, day = map(int, current_date.split('-'))
        specific_date = datetime.date(year, month, day)
        self.calendar.selection_set(specific_date)
        ### Resetting time to current time ###
        current_hour, current_minute = self.get_current_time().split(':')
        self.hour_spin.delete(0, "end")
        self.hour_spin.insert(0, current_hour)
        self.minute_spin.delete(0, "end")
        self.minute_spin.insert(0, current_minute)
        self.second_spin.delete(0, "end")
        self.second_spin.insert(0, "00")
        ### Resetting Start and End date fields ###
        self.start_date_var.set(current_date)
        self.end_date_var.set(current_date)
        self.start_time_var.set("00:01")
        self.end_time_var.set(self.get_current_time())
        ### Resetting dev mode checkbox ###
        self.dev_var.set(False)
    def initialize_tooltips(self):
        APPLOGGER.info(f'The <{inspect.currentframe().f_code.co_name}> has been activated.')
        create_tooltip(self.set_start_button, "Set the start date and time to the selected values.")
        create_tooltip(self.set_end_button, "Set the end date and time to the selected values.")
        create_tooltip(self.dev_checkbox, "Enable development mode (for debugging or advanced features).")
    def dev_checkbox_changed(self):
        if self.dev_var.get():
            self.initialize_data_from_external()                                                                        # TODO: Placeholder function
    def initialize_data_from_external(self):
        APPLOGGER.info(f'The <{inspect.currentframe().f_code.co_name}> has been activated!')                            # TODO: Placeholder values
    def get_press_sn_values(self):
        APPLOGGER.info(f'The <{inspect.currentframe().f_code.co_name}> has been activated!')                            # TODO: Placeholder values
        return ["..."]
    def get_default_press_sn(self):
        APPLOGGER.info(f'The <{inspect.currentframe().f_code.co_name}> has been activated!')                            # TODO: Placeholder default values
        return DMDD["PRESS_DICT_SN"] if DMDD["PRESS_DICT_SN"] != DMD.PRESS_DICT_SN else SHARE_DATA.PRESS_SN[0]          # Return local_machine if there is local METADATA_CONF.json
    def update_press_sn_dropdown(self, new_values):                                                                     # Update the dropdown values with new_values.
        _ = {inspect.currentframe().f_code.co_name}
        try:
            self.press_sn_dropdown["menu"].delete(0, "end")                                                             # Clear the current menu entries
            self.press_sn_var.set(self.press_sn_default_value if self.press_sn_default_value in new_values else new_values[0]) # Update the variable holding the current value
            for value in new_values:                                                                                    # Add new menu entries
                self.press_sn_dropdown["menu"].add_command(label=value, command=tk._setit(self.press_sn_var, value))
            self.stop_loading_animation()
            self.press_sn_dropdown.pack(anchor="n")
            APPLOGGER.info(f'The <{_}> done - list is updated!')
        except Exception as e:
            APPLOGGER.error(f'{logger_explain_template(func=_, err=e)}')
    def get_current_date(self):
        return time.strftime('%Y-%m-%d')
    def get_current_time(self):
        return time.strftime('%H:%M')
    def coerce_hour(self):
        hour = int(self.hour_spin.get())
        if hour < 0:
            self.hour_spin.delete(0, "end")
            self.hour_spin.insert(0, "00")
            APPLOGGER.debug(f'The <{inspect.currentframe().f_code.co_name}> has been activated! - The user inputs was incorrect and fixed.')
        elif hour > 23:
            self.hour_spin.delete(0, "end")
            self.hour_spin.insert(0, "23")
            APPLOGGER.debug(f'The <{inspect.currentframe().f_code.co_name}> has been activated! - The user inputs was incorrect and fixed.')
    def coerce_minute(self):
        minute = int(self.minute_spin.get())
        if minute < 0:
            self.minute_spin.delete(0, "end")
            self.minute_spin.insert(0, "00")
            APPLOGGER.debug(f'The <{inspect.currentframe().f_code.co_name}> has been activated! - The user inputs was incorrect and fixed.')
        elif minute > 59:
            self.minute_spin.delete(0, "end")
            self.minute_spin.insert(0, "59")
            APPLOGGER.debug(f'The <{inspect.currentframe().f_code.co_name}> has been activated! - The user inputs was incorrect and fixed.')
    def coerce_second(self):
        second = int(self.second_spin.get())
        if second < 0:
            self.second_spin.delete(0, "end")
            self.second_spin.insert(0, "00")
            APPLOGGER.debug(f'The <{inspect.currentframe().f_code.co_name}> has been activated! - The user inputs was incorrect and fixed.')
        elif second > 59:
            self.second_spin.delete(0, "end")
            self.second_spin.insert(0, "59")
            APPLOGGER.debug(f'The <{inspect.currentframe().f_code.co_name}> has been activated! - The user inputs was incorrect and fixed.')
    def set_start(self):
        APPLOGGER.info(f'The <{inspect.currentframe().f_code.co_name}> has been activated!')
        self.coerce_hour()
        self.coerce_minute()
        self.coerce_second()
        selected_date = self.calendar.selection_get()
        selected_time = f"{self.hour_var.get()}:{self.minute_var.get()}:00"
        self.start_date_var.set(f"{selected_date.strftime('%Y-%m-%d')}")
        self.start_time_var.set(selected_time)
    def set_end(self):
        APPLOGGER.info(f'The <{inspect.currentframe().f_code.co_name}> has been activated!')
        self.coerce_hour()
        self.coerce_minute()
        self.coerce_second()
        selected_date = self.calendar.selection_get()
        selected_time = f"{self.hour_var.get()}:{self.minute_var.get()}:00"
        self.end_date_var.set(f"{selected_date.strftime('%Y-%m-%d')}")
        self.end_time_var.set(selected_time)
    def confirm_and_proceed(self):
        print(f"Start Date: {self.start_date_var.get()}, Start Time: {self.start_time_var.get()}")                      # TODO: Placeholder for functionality that you'd like to add when 'Confirm' is clicked. For now, we'll simply display the values chosen in this window.
        print(f"End Date: {self.end_date_var.get()}, End Time: {self.end_time_var.get()}")                              # TODO: If you want to transition to the next window, add the necessary code here. For demonstration purposes, we'll just close the current window.
        self.on_close()
    def supporter_action(self):
        print("Supporter button clicked!")                                                                              # TODO: Add your logic here...SUPPORTER
        self.confirm_and_proceed()
    def press_pc_action(self):
        print("Press-PC button clicked!")                                                                               # TODO: Add your logic here...PRESS_PC
        self.confirm_and_proceed()
    def on_close(self):
        if self.dev_var.get():                                                                                          # If development mode checked - you should work with the ROOT
            super().on_close()
            APPLOGGER.debug(f'<{self.T}> closed in Development mode')
        else:                                                                                                           # If development mode unchecked [Default] - The application will closed.
            current_window_name = self.__class__.__name__
            self.manager.hide_window(current_window_name)
            self.manager.root.destroy()
        APPLOGGER.info(f'<{self.T}> closed!')
def root_window_definition(root, extra_width=0, extra_height=0):
    APPLOGGER.info(f'The <{inspect.currentframe().f_code.co_name}> has been activated.')
    root.attributes('-alpha', 1.0)  # This will make the root window fully opaque
    root.protocol("WM_DELETE_WINDOW", root.destroy)
    root.update_idletasks()                                                                                             # Get the current width and height of the root window
    width = root.winfo_width() + extra_width
    height = root.winfo_height() + extra_height
    root.geometry(f"{width}x{height}")                                                                                  # Set the new size
    root.withdraw()
    # ### Start the azure_main_initialization subprocess ###
    # azure_initialization_thread = threading.Thread(name="azure_initialization_thread", target=azure_initialization, args=(APPLOGGER, SHARE_DATA), daemon=True)
    # azure_initialization_thread.start()
    # register_thread(azure_initialization_thread)
# TODO:
#       background SUPPORTER GUI building and withdraw()
#       background Press-PC GUI building and withdraw()
def main_gui_handling_system():
    root = tk.Tk()
    root.attributes('-alpha', 0.0)                                                                                      # This will make the root window fully transparent
    manager = WindowManager(root)                                                                                       # Define the Manager for the root
    SHARE_DATA.MANAGER = manager
    ### Start the background checker in a separate thread ###
    checker_thread = threading.Thread(target=background_thread_checker, daemon=True)
    checker_thread.start()
    ### Start azure_initialization subprocess from config.py ###
    azure_initialization_thread = threading.Thread(name="azure_initialization_thread", target=azure_initialization, args=(APPLOGGER, SHARE_DATA), daemon=True)
    azure_initialization_thread.start()
    register_thread(azure_initialization_thread)

    ### Start root_window_definition subprocess ###
    tr_root_window_definition = threading.Thread(name="tr_root_window_definition", target=root_window_definition, args=(root, 100, 100), daemon=True)
    tr_root_window_definition.start()
    register_thread(tr_root_window_definition)

    ### Register windows
    manager.register_window(Window_1, shared_data=SHARE_DATA, extra_width=50, extra_height=100)                         # passing the shared data object and extra width&height
    manager.register_window(Window_2, shared_data=SHARE_DATA, extra_width=20, extra_height=10)                          # passing the shared data object and extra width&height
    manager.register_window(Window_3, shared_data=SHARE_DATA, extra_width=100, extra_height=100)                        # passing the shared data object and extra width&height
    manager.register_window(Window_4, shared_data=SHARE_DATA, extra_width=1, extra_height=1)                            # passing the shared data object and extra width&height

    # Automatically open Window_4
    manager.show_window("Window_4")
    # tr_root_window_definition = threading.Thread(name="tr_root_window_definition", target=root_window_definition, args=(root, 100, 100), daemon=True)
    # tr_root_window_definition.start()
    # register_thread(tr_root_window_definition)

    ### Start Main Loop ###
    root.mainloop()
