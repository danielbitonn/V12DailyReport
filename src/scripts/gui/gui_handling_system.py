import threading
import time
import datetime
import os
from PIL import Image, ImageTk
import tkinter as tk
from tkinter.ttk import Progressbar
from tkcalendar import DateEntry, Calendar
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
        label = tk.Label(tw, text=self.text, justify=tk.LEFT, background="#ffffe0", relief=tk.SOLID, borderwidth=1, font=("tahoma", "8", "normal"))
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
def get_image_path(filename):
    script_dir = os.path.dirname(os.path.abspath(__file__))                                                             # Get the directory of the current script
    return os.path.join(script_dir, filename)                                                                           # Join the script directory with the relative path to the image
class SharedData:
    def __init__(self):
        self.some_attribute = 0
    def update_attribute(self, value):
        self.some_attribute = value
    def get_attribute(self):
        return self.some_attribute
class WindowManager:
    """ Factory or Registry Pattern Create a factory or registry class to manage window creation dynamically """
    def __init__(self, root):
        self.windows = {}
        self.root = root
        self.window_history = []                                                                                        # Stack to keep track of window history
    def open_loading_bar(self, stop_function=None):
        return LoadingBarWindow(self.root, self, stop_function)
    def register_window(self, window_class, shared_data=None, relation=None, extra_width=0, extra_height=0):
        name = window_class.__name__
        window = window_class(self.root, self, shared_data, relation, extra_width, extra_height)
        window.withdraw()
        self.windows[name] = window
        button = window_class.create_activation_button(self.root, lambda: self.show_window(name))                       # Create and pack the activation button for this window
        button.pack()
    def show_window(self, name):
        current_window_name = next((key for key, win in self.windows.items() if win.winfo_viewable()), None)
        if current_window_name and current_window_name != name:
            if current_window_name not in self.window_history:
                self.window_history.append(current_window_name)
        self.windows[name].show()
        self.root.withdraw()
    def hide_window(self, name):
        self.windows[name].hide()
    def close_window(self, name):
        window = self.windows.pop(name, None)
        if window:
            window.destroy()
    def close_and_return_to_root(self, name):
        window = self.windows.pop(name, None)
        if window:
            window.destroy()
        self.root.deiconify()  # Show the root window
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
    @classmethod
    def create_image_button(cls, root, command, image_path):
        image = Image.open(image_path)
        photo_image = ImageTk.PhotoImage(image)
        button = tk.Button(root, image=photo_image, command=command)
        button.image = photo_image
        return button
    @classmethod
    def create_text_button(cls, root, command, text):
        return tk.Button(root, text=text, command=command)
    @classmethod
    def create_toggle_button(cls, root, command, text):
        return tk.Checkbutton(root, text=text, command=command)
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
        else:
            self.manager.root.deiconify()
    def show(self):
        self.deiconify()
    def hide(self):
        self.withdraw()
''' ####################### Create individual window classes that inherit from BaseWindow   ####################### '''
class Window_1(BaseWindow):
    def __init__(self, root, manager, shared_data=None, relation=None, extra_width=0, extra_height=0):
        super().__init__(root, manager, shared_data, relation, extra_width, extra_height)
        self.title("Window 1")
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
        self.after(500, self.update_label_from_shared_data)                                                             # Schedule this method to run again after 1 second
    def start_processing(self):
        print("Starting processing...")
        self.processing_done.clear()
        self.stop_event.clear()
        self.start_button.config(state='disabled')
        self.loading_bar_window = self.manager.open_loading_bar(stop_function=self.stop_processing)
        self.loading_bar_window.deiconify()                                                                             # Show the loading bar window
        threading.Thread(target=self.processing, daemon=True).start()
    def stop_processing(self):
        print("stop-processing...")
        self.stop_event.set()
        self.loading_bar_window.progress.stop()                                                                         # Stop the progress bar
        self.loading_bar_window.withdraw()                                                                              # Hide the loading bar window
    def processing(self):
        # TODO:                                                                                                         Example processing logic - replace with real program activation
        for i in range(10):
            if self.stop_event.is_set():
                print("Stop event detected, breaking the loop")
                break
            time.sleep(1)
            print("Processing step", i)
        print("Processing ended!")
        self.on_reset()
    def on_reset(self):
        self.processing_done.set()
        self.stop_event.clear()
        self.start_button.config(state='normal')
        self.loading_bar_window.on_close()                                                                              # Close the loading bar window
    def on_close(self):
        super().on_close()                                                                                              # If additional closing behavior specific to that window is necessary
                                                                                                                        # The super().on_close() Call the base class's on_close method () from 'BaseWindow' class
class Window_2(BaseWindow):
    def __init__(self, root, manager, shared_data=None, relation=None, extra_width=0, extra_height=0):
        super().__init__(root, manager, shared_data, relation, extra_width, extra_height)
        self.title("Window 2")
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
                                                                                                                        # The super().on_close() Call the base class's on_close method () from 'BaseWindow' class
class Window_3(BaseWindow):
    def __init__(self, root, manager, shared_data=None, relation=None, extra_width=0, extra_height=0):
        super().__init__(root, manager, shared_data, relation, extra_width, extra_height)
        self.title("Date Selection Window")
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

        self.update_idletasks()                                                                                         # Update layout calculations
        self.adjust_size(extra_width, extra_height)                                                                     # Adjust the window size

    @classmethod
    def create_activation_button(cls, root, command):
        text = "Activate " + cls.__name__
        return cls.create_text_button(root, command, text=text)
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
        super().on_close()                                                                                              # If additional closing behavior specific to that window is necessary
                                                                                                                        # The super().on_close() Call the base class's on_close method () from 'BaseWindow' class
class Window_4(BaseWindow):
    def __init__(self, root, manager, shared_data=None, relation=None, extra_width=0, extra_height=0):
        super().__init__(root, manager, shared_data, relation, extra_width, extra_height)
        self.title("DATE&TIME_WINDOW")
        ### Create the Frames ###
        self.create_frame_0()
        self.create_frame_1()
        self.create_frame_2()
        self.create_frame_3()

        ### Initialize the ability for toolkit ###
        self.initialize_tooltips()

        self.update_idletasks()                                                                                         # Update layout calculations
        self.adjust_size(extra_width, extra_height)                                                                     # Adjust the window size
        
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
        self.dev_checkbox = tk.Checkbutton(self.right_frame, text="Dev", variable=self.dev_var,command=self.dev_checkbox_changed)
        self.dev_checkbox.pack(anchor="ne")
    def create_frame_1(self):                                                                                           # Frame 1 (F1): "Config"
        self.f1 = tk.Frame(self)
        self.f1.pack(anchor="n", padx=10, pady=5)

        self.press_sn_values = self.get_press_sn_values()                                                               # TODO: Placeholder function to get dropdown values
        self.press_sn_var = tk.StringVar(value=self.get_default_press_sn())                                             # TODO: Placeholder function to get default value
        self.press_sn_dropdown = tk.OptionMenu(self.f1, self.press_sn_var, *self.press_sn_values)
        self.press_sn_dropdown.pack(anchor="n")

    def create_frame_2(self):                                                                                           # Frame 2 (F2): "dateNtime"
        self.f2 = tk.Frame(self)
        self.f2.pack(anchor="n", padx=10, pady=5)

        ### Large Calendar widget ###
        self.calendar = Calendar(self.f2, selectmode="day", font="Arial 22")
        self.calendar.pack(side="top", padx=5, pady=10, fill=tk.BOTH, expand=True)

        ### Time Picker using Spinbox ###
        self.time_frame = tk.Frame(self.f2)
        self.time_frame.pack(side="top", pady=5)

        current_time = datetime.datetime.now().time()
        self.hour_var = tk.StringVar(value=current_time.strftime("%H"))                                                 # HOUR spinbox
        self.hour_spin = tk.Spinbox(self.time_frame, from_=0, to=23, textvariable=self.hour_var, command=self.coerce_hour, width=5, format="%02.0f", font="Arial 10", justify='center')
        self.hour_spin.pack(side="left", padx=2)

        self.minute_var = tk.StringVar(value=current_time.strftime("%M"))                                               # MINUTE spinbox
        self.minute_spin = tk.Spinbox(self.time_frame, from_=0, to=59, textvariable=self.minute_var, command=self.coerce_minute, width=5, format="%02.0f", font="Arial 10",justify='center')
        self.minute_spin.pack(side="left", padx=2)

        self.second_var = tk.StringVar(value="00")                                                                      # SECOND spinbox
        self.second_spin = tk.Spinbox(self.time_frame, from_=0, to=59, textvariable=self.second_var, command=self.coerce_second, width=5, format="%02.0f", font="Arial 10", justify='center')
        self.second_spin.pack(side="left", padx=5)

        ### Right Frame containing both Start and End sections ###
        self.right_frame = tk.Frame(self.f2)
        self.right_frame.pack(side="top", padx=5, pady=10)

        ### Left side: Start section ###
        self.start_frame = tk.Frame(self.right_frame)
        self.start_frame.pack(side="left", padx=10, pady=5)

        self.set_start_button = tk.Button(self.start_frame, text="Set Start", command=self.set_start)
        self.set_start_button.pack(anchor="n")

        self.start_date_var = tk.StringVar(value=self.get_current_date())
        self.start_date_entry = tk.Entry(self.start_frame, textvariable=self.start_date_var, justify='center')
        self.start_date_entry.pack(anchor="n", pady=5)

        self.start_time_var = tk.StringVar(value="00:01")
        self.start_time_entry = tk.Entry(self.start_frame, textvariable=self.start_time_var, justify='center')
        self.start_time_entry.pack(anchor="n")

        ### Right side: End section ###
        self.end_frame = tk.Frame(self.right_frame)
        self.end_frame.pack(side="left", padx=10, pady=5)
        self.set_end_button = tk.Button(self.end_frame, text="Set End", command=self.set_end)
        self.set_end_button.pack(anchor="n")
        self.end_date_var = tk.StringVar(value=self.get_current_date())
        self.end_date_entry = tk.Entry(self.end_frame, textvariable=self.end_date_var, justify='center')
        self.end_date_entry.pack(anchor="n", pady=5)
        self.end_time_var = tk.StringVar(value=self.get_current_time())
        self.end_time_entry = tk.Entry(self.end_frame, textvariable=self.end_time_var, justify='center')
        self.end_time_entry.pack(anchor="n")
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

    @classmethod
    def create_activation_button(cls, root, command):
        text = "Activate " + cls.__name__
        return cls.create_text_button(root, command, text=text)

    def reset_fields(self):
        print("reset_fields function called!")
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
        create_tooltip(self.set_start_button, "Set the start date and time to the selected values.")
        create_tooltip(self.set_end_button, "Set the end date and time to the selected values.")
        create_tooltip(self.dev_checkbox, "Enable development mode (for debugging or advanced features).")
    def dev_checkbox_changed(self):
        if self.dev_var.get():
            self.initialize_data_from_external()                                                                        # TODO: Placeholder function
    def initialize_data_from_external(self):
        print("initialize_data_from_external function called!")                                                         # TODO: Placeholder values
    def get_press_sn_values(self):
        print("get_press_sn_values function called!")                                                                   # TODO: Placeholder values
        return ["Option1", "Option2", "Option3"]
    def get_default_press_sn(self):
        print("get_default_press_sn function called!")                                                                  # TODO: Placeholder default value
        return "Option1"
    def get_current_date(self):
        return time.strftime('%Y-%m-%d')
    def get_current_time(self):
        return time.strftime('%H:%M')
    def coerce_hour(self):
        hour = int(self.hour_spin.get())
        if hour < 0:
            self.hour_spin.delete(0, "end")
            self.hour_spin.insert(0, "00")
        elif hour > 23:
            self.hour_spin.delete(0, "end")
            self.hour_spin.insert(0, "23")
    def coerce_minute(self):
        minute = int(self.minute_spin.get())
        if minute < 0:
            self.minute_spin.delete(0, "end")
            self.minute_spin.insert(0, "00")
        elif minute > 59:
            self.minute_spin.delete(0, "end")
            self.minute_spin.insert(0, "59")
    def coerce_second(self):
        second = int(self.second_spin.get())
        if second < 0:
            self.second_spin.delete(0, "end")
            self.second_spin.insert(0, "00")
        elif second > 59:
            self.second_spin.delete(0, "end")
            self.second_spin.insert(0, "59")
    def set_start(self):
        self.coerce_hour()
        self.coerce_minute()
        self.coerce_second()
        print("set_start function called!")
        selected_date = self.calendar.selection_get()
        selected_time = f"{self.hour_var.get()}:{self.minute_var.get()}:00"
        self.start_date_var.set(f"{selected_date.strftime('%Y-%m-%d')}")
        self.start_time_var.set(selected_time)
    def set_end(self):
        self.coerce_hour()
        self.coerce_minute()
        self.coerce_second()
        print("set_end function called!")
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
    def press_pc_action(self):
        print("Press-PC button clicked!")                                                                               # TODO: Add your logic here...PRESS_PC

class LoadingBarWindow(tk.Toplevel):
    """ LoadingBarWindow: This class represents a loading bar window, which can be shown while a process is running.
        It includes a method to handle the closing event and stop the current process if needed. """
    def __init__(self, root, manager, stop_function=None):
        super().__init__(root)
        self.manager = manager
        self.stop_function = stop_function
        self.title("Loading...")
        self.progress = Progressbar(self, length=200, mode='indeterminate')
        self.progress.pack(pady=10)
        self.bind("<Map>", self.on_show)                                                                                # Bind the show event
        self.protocol('WM_DELETE_WINDOW', self.on_close)                                                                # Override close behavior
    def on_close(self):
        if self.stop_function:
            self.stop_function()                                                                                        # Stop the current process
        self.progress.stop()                                                                                            # Stop the progress bar
        self.withdraw()                                                                                                 # Hide the window
    def on_show(self, event):
        self.progress.stop()                                                                                            # Stop the progress bar (if it's running)
        self.progress.start()                                                                                           # Restart the progress bar
def root_window_definition(root, extra_width=0, extra_height=0):
    root.protocol("WM_DELETE_WINDOW", root.destroy)
    root.update_idletasks()                                                                                             # Get the current width and height of the root window
    width = root.winfo_width() + extra_width
    height = root.winfo_height() + extra_height
    root.geometry(f"{width}x{height}")                                                                                  # Set the new size
def main_gui_handling_system():
    root = tk.Tk()
    manager = WindowManager(root)                                                                                       # Define the Manager for the root
    shared_data = SharedData()                                                                                          # Create the shared data object

    ### Register the windows
    manager.register_window(Window_1, shared_data=shared_data, extra_width=50, extra_height=100)                        # passing the shared data object and extra width&height
    manager.register_window(Window_2, shared_data=shared_data, extra_width=20, extra_height=10)                         # passing the shared data object and extra width&height
    manager.register_window(Window_3, shared_data=shared_data, extra_width=100, extra_height=100)                       # passing the shared data object and extra width&height
    manager.register_window(Window_4, shared_data=shared_data, extra_width=1, extra_height=1)                           # passing the shared data object and extra width&height

    root_window_definition(root, extra_width=100, extra_height=100)                                                     # Define the root window
    ### Start Main Loop ###
    root.mainloop()
