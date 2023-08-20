import inspect
import threading
import time

from src.scripts.system.config import DMDD, DMD, folders_handler
from src.scripts.system.applogger import APPLOGGER
from src.scripts.gui.windows.win_utility import SHARE_DATA, BaseWindow, logger_explain_template, register_thread

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import json
from datetime import datetime
import os
from tkinter import messagebox                                                                                          # messagebox.showerror(title="Error", message=f'Processing step {i}')

from src.scripts.system.utilities_functions import update_master_json, read_master_json

ANIMATION_OR_PICTURE_FLAG   = DMDD["ANIMATION_OR_PICTURE_FLAG"]                                                         # Animation or picture

# PRESS_STATUS_OPTIONS = [
#     ('Printing',                    'lightgreen',   '#ccffcc'),     # Light green
#     ('Printing with limitation',    'orange',       '#ffe6cc'),     # Light orange
#     ('Proactive shutdown',          '#999900',      '#ffffcc'),     # Light yellow
#     ('Pending customer',            'purple',       '#e6ccff'),     # Light purple
#     ('MD - Troubleshooting',        'red',          '#ffcccc'),     # Light red
#     ('MD - Waiting for parts',      'red',          '#ffcccc'),     # Light red
#     ('MD - Escalation',             'red',          '#ffcccc')      # Light red
# ]

# SHIFT_OPTIONS = ('Morning', 'Noon', 'Night')
class Window_5(BaseWindow):
    """
    sticky="ns": The widget will expand vertically, sticking to both the top (North) and bottom (South) of the cell.
    sticky="nsew": The widget will expand in both directions, filling the entire cell.
    If sticky isn't provided, the widget is centered in its cell without expanding
    In your example, sticky="we" makes the press_status_combo widget expand horizontally to fill its cell in the grid, sticking to both the left and right sides.
    """
    def __init__(self, root, manager, shared_data=None, relation=None, extra_width=0, extra_height=0):
        super().__init__(root, manager, shared_data, relation, extra_width, extra_height)
        self.T = "Window_5"
        self.title("V12 Daily Report")
        self.extra_width = extra_width
        self.extra_height = extra_height
        self._today = datetime.today().date().isoformat()
        self.shared_data.DICT_PRESS_STATUS_OPTIONS_n_COLORS
        self.shared_data.DICT_SHIFT_OPTIONS

        ### Data ###
        self.press_history  = read_master_json().get("press_history", {}).get("data", [])                               # History Data or [] for the first time!
        self.press_data     = read_master_json().get("press_data", {}).get("data", [])                                  # History Data or [] for the first time!

        self.create_frame_0()
        self.start_loading_animation()  # Start Animation
        threading.Thread(target=self.design_window, daemon=True).start()                                                # Schedule the design of the window in a background thread
        APPLOGGER.info(f'The <{self.T}> which is created based on (BaseWindow class) with the relations:<{relation}>, Frames and Buttons.')
    def design_window(self):                                                                                            # Finalize the design in the main thread
        task_info = (self.finalize_window_design, f"{self.__class__.__name__} - design_window")
        SHARE_DATA.TASK_QUEUE.put(task_info)                                                                            # SHARE_DATA.TASK_QUEUE.put(self.finalize_window_design)
    def gate_func_win_5(self):
        """The Gate to window_5"""
        background_tasks_window_5 = threading.Thread(name="background_tasks_window_5", target=self.background_tasks_window_5, daemon=True)                                               # Schedule the design of the window in a background thread
        register_thread(background_tasks_window_5)
        background_tasks_window_5.start()
        self.stop_loading_animation()
        # TODO: Still waiting to the data to be loaded.
        #   Only the constant data can be edit. keep "animation loader" on the EVENT ZONE
        #   But the GUI stil resposible where it is ENable.
    def background_tasks_window_5(self):
        print("background_tasks_window_5 - Reading data")

        # self.shared_data.START_TIME
        # self.shared_data.START_TIME
        # self.shared_data.END_DATE
        # self.shared_data.END_TIME
        print(f"CHEKC - Start Date: {self.shared_data.START_TIME}, Start Time: {self.shared_data.START_TIME}")
        print(f"CHEKC - End Date: {self.shared_data.END_DATE}, End Time: {self.shared_data.END_TIME}")

        print("<temp><temp><temp><temp><temp><temp><temp><temp><temp><temp><temp><temp><temp><temp>")
        print(self.shared_data.DICT_PRESS_STATUS_OPTIONS_n_COLORS)
        print("DONE - background_tasks_window_5")


    def finalize_window_design(self):
        ### Design & Widgets - Create the Frames ###
        self.create_main_frame()
        self.update_idletasks()  # Update layout calculations
        self.adjust_size(self.extra_width, self.extra_height)  # Adjust the window size
        return f"task {inspect.currentframe().f_code.co_name} from {self.__class__.__name__} is Done!"
    def create_frame_0(self):
        self.f0 = tk.Frame(self)
        self.f0.pack(anchor="n", padx=10, pady=5, fill='x')
        self.middle_frame = tk.Frame(self.f0)                                                                           ### Middle frame ###
        self.middle_frame.pack(side="left", fill='x', expand=True)                                                      # Use fill and expand to ensure this frame takes up the remaining space
    def animate_loading(self):
        if self.animate_flag and hasattr(self, 'loading_label'):                                                        # Check if the loading label still exists AND the Flag
            self.loading_frame_index = (self.loading_frame_index + 1) % len(self.loading_frames)                        # Update the image to the next frame
            self.loading_label.config(image=self.loading_frames[self.loading_frame_index])
            self.loading_label.image = self.loading_frames[self.loading_frame_index]
            self.after(50, self.animate_loading)                                                                        # Call this function again after a delay to get the next frame # 100ms delay, adjust as needed
    def start_loading_animation(self):
        animation_resize = [200, 40]
        self.animate_flag = True                                                                                        # Logic to stop the loop
        if ANIMATION_OR_PICTURE_FLAG:
            self.loading_frame_index = 0
            self.loading_frames = []                                                                                    # List to hold each frame
            frames_folder = os.path.join('src', 'media', 'loading_frames')
            for frame_file in sorted(os.listdir(frames_folder)):                                                        # Load each frame into the list
                frame_path = os.path.join(frames_folder, frame_file)
                frame_image = Image.open(frame_path)
                frame_image_resized = frame_image.resize((animation_resize[0], animation_resize[1]), Image.ANTIALIAS)
                photo_frame = ImageTk.PhotoImage(frame_image_resized)
                self.loading_frames.append(photo_frame)
            self.loading_label = tk.Label(self.middle_frame, image=self.loading_frames[self.loading_frame_index])       # Create the label to display the frame
            self.loading_label.pack()
            self.animate_loading()
        else:
            gif_image = Image.open(os.path.join('src', 'media', 'loading_frames.gif'))                                  # Load the gif using PIL
            gif_image_resized = gif_image.resize((animation_resize[0], animation_resize[1]), Image.ANTIALIAS)           # Resize the gif
            self.loading_gif = ImageTk.PhotoImage(gif_image_resized)                                                    # Convert the resized gif to a PhotoImage for use in Tkinter
            self.loading_label = tk.Label(self.middle_frame, image=self.loading_gif)                                    # Create a label to display the gif
            self.loading_label.image = self.loading_gif                                                                 # Keep a reference to prevent garbage collection
            self.loading_label.pack()
    def stop_loading_animation(self):
        _ = {inspect.currentframe().f_code.co_name}
        self.animate_flag = False
        try:
            self.loading_label.destroy()
            self.f0.destroy()
        except Exception as e:
            APPLOGGER.error(f'{logger_explain_template(func=_, err=e)}')
    def create_main_frame(self):
        ### Main Frame ###
        self.main_frame = tk.Frame(self)  # Main Frame
        self.main_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.tmp_StringVar = tk.StringVar()
        self.tmp_StringVar.trace_add("write", self.trace_add_callback)
        self.tmp_combo = ttk.Combobox(self.main_frame, textvariable=self.tmp_StringVar, values=[0, 1])
        ### 1. Press Status widget
        self.press_status_label = tk.Label(self.main_frame, text="Press Status:", )                                     # "Press Status" - Label
        self.press_status_label.grid(row=0, column=0, sticky="w")                                                       # "Press Status" - Label location
        self.press_status_var = tk.StringVar()
        self.press_status_var.set(self.press_history[-1]['machine_state'] if self.press_history else "Printing")
        self.press_status_var.trace_add("write", self.trace_add_callback)                                               # "Press Status" - Tracer to press_status_var It's quite similar to <# self.press_status_combo.bind("<<ComboboxSelected>>", self.action_for_press_status_var) # Bind the selection event>
        self.press_status_combo = ttk.Combobox(self.main_frame, textvariable=self.press_status_var, values=[status[0] for status in self.shared_data.DICT_PRESS_STATUS_OPTIONS_n_COLORS], state='readonly')
        self.press_status_combo.grid(row=1, column=0, sticky="w")
        self.last_press_status_value = self.press_status_var.get()
        ################################################################################################################# Add a gap and vertical separator
        tk.Label(self.main_frame, text="   ").grid(row=0, column=1)                                                     # Empty label for gap
        ttk.Separator(self.main_frame, orient='vertical').grid(row=0, column=1, sticky='ns', padx=5)                    # Vertical separator
        ttk.Separator(self.main_frame, orient='vertical').grid(row=1, column=1, sticky='ns', padx=5)                    # Vertical separator
        ################################################################################################################
        ### 2. Shifts widget
        self.shift_label = tk.Label(self.main_frame, text="Shift:")                                                     # "Shifts" - Label
        self.shift_label.grid(row=0, column=2, sticky="w")                                                              # "Shifts" - Label location
        self.shift_vars = [tk.BooleanVar() for _ in self.shared_data.DICT_SHIFT_OPTIONS]                                                      # Use BooleanVar for each checkbutton
        self.last_shift_var = self.press_history[-1]['shift'] if self.press_history else ["Morning"]
        for i, shift in enumerate(self.shared_data.DICT_SHIFT_OPTIONS):
            self.shift_checkbutton = tk.Checkbutton(self.main_frame, text=shift, variable=self.shift_vars[i])
            self.shift_checkbutton.grid(row=1, column=i+2 , sticky="w")
            self.shift_vars[i].set(1) if shift in self.last_shift_var else self.shift_vars[i].set(0)
            self.shift_vars[i].trace_add("write", self.trace_shift_callback)
        ### State machine based on variable name ###
        self.function_list_for_StringVar_objects = {
                                                    self.press_status_var._name: self.action_for_press_status_var,
                                                    self.tmp_StringVar._name: self.action_tmp_StringVar                          # Reqeuired # def action_for_StringVar(self, name=None, mode=None, index=None): #     self.last_shift_var = self.shift_var.get()    #     threading.Thread(target=self.base_widgets, daemon=True).start()  #     print(f"Action for {name} # {mode}, {index}")
                                                    }
        ################################################################################################################# Add a gap and vertical separator
        tk.Label(self.main_frame, text="   ").grid(row=0, column=1)                                                     # Empty label for gap
        ttk.Separator(self.main_frame, orient='vertical').grid(row=0, column=1, sticky='ns', padx=5)                    # Vertical separator
        ttk.Separator(self.main_frame, orient='vertical').grid(row=1, column=1, sticky='ns', padx=5)                    # Vertical separator
        ################################################################################################################
    @classmethod
    def create_activation_button(cls, root, command):
        text = "Activate " + cls.__name__
        return cls.create_text_button(root, command, text=text)
    def trace_add_callback(self, name=None, mode=None, index=None):
        if name in self.function_list_for_StringVar_objects:
            self.function_list_for_StringVar_objects[name](name, mode, index)
    def action_for_press_status_var(self, name=None, mode=None, index=None):
        self.last_press_status_value = self.press_status_var.get()
        self.press_status_combo.config(foreground=next((item[2] for item in self.shared_data.DICT_PRESS_STATUS_OPTIONS_n_COLORS if item[0] == self.last_press_status_value), "black"))
        self.last_shift_var = [shift_option for i, shift_option in enumerate(self.shared_data.DICT_SHIFT_OPTIONS) if self.shift_vars[i].get()]  # Collect selected shifts
        threading.Thread(target=self.base_widgets, daemon=True).start()
        self.tmp_combo.set(1)
        print(f"Action for {name} # {mode}, {index}")
    def action_tmp_StringVar(self, name=None, mode=None, index=None):
        print(f"Action for {name} # {mode}, {index}")
    def base_widgets(self):
        item = next((x for x in self.press_history if x['date'] == self._today), None)                                  # Looking for today if existed.
        if item:
            item['machine_state'] = self.last_press_status_value
            item['shift'] = self.last_shift_var
        else:
            self.press_history.append({
                                        "date": self._today,
                                        "machine_state": self.last_press_status_value,
                                        "shift": self.last_shift_var
                                    })

        update_master_json(file_name="press_history", data=self.press_history)                                          # threading.Thread(target=update_master_json, args=("press_history", self.press_history), daemon=True).start()
    def trace_shift_callback(self, *args):
        self.last_shift_var = [shift_option for k, shift_option in enumerate(self.shared_data.DICT_SHIFT_OPTIONS) if self.shift_vars[k].get()]  # Collect selected shifts
        item = next((x for x in self.press_history if x['date'] == self._today), None)                                  # Update press_history with the selected shifts
        if item:
            item['machine_state'] = self.last_press_status_value
            item['shift'] = self.last_shift_var
        else:
            self.press_history.append({
                                        "date": self._today,
                                        "machine_state": self.last_press_status_value,
                                        "shift": self.last_shift_var
                                    })
        update_master_json(file_name="press_history", data=self.press_history)








        # # Checking the press status history and setting the recent status
        # if self.press_status_history:
        #     today = datetime.today().date().isoformat()
        #     recent_status = next(
        #         (item for item in reversed(self.press_status_history) if 'date' in item and item['date'] == today),
        #         None)
        #     if recent_status:
        #         self.press_status_var.set(recent_status['machine_state'])
        #
        # # Gap and vertical separator
        # tk.Label(self.main_frame, text="   ").grid(row=0, column=2)  # Empty label for gap
        # ttk.Separator(self.main_frame, orient='vertical').grid(row=0, column=3, sticky='ns',
        #                                                        padx=5)  # Vertical separator
        #
        # # Load press data
        # with open('data/press_data.json', 'r') as file:
        #     self.press_data = json.load(file)
        #
        # # Create the "Shift" part
        # shift_label = tk.Label(self.main_frame, text="Shift:")
        # shift_label.grid(row=0, column=4, sticky="w")
        #
        # # Setting up the "Shift" checkboxes
        # for i, shift in enumerate(self.shared_data.DICT_SHIFT_OPTIONS):
        #     shift_checkbutton = tk.Checkbutton(self.main_frame, text=shift, variable=self.shift_vars[i],
        #                                        onvalue=shift, offvalue="")
        #     shift_checkbutton.grid(row=0, column=i + 5)
        #
        #     # Add trace to shift_vars[i]
        #     self.shift_vars[i].trace("w", self.save_shift_data)
        #
        # # Load saved shifts and set the checkboxes accordingly
        # saved_shifts = self.press_data.get("Shift", [])
        # for i, shift in enumerate(self.shared_data.DICT_SHIFT_OPTIONS):
        #     if shift in saved_shifts:
        #         self.shift_vars[i].set(shift)
        #     else:
        #         self.shift_vars[i].set("")
        #
        # # Add another gap and vertical separator
        # tk.Label(self.main_frame, text="    ").grid(row=0, column=len(self.shared_data.DICT_SHIFT_OPTIONS) + 5)  # Empty label for gap
        # ttk.Separator(self.main_frame, orient='vertical').grid(row=0, column=len(self.shared_data.DICT_SHIFT_OPTIONS) + 6, sticky='ns',
        #                                                        padx=5)  # Vertical separator
        #
        # # "Edit FSE and Local Staff" button
        # edit_button = tk.Button(self.main_frame, text="Edit FSE and Local Staff", command=self.fse_data_gui)
        # edit_button.grid(row=0, column=len(self.shared_data.DICT_SHIFT_OPTIONS) + 7, sticky="we", padx=(20, 0))
        #
        # # Another gap and vertical separator
        # tk.Label(self.main_frame, text="    ").grid(row=0, column=len(self.shared_data.DICT_SHIFT_OPTIONS) + 8)  # Empty label for gap
        # ttk.Separator(self.main_frame, orient='vertical').grid(row=0, column=len(self.shared_data.DICT_SHIFT_OPTIONS) + 9, sticky='ns',
        #                                                        padx=5)  # Vertical separator
        #
        # # "DFE Version" label and entry box
        # dfe_version_label = tk.Label(self.main_frame, text="DFE Version:")
        # dfe_version_label.grid(row=0, column=len(self.shared_data.DICT_SHIFT_OPTIONS) + 10)
        #
        # self.dfe_version_var = tk.StringVar()
        # self.dfe_version_var.set(self.press_data.get("DFE Version", ""))
        # dfe_version_entry = tk.Entry(self.main_frame, textvariable=self.dfe_version_var)
        # dfe_version_entry.grid(row=0, column=len(self.shared_data.DICT_SHIFT_OPTIONS) + 11)
        #
        # # Function to update DFE version and its change date in JSON
        # def update_dfe_version(*args):
        #     self.press_data['DFE Version'] = self.dfe_version_var.get()
        #     self.press_data['DFE Version Change Date'] = datetime.now().strftime('%Y-%m-%d')
        #     with open('data/press_data.json', 'w') as file:
        #         json.dump(self.press_data, file)
        #
        # # Add trace to dfe_version_var
        # self.dfe_version_var.trace("w", update_dfe_version)
        #
        # # Another gap and vertical separator
        # tk.Label(self.main_frame, text="    ").grid(row=0, column=len(self.shared_data.DICT_SHIFT_OPTIONS) + 12)  # Empty label for gap
        # ttk.Separator(self.main_frame, orient='vertical').grid(row=0, column=len(self.shared_data.DICT_SHIFT_OPTIONS) + 13, sticky='ns',
        #                                                        padx=5)  # Vertical separator
        #
        # # "Select press" button
        # change_sn_button = tk.Button(self.main_frame, text="Select press", command=select_number_window)
        # change_sn_button.grid(row=0, column=len(self.shared_data.DICT_SHIFT_OPTIONS) + 14)
        #
        # # Finally, place the main_frame in the window
        # self.main_frame.grid(row=0, column=0, sticky="we", padx=5, pady=5)


    # def save_shift_data(self, *args):
    #     # Update the shifts in the press data
    #     self.press_data["Shift"] = [var.get() for var in self.shift_vars if var.get()]
    #
    #     # Save the updated press data
    #     with open('data/press_data.json', 'w') as file:
    #         json.dump(self.press_data, file, indent=2)

########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################

# def update_dfe_version(*args):
#     # Extracted from your code
#     main_app.press_data['DFE Version'] = main_app.dfe_version_var.get()
#     main_app.press_data['DFE Version Change Date'] = datetime.now().strftime('%Y-%m-%d')
#     with open('data/press_data.json', 'w') as file:
#         json.dump(main_app.press_data, file)
# def delete_row(container, row, status_vars, row_counters):
#     for widget in container.grid_slaves(row=row):
#         widget.destroy()
#     del status_vars[id(container), row]
#     row_counters[container] -= 1
# def create_row(container, name, status, row, status_vars, row_counters):
#     name_entry = tk.Entry(container)
#     status_var = tk.IntVar(value=1 if status == "Active" else 0)
#     check = tk.Checkbutton(container, variable=status_var)
#     if status == "Active":
#         check.select()
#     del_button = tk.Button(container, text="Delete", command=lambda row=row: delete_row(container, row, status_vars, row_counters))
#
#     check.grid(row=row, column=0)
#     name_entry.grid(row=row, column=1)
#     name_entry.insert(0, name)
#     del_button.grid(row=row, column=2)
#
#     status_vars[id(container), row] = status_var, name_entry
#
# def add_person(container, status_vars, row_counters):
#     row = row_counters[container]
#     create_row(container, "", "Active", row, status_vars, row_counters)
#     row_counters[container] += 1
# def save_data_fse(row_counters, status_vars, original_keys):
#     data = {}
#     for container in row_counters:
#         key = original_keys[id(container)]
#         rows = sorted(i for i in status_vars if i[0] == id(container))  # get all valid rows in this container
#         data[key] = [{"name": status_vars[row][1].get(), "status": "Active" if status_vars[row][0].get() else "Inactive"} for row in rows]
#
#     with open('data/fse_data.json', 'w') as file:
#         json.dump(data, file, indent=2)
#     main_app.window.destroy()
