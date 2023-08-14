import threading
import time
import os
from PIL import Image, ImageTk
import tkinter as tk
from tkinter.ttk import Progressbar
from tkcalendar import DateEntry, Calendar

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
        window.hide()
        self.windows[name] = window
        # Create and pack the activation button for this window
        button = window_class.create_activation_button(self.root, lambda: self.show_window(name))
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

    # TODO:                                                                                                             Add any other root-specific configurations here


def main_gui_handling_system():
    root = tk.Tk()
    manager = WindowManager(root)                                                                                       # Define the Manager for the root
    shared_data = SharedData()                                                                                          # Create the shared data object

    ### Register the windows
    manager.register_window(Window_1, shared_data=shared_data, extra_width=50, extra_height=100)                        # passing the shared data object and extra width&height
    manager.register_window(Window_2, shared_data=shared_data, extra_width=20, extra_height=10)                         # passing the shared data object and extra width&height
    manager.register_window(Window_3, shared_data=shared_data, extra_width=100, extra_height=100)                       # passing the shared data object and extra width&height

    root_window_definition(root, extra_width=100, extra_height=100)                                                     # Define the root window
    ### Start Main Loop ###
    root.mainloop()














    # Optionally, you can access shared data or interact with other windows through self.shared_data and self.manager


'''
############################################################ START HERE   ############################################################
'''
# main_gui_handling_system()
