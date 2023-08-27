# TODO: 2023-08-23
#           # LOADING DATA: Still waiting to the data to be loaded.
#               * Only the constant data can be edit. keep "animation loader" on the EVENT ZONE
#               * But the GUI still responsible where it is Enable.
#           # FEATURES
#           # BUTTONS
import json
import os
from datetime import datetime
import inspect
import threading
import time
from src.scripts.system.config import DMD
from src.scripts.system.applogger import APPLOGGER
from src.scripts.gui.windows.win_utility import SHARE_DATA, BaseWindow, logger_explain_template, register_thread, create_tooltip, daniel
from src.scripts.system.utilities_functions import update_master_json, read_master_json
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
class Window_SUPPORTER(BaseWindow):
    default_values = {
        "category": "Category A",
        "start_time": "00:00",
        "middle_time": "01:00",
        "end_time": "02:00",
        "description": "Description Here..."
    }
    def __init__(self, root, manager, shared_data=None, relation=None, extra_width=0, extra_height=0):
        super().__init__(root, manager, shared_data, relation, extra_width, extra_height, adjust_size=True)
        self.T = "Window_SUPPORTER"
        self.title("V12 Daily Report")
        self.extra_width = extra_width
        self.extra_height = extra_height
        self.max_height = int(self.winfo_screenheight() * 0.8) + self.extra_height                                      # Set maximum height and width based on the screen dimensions
        self.max_width = int(self.winfo_screenwidth() * 0.8) + self.extra_width
        self.f0 = None
        self.top_constant_data_frame= None
        self.setup_main_frame = None
        ### RESET WINDOW PARAM ###
        self.initialization_win_supporter()
        ################################################################################################################
    def initialization_win_supporter(self):
        self.press_history = read_master_json().get("press_history", {}).get("data", [])
        self.press_data = read_master_json().get("press_data", {}).get("data", [])
        self.fse_data = read_master_json().get("fse_data", {}).get("data", [])
        self.frame_max_h = 0
        self.frame_max_w = 0
        self.create_frame_0()
        self.load_media()
        self.start_loading_animation()
        if SHARE_DATA.METADATA["ANIMATION_OR_PICTURE_FLAG"]:
            self.animate_loading()
        self.create_top_constant_data_frame()
        self.rows = []
        self.setup_ui()
    def log_action(self, action):                                                                                       # Designated Logger usage
        APPLOGGER.info(f"{action}")
        print(action)
    def enter_to_win_supporter(self):                                                                                # The Gate to window_5 - Happened Any "Show"
        # TODO: Still waiting to the data to be loaded.
        #   Only the constant data can be edit. keep "animation loader" on the EVENT ZONE
        #   But the GUI stil resposible where it is ENable.
        self._today = SHARE_DATA.END_DATE
        self._today_time = SHARE_DATA.END_TIME
        self._start_date = SHARE_DATA.START_DATE
        self._start_time = SHARE_DATA.START_TIME
        daniel(_val=self._today, _name="self._today")
        background_tasks_window_5 = threading.Thread(name="background_tasks_window_5", target=self.background_tasks_window_5, daemon=True)                                               # Schedule the design of the window in a background thread
        register_thread(background_tasks_window_5)
        background_tasks_window_5.start()
    def background_tasks_window_5(self):
        print("background_tasks_window_5 - Reading data")
        for i in range(5):
            print(f"{i} # <temp><temp><temp><temp><temp><temp><temp><temp><temp><temp><temp><temp><temp><temp>")
            print(f"CHEKC - Start Date: {self.shared_data.START_DATE}, Start Time: {self.shared_data.START_TIME}")
            print(f"CHEKC - End Date: {self.shared_data.END_DATE}, End Time: {self.shared_data.END_TIME}")
            time.sleep(1)
        print(self.shared_data.METADATA["DICT_PRESS_STATUS_OPTIONS_n_COLORS"])
        print("DONE - background_tasks_window_5")
    def create_frame_0(self):
        self.f0 = tk.Frame(self)
        self.f0.pack(anchor="n", fill=tk.BOTH, expand=False)
    def load_media(self):
        animation_resize = [400, 80]
        self.animate_flag = True                                                                                        # Logic to stop the loop
        if SHARE_DATA.METADATA["ANIMATION_OR_PICTURE_FLAG"]:                                                            # SHARE_DATA.METADATA.get("ANIMATION_OR_PICTURE_FLAG", DMD.ANIMATION_OR_PICTURE_FLAG):
            self.loading_frame_index = 0
            self.loading_frames = []                                                                                    # List to hold each frame
            frames_folder = os.path.join('src', 'media', 'loading_frames')
            for frame_file in sorted(os.listdir(frames_folder)):                                                        # Load each frame into the list
                frame_path = os.path.join(frames_folder, frame_file)
                frame_image = Image.open(frame_path)
                frame_image_resized = frame_image.resize((animation_resize[0], animation_resize[1]), Image.ANTIALIAS)
                photo_frame = ImageTk.PhotoImage(frame_image_resized)
                self.loading_frames.append(photo_frame)
        else:
            gif_image = Image.open(os.path.join('src', 'media', 'loading_frames.gif'))                                  # Load the gif using PIL
            gif_image_resized = gif_image.resize((animation_resize[0], animation_resize[1]), Image.ANTIALIAS)           # Resize the gif
            self.loading_gif = ImageTk.PhotoImage(gif_image_resized)                                                    # Convert the resized gif to a PhotoImage for use in Tkinter
    def start_loading_animation(self):
        if SHARE_DATA.METADATA.get("ANIMATION_OR_PICTURE_FLAG", DMD.ANIMATION_OR_PICTURE_FLAG):
            self.loading_label = tk.Label(self.f0, image=self.loading_frames[self.loading_frame_index])                 # Create the label to display the frame
            self.loading_label.pack()
        else:
            self.loading_label = tk.Label(self.f0, image=self.loading_gif)                                              # Create a label to display the gif
            self.loading_label.image = self.loading_gif                                                                 # Keep a reference to prevent garbage collection
            self.loading_label.pack()
    def animate_loading(self):
        if self.animate_flag and hasattr(self, 'loading_label'):                                                        # Check if the loading label still exists AND the Flag
            self.loading_frame_index = (self.loading_frame_index + 1) % len(self.loading_frames)                        # Update the image to the next frame
            self.loading_label.config(image=self.loading_frames[self.loading_frame_index])
            self.loading_label.image = self.loading_frames[self.loading_frame_index]
            self.after(50, self.animate_loading)                                                                        # Call this function again after a delay to get the next frame # 100ms delay, adjust as needed
            self.geometry(f"{self.f0.winfo_reqwidth()}x{self.f0.winfo_reqheight()}")
    def stop_loading_animation(self):
        _ = {inspect.currentframe().f_code.co_name}
        self.geometry(f"{self.frame_max_w+100}x{self.frame_max_h+100}")
        self.animate_flag = False
        try:
            self.loading_label.destroy()
            self.f0.destroy()
        except Exception as e:
            APPLOGGER.error(f'{logger_explain_template(func=_, err=e)}')
    def create_top_constant_data_frame(self):
        ### Main Frame ###
        self.top_constant_data_frame = tk.Frame(self, bg="blue")                                                        # Main Frame
        self.top_constant_data_frame.pack(fill=tk.BOTH, expand=False)
        self.ref_widget_height = 1
        # self.tmp_StringVar = tk.StringVar()
        # self.tmp_StringVar.trace_add("write", self.trace_add_callback)
        # self.tmp_combo = ttk.Combobox(self.top_constant_data_frame, textvariable=self.tmp_StringVar, values=[0, 1])
        ### 1. Press Status widget
        self.press_status_label = tk.Label(self.top_constant_data_frame, text="Press Status:", height=self.ref_widget_height)                          # "Press Status" - Label
        self.press_status_label.grid(row=0, column=0, sticky="w")                                                       # "Press Status" - Label location
        self.press_status_var = tk.StringVar()
        self.press_status_var.set(self.press_history[-1]['machine_state'] if self.press_history else "Printing")
        self.press_status_var.trace_add("write", self.trace_add_callback)                                               # "Press Status" - Tracer to press_status_var It's quite similar to <# self.press_status_combo.bind("<<ComboboxSelected>>", self.action_for_press_status_var) # Bind the selection event>
        self.press_status_combo = ttk.Combobox(self.top_constant_data_frame, textvariable=self.press_status_var, values=[status[0] for status in self.shared_data.METADATA["DICT_PRESS_STATUS_OPTIONS_n_COLORS"]], state='readonly', height=self.ref_widget_height)
        self.press_status_combo.grid(row=1, column=0, sticky="w")
        self.last_press_status_value = self.press_status_var.get()
        ################################################################################################################ Add a gap and vertical separator
        # tk.Label(self.top_constant_data_frame, text="").grid(row=0, column=1)                                        # Empty label for gap
        ttk.Separator(self.top_constant_data_frame, orient='vertical').grid(row=0, column=1, sticky='ns', padx=5)       # Vertical separator
        ttk.Separator(self.top_constant_data_frame, orient='vertical').grid(row=1, column=1, sticky='ns', padx=5)       # Vertical separator
        ################################################################################################################
        ### 2. Shifts widget
        self.shift_label = tk.Label(self.top_constant_data_frame, text="Shift:", height=self.ref_widget_height)                                        # "Shifts" - Label
        self.shift_label.grid(row=0, column=2, sticky="w")                                                              # "Shifts" - Label location
        self.shift_vars = [tk.BooleanVar() for _ in self.shared_data.METADATA["DICT_SHIFT_OPTIONS"]]                                # Use BooleanVar for each checkbutton
        self.last_shift_var = self.press_history[-1]['shift'] if self.press_history else ["Morning"]
        for i, shift in enumerate(self.shared_data.METADATA["DICT_SHIFT_OPTIONS"]):
            self.shift_checkbutton = tk.Checkbutton(self.top_constant_data_frame, text=shift, variable=self.shift_vars[i], height=self.ref_widget_height)
            self.shift_checkbutton.grid(row=1, column=i + 2, sticky="w")
            self.shift_vars[i].set(1) if shift in self.last_shift_var else self.shift_vars[i].set(0)
            self.shift_vars[i].trace_add("write", self.trace_status_and_shift_callback)
        ### State machine based on variable name ###
        self.function_list_for_StringVar_objects = {
            self.press_status_var._name: self.action_for_press_status_var,
            # self.tmp_StringVar._name: self.action_tmp_StringVar                                                         # Reqeuired # def action_for_StringVar(self, name=None, mode=None, index=None): #     self.last_shift_var = self.shift_var.get()    #     threading.Thread(target=self.trace_status_and_shift_callback, daemon=True).start()  #     print(f"Action for {name} # {mode}, {index}")
        }
        ################################################################################################################ Add a gap and vertical separator
        last_column = self.get_last_column_with_widget(self.top_constant_data_frame)
        ttk.Separator(self.top_constant_data_frame, orient='vertical').grid(row=0, column=last_column+1, sticky='ns', padx=5)       # Vertical separator
        ttk.Separator(self.top_constant_data_frame, orient='vertical').grid(row=1, column=last_column+1, sticky='ns', padx=5)       # Vertical separator
        ################################################################################################################
        # Add the "Edit FSE and Local Staff" part
        last_column = self.get_last_column_with_widget(self.top_constant_data_frame)
        edit_button = tk.Button(self.top_constant_data_frame, text="Edit FSE and Local Staff", command=self.fse_data_gui, height=self.ref_widget_height*2)
        edit_button.grid(row=0, column=last_column+1, rowspan=2, sticky="w")
        ################################################################################################################ Add a gap and vertical separator
        last_column = self.get_last_column_with_widget(self.top_constant_data_frame)
        ttk.Separator(self.top_constant_data_frame, orient='vertical').grid(row=0, column=last_column+1, sticky='ns', padx=5)       # Vertical separator
        ttk.Separator(self.top_constant_data_frame, orient='vertical').grid(row=1, column=last_column+1, sticky='ns', padx=5)       # Vertical separator
        ################################################################################################################
        # Add the "Edit FSE and Local Staff" part
        last_column = self.get_last_column_with_widget(self.top_constant_data_frame)
        press_data_edit_button = tk.Button(self.top_constant_data_frame, text="Press Vresions", command=self.press_data_gui, height=self.ref_widget_height*2)
        press_data_edit_button.grid(row=0, column=last_column+1, rowspan=2, sticky="w")
        ################################################################################################################ Add a gap and vertical separator
        last_column = self.get_last_column_with_widget(self.top_constant_data_frame)
        ttk.Separator(self.top_constant_data_frame, orient='vertical').grid(row=0, column=last_column+1, sticky='ns', padx=5)       # Vertical separator
        ttk.Separator(self.top_constant_data_frame, orient='vertical').grid(row=1, column=last_column+1, sticky='ns', padx=5)       # Vertical separator
        ################################################################################################################
    def press_data_gui(self):                                                                                           # TODO: Insert APPLOGGER TO THIS FUNCTIONALITY
        def initialize_press_data():
            _tmp = {
                "DFE Version": [
                    {
                        "date": SHARE_DATA.METADATA["DFE_VERSION_DATE"],
                        "version": SHARE_DATA.METADATA["DFE_VERSION"],
                        "status": "Inactive"
                    }
                ],
                "SW Version": [
                    {
                        "date": SHARE_DATA.METADATA["SW_VERSION_DATE"],
                        "version": SHARE_DATA.METADATA["SW_VERSION"],
                        "status": "Inactive"
                    }
                ],
                "PLC Version": [
                    {
                        "date": SHARE_DATA.METADATA["PLC_VERSION_DATE"],
                        "version": SHARE_DATA.METADATA["PLC_VERSION"],
                        "status": "Inactive"
                    }
                ]
            }
            self.press_data.append(_tmp)
        def create_row(container, version, status, name, row, status_vars, row_counters):
            name_entry = tk.Entry(container)
            status_var = tk.IntVar(value=1 if status == "Active" else 0)
            check = tk.Checkbutton(container, variable=status_var)
            if status == "Active":
                check.select()
            check.grid(row=row, column=0)
            name_entry.grid(row=row, column=1)
            name_entry.insert(0, version)
            status_vars[id(container), row] = status_var, name_entry
        def save_press_version_data(row_counters, status_vars, original_keys):
            for container in row_counters:
                key = original_keys[id(container)]
                rows = sorted(i for i in status_vars if i[0] == id(container))  # get all valid rows in this container
                _tmp = [{"date": self._today if status_vars[row][0].get() else self.press_data[0][key][0]["date"],
                         "version": status_vars[row][1].get() if status_vars[row][0].get() else self.press_data[0][key][0]["version"],
                         "status": "Active" if status_vars[row][0].get() else "Inactive"
                         } for row in rows]
                self.press_data[0][key] = _tmp
            update_master_json(file_name="press_data", data=self.press_data)
            self.window.destroy()
        def load_and_create_versions_window():
            self.window = tk.Toplevel(self.master)
            self.window.title("Press Versions")
            if not len(self.press_data):
                initialize_press_data()
            data = self.press_data[0]
            row_counters = {}
            status_vars = {}
            original_keys = {}
            for i, (key, values) in enumerate(data.items()):
                frame = tk.LabelFrame(self.window, text=key)
                frame.grid(row=0, column=i, padx=10, pady=10, sticky='ns')
                row_counters[frame] = 0
                original_keys[id(frame)] = key
                if isinstance(values, list):
                    for value in values:
                        row = row_counters[frame]
                        create_row(frame, value.get('version', ''), value.get('status', ''), value.get('date', ''), row, status_vars, row_counters)
                        row_counters[frame] += 1
                else:
                    row = row_counters[frame]
                    create_row(frame, value.get('version', ''), value.get('status', ''), value.get('date', ''), row, status_vars, row_counters)
                    row_counters[frame] += 1
            save_button = tk.Button(self.window, text="Save", command=lambda: save_press_version_data(row_counters, status_vars, original_keys))
            save_button.grid(row=1, column=0, columnspan=3, sticky='we')
            self.window.mainloop()
        load_and_create_versions_window()
    def fse_data_gui(self):                                                                                             # TODO: Insert APPLOGGER TO THIS FUNCTIONALITY
        def delete_row(container, row, status_vars, row_counters):
            for widget in container.grid_slaves(row=row):
                widget.destroy()
            del status_vars[id(container), row]
            row_counters[container] -= 1
        def create_row(container, name, status, row, status_vars, row_counters):
            name_entry = tk.Entry(container)
            status_var = tk.IntVar(value=1 if status == "Active" else 0)
            check = tk.Checkbutton(container, variable=status_var)
            if status == "Active":
                check.select()
            del_button = tk.Button(container, text="Delete", command=lambda row=row: delete_row(container, row, status_vars, row_counters))
            check.grid(row=row, column=0)
            name_entry.grid(row=row, column=1)
            name_entry.insert(0, name)
            del_button.grid(row=row, column=2)
            status_vars[id(container), row] = status_var, name_entry
        def add_person(container, status_vars, row_counters):
            row = row_counters[container]
            create_row(container, "", "Active", row, status_vars, row_counters)
            row_counters[container] += 1
        def save_data_fse(row_counters, status_vars, original_keys):
            for container in row_counters:
                key = original_keys[id(container)]
                rows = sorted(i for i in status_vars if i[0] == id(container))  # get all valid rows in this container
                _tmp = [{"name": status_vars[row][1].get(), "status": "Active" if status_vars[row][0].get() else "Inactive"} for row in rows]
                self.fse_data[0][key] = [d for d in _tmp if d['name'] != '']
            update_master_json(file_name="fse_data", data=self.fse_data)
            self.window.destroy()
        def initialize_fse_data():
            _tmp = {
                    "WWTS FSE": [
                                    {
                                    "name": "Write Your Name...",
                                    "status": "Inactive"
                                    }
                                ],
                    "Local FSE": [
                                    {
                                    "name": "AAAAA",
                                    "status": "Inactive"
                                    }
                                ],
                    "Local T3 / other": [
                                    {
                                    "name": "BBBBBB",
                                    "status": "Inactive"
                                    }
                                ]
                    }
            self.fse_data.append(_tmp)
        def load_and_create_fse_window():
            self.window = tk.Toplevel(self.master)
            self.window.title("FSE Data")
            if not len(self.fse_data):
                initialize_fse_data()
            data = self.fse_data[0]
            row_counters = {}
            status_vars = {}
            original_keys = {}
            for i, (key, values) in enumerate(data.items()):
                frame = tk.LabelFrame(self.window, text=key)
                frame.grid(row=0, column=i, padx=10, pady=10, sticky='ns')
                row_counters[frame] = 0
                original_keys[id(frame)] = key
                if isinstance(values, list):
                    for value in values:
                        row = row_counters[frame]
                        create_row(frame, value.get('name', ''), value.get('status', ''), row, status_vars,
                                   row_counters)
                        row_counters[frame] += 1
                else:
                    row = row_counters[frame]
                    create_row(frame, values.get('name', ''), values.get('status', ''), row, status_vars, row_counters)
                    row_counters[frame] += 1
                add_button = tk.Button(frame, text="Add Person", command=lambda frame=frame: add_person(frame, status_vars, row_counters))
                add_button.grid(row=1000, columnspan=3)
            save_button = tk.Button(self.window, text="Save", command=lambda: save_data_fse(row_counters, status_vars, original_keys))
            save_button.grid(row=1, column=0, columnspan=3, sticky='we')
            self.window.mainloop()
        load_and_create_fse_window()
    def get_last_column_with_widget(self, container):
        last_column = 0
        for widget in container.grid_slaves():
            col = widget.grid_info()['column']  # Get the column of the widget
            if col > last_column:
                last_column = col
        return last_column
    def trace_add_callback(self, name=None, mode=None, index=None):
        if name in self.function_list_for_StringVar_objects:
            self.function_list_for_StringVar_objects[name](name, mode, index)
    def action_for_press_status_var(self, name=None, mode=None, index=None):
        threading.Thread(target=self.trace_status_and_shift_callback, daemon=True).start()
        self.log_action(f"Action for {name} # {mode}, {index}")
    def action_tmp_StringVar(self, name=None, mode=None, index=None):
        self.log_action(f"Action for {name} # {mode}, {index}")
    def trace_status_and_shift_callback(self, *args):
        self.last_press_status_value = self.press_status_var.get()
        # self.press_status_combo.config(foreground=next((item[2] for item in self.shared_data.METADATA["DICT_PRESS_STATUS_OPTIONS_n_COLORS"] if item[0] == self.last_press_status_value), "black"))
        self.last_shift_var = [shift_option for k, shift_option in enumerate(self.shared_data.METADATA["DICT_SHIFT_OPTIONS"]) if self.shift_vars[k].get()]  # Collect selected shifts
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
    def setup_ui(self):
        self.setup_main_frame = tk.Frame(self, bg="orange")
        self.setup_main_frame.pack(anchor='n', fill=tk.X, expand=False)

        # Create the headers first
        self.frame_top_canvas = tk.Frame(self.setup_main_frame, bg="lightgray")
        self.frame_top_canvas.pack(anchor='n', fill=tk.X, expand=False)
        self.create_headers()


        self.canvas = tk.Canvas(self.setup_main_frame, bg="purple")
        self.canvas.pack(anchor='n', side=tk.LEFT, fill=tk.X, expand=True)


        self.scrollbar = tk.Scrollbar(self.setup_main_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y, expand=False)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)


        # TODO: STOP HERE

        self.frame_inside_canvas = tk.Frame(self.canvas, bg="cyan")
        self.canvas_frame = self.canvas.create_window((0, 0), window=self.frame_inside_canvas, anchor="nw")
        self.canvas.bind('<Configure>', self.on_canvas_resize)                                                          # Bind the resize event to the canvas
        for i in range(7):                                                                                              # Configure rows and columns for resizing # Configures the behavior of the grid geometry manager. By setting the weight attribute, it ensures that when the containing widget is resized, each of these rows or columns also resizes proportionally. When we have equal weight like (frame_inside_canvas and the single column of main_frame and canvas), so they'll expand or shrink equally when their parent widget's size changes.
            self.frame_top_canvas.columnconfigure(i, weight=1)
            self.frame_inside_canvas.columnconfigure(i, weight=1)

        self.setup_main_frame.columnconfigure(0, weight=1)
        self.setup_main_frame.rowconfigure(0, weight=1)
        self.canvas.columnconfigure(0, weight=1)
        self.canvas.rowconfigure(0, weight=1)

        self.add_main_btn = tk.Button(self.frame_inside_canvas, text="Add Row", command=self.add_row)                   # Define add_main_btn but don't grid it yet. It will be gridded in add_row()
        self.add_row()
    def on_close(self):
        self.manager.windows["Window_4"].activate_deactivate_pic_images(flag=False)
        for widget in self.winfo_children():
            print(widget)
            widget.destroy()
        self.initialization_win_supporter()
        self.manager.windows["Window_4"].activate_deactivate_pic_images(flag=True)
        super().on_close()
    def show(self):
        super().show()                                                                                                  # Call the parent class's show method to actually display the window
        self.enter_to_win_supporter()
    @classmethod
    def create_activation_button(cls, root, command):
        text = "Activate " + cls.__name__
        return cls.create_text_button(root, command, text=text)

    def create_headers(self):
        headers = ["Category", "Start Time", "Middle Time", "End Time", "Description", "Function", "Actions"]
        for idx, header in enumerate(headers):
            label = tk.Label(self.frame_top_canvas, text=header, font=("Arial", 10, "bold"), bg="lightgray", relief=tk.RAISED)
            label.grid(row=0, column=idx, sticky='ew')

    def add_row(self):                                                                                                  # Function to add a new row of widgets to the canvas frame.
        _row_widgets = []                                                                                               # Initialize the list to hold this row's widgets
        categories = ["Category A", "Category B (Enables Middle Time)", "Category C"]
        category_dropdown = ttk.Combobox(self.frame_inside_canvas, values=categories)
        category_dropdown.set(self.default_values["category"])
        category_dropdown.bind("<<ComboboxSelected>>", lambda e, dd=category_dropdown: self.on_category_change(dd))
        category_dropdown.grid(row=len(self.rows), column=0, sticky='ew')
        _row_widgets.append(category_dropdown)
        ### TIMES ###
        times = ["00:00", "01:00", "02:00", "..."]
        start_time_dropdown = ttk.Combobox(self.frame_inside_canvas, values=times)
        start_time_dropdown.set(self.default_values["start_time"])
        start_time_dropdown.grid(row=len(self.rows), column=1, sticky='ew')
        _row_widgets.append(start_time_dropdown)
        middle_time_dropdown = ttk.Combobox(self.frame_inside_canvas, values=times, state="disabled")
        middle_time_dropdown.set(self.default_values["middle_time"])
        middle_time_dropdown.grid(row=len(self.rows), column=2, sticky='ew')
        _row_widgets.append(middle_time_dropdown)
        end_time_dropdown = ttk.Combobox(self.frame_inside_canvas, values=times)
        end_time_dropdown.set(self.default_values["end_time"])
        end_time_dropdown.grid(row=len(self.rows), column=3, sticky='ew')
        _row_widgets.append(end_time_dropdown)
        ### Description ###
        description_text = tk.Text(self.frame_inside_canvas, height=1, width=20)
        description_text.insert(tk.END, self.default_values["description"])
        description_text.grid(row=len(self.rows), column=4, sticky='ew')
        _row_widgets.append(description_text)
        ### Function Place-holder ###
        placeholder_btn = tk.Button(self.frame_inside_canvas, text="Button", command=lambda row_num=len(self.rows), row_widgets=_row_widgets: self.handle_placeholder_btn_action(row_num, row_widgets))
        placeholder_btn.grid(row=len(self.rows), column=5, sticky='ew')
        _row_widgets.append(placeholder_btn)
        ### Delete button ###
        del_btn = tk.Button(self.frame_inside_canvas, text="Delete", command=lambda row_num=len(self.rows): self.delete_row(row_num))
        del_btn.grid(row=len(self.rows), column=6, sticky='ew')
        _row_widgets.append(del_btn)
        ### Widget list ###
        self.rows.append(_row_widgets)                                                                                  # Instead of rows.append([category_dropdown, start_time_dropdown, middle_time_dropdown, end_time_dropdown, description_text, placeholder_btn, del_btn])
        self.add_main_btn.grid(row=len(self.rows), columnspan=7)                                                        # Shift the add_main_btn below the last row (span across all columns)
        self.resize_window_and_scrollregion()                                                                           # Resize the root window dynamically
        self.log_action(f"Adding row # {len(self.rows)} to {self.rows}")
    def handle_placeholder_btn_action(self, row_num, row_widgets):
        category = row_widgets[0].get()
        start_time = row_widgets[1].get()
        middle_time = row_widgets[2].get()
        end_time = row_widgets[3].get()
        description = row_widgets[4].get("1.0", "end-1c")                                                               # Gets text from the Text widget
        self.log_action(f"Button #{row_num} Data >>> Category: {category}, Start: {start_time}, Middle: {middle_time}, End: {end_time}, Description: {description}")
    def delete_row(self, target_row_num):                                                                               # Function to delete a specific row of widgets.
        self.log_action(f"Deleting row # {target_row_num} from {self.rows}")
        for widget in self.rows[target_row_num]:                                                                        # Destroy all the widgets in the target row
            widget.destroy()
        self.rows.pop(target_row_num)                                                                                   # Remove the row from the rows list
        for inx, row_widgets in enumerate(self.rows[target_row_num:], start=target_row_num):                            # Re-grid all the widgets below the deleted row
            for j, widget in enumerate(row_widgets):
                widget.grid(row=inx, column=j, sticky='ew')
        for indx in range(target_row_num, len(self.rows)):                                                              # Update the command for all delete buttons below the deleted row
            self.rows[indx][-1]['command'] = lambda row_num=indx: self.delete_row(row_num)
        self.add_main_btn.grid(row=len(self.rows), columnspan=7)                                                        # Shift the add_main_btn below the last row (span across all columns)
        self.resize_window_and_scrollregion()                                                                           # Adjust the canvas's scroll region after deleting widgets
        self.log_action(f"The updated rows list ({len(self.rows)}): {self.rows}")
    def resize_window_and_scrollregion(self):
        if not self.rows:
            return                                                                                                      # Return if no rows exist
        estimated_widget_height = self.rows[0][0].winfo_reqheight() + 5                                                 # Assuming an average widget height of 30 pixels
        total_height = estimated_widget_height * (len(self.rows)) + self.top_constant_data_frame.winfo_reqheight()  # +1 for some buffer space
        total_width = sum(widget.winfo_reqwidth() for widget in self.rows[0])                                           # Calculate total width based on the width of all widgets in the first row. (Assuming all rows have the same width.)
        scrollbar_width = self.scrollbar.winfo_width()                                                                  # Account for scrollbar width.
        total_width += scrollbar_width
        self.frame_max_h = max(self.frame_max_h, total_height)
        self.frame_max_w = max(self.frame_max_w, total_width)
        self.frame_inside_canvas.config(height=total_height)                                                            # Configure the height of the frame_inside_canvas
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))                                                     # Update the canvas's scroll region
        self.canvas.yview_moveto(1)                                                                                     # Scroll to the bottom
    def on_category_change(self, category_dropdown):
        if category_dropdown.get() == "Category B (Enables Middle Time)":
            self.rows[category_dropdown.grid_info()["row"]][2].configure(state="normal")
        else:
            self.rows[category_dropdown.grid_info()["row"]][2].configure(state="disabled")
    def on_mousewheel(self, event):
        """
        It's called whenever the user scrolls the mouse wheel. It adjusts the scroll position of the canvas (yview
        The event.delta returns a positive value if the scroll is upwards and a negative value if the scroll is downwards.
        Multiplying by -1 ensures the scroll direction feels natural.
        Dividing by 120 normalizes this delta to handle scroll speed across different OS and devices
        :param event:
        :return:
        """
        self.canvas.yview_scroll(-1 * (event.delta // 120), "units")
    def on_canvas_resize(self, event):                                                                                  # Set the width of frame_inside_canvas to be the width of canvas minus scrollbar width
        canvas_width = event.width - self.scrollbar.winfo_width() + 5                                                   # +5 find-tune
        self.canvas.itemconfig(self.canvas_frame, width=canvas_width)
