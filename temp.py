# print("\nauthor\t:\tDaniel Biton\ndate\t:\t2023-08-23\nversion\t:\tv001\nlicense\t:\tna\n")

import json
import os
import numpy as np
import tkinter as tk
from tkinter import ttk, Canvas, messagebox

DEFAULT_VALUES = {
    'flag': 0,
    'K': 0.0221,
    'MAX_REPEAT_LENGTH': 5330,
    'MAX_PROCESS_SPEED': 117.5,
    'DEFAULT_REPEAT_LENGTH': 5330,
    'MAX_HOURS': 24,
    'DEFAULT_HOURS': 1,
    'MAX_UTILIZATION': 100,
    'author': 'Daniel Biton',
    'date': '2023-08-27',
    'version': 'v002',
    'license': 'na'
}
JSON_FILE_PATH = 'settings.json'
class SettingsManager:
    @staticmethod
    def initialize_from_file():
        """Read settings from the JSON file and update defaults if flag is True."""
        if os.path.exists(JSON_FILE_PATH):
            with open(JSON_FILE_PATH, 'r') as f:
                data = json.load(f)
                if data.get('flag'):
                    for key, value in data.items():
                        DEFAULT_VALUES[key] = value
                else:
                    # If the file doesn't exist, create one with the default values
                    with open(JSON_FILE_PATH, 'w') as f:
                        json.dump(DEFAULT_VALUES, f, indent=4)  # Indentation added for readability
        else:
            # If the file doesn't exist, create one with the default values
            with open(JSON_FILE_PATH, 'w') as f:
                json.dump(DEFAULT_VALUES, f, indent=4)  # Indentation added for readability
    @staticmethod
    def update_settings(new_settings):
        """Update or append values in the JSON file."""
        with open(JSON_FILE_PATH, 'r') as f:
            data = json.load(f)
        for key, value in new_settings.items():
            data[key] = value
        with open(JSON_FILE_PATH, 'w') as f:
            json.dump(data, f, indent=4)  # Indentation added for readability

setting = SettingsManager()
setting.initialize_from_file()

# Extracting the values from DEFAULT_VALUES
K = DEFAULT_VALUES['K']
MAX_REPEAT_LENGTH = DEFAULT_VALUES['MAX_REPEAT_LENGTH']
MAX_PROCESS_SPEED = DEFAULT_VALUES['MAX_PROCESS_SPEED']
DEFAULT_REPEAT_LENGTH = DEFAULT_VALUES['DEFAULT_REPEAT_LENGTH']
MAX_HOURS = DEFAULT_VALUES['MAX_HOURS']
DEFAULT_HOURS = DEFAULT_VALUES['DEFAULT_HOURS']
MAX_UTILIZATION = DEFAULT_VALUES['MAX_UTILIZATION']
class MeterOutputCalculator(tk.Tk):
    def __init__(self):
        super().__init__()
        # Window configurations
        self.title("V12 Linear Meter Output Calculator")
        self.geometry(f"{int(self.winfo_screenwidth())}x{int(self.winfo_screenheight())}")
        self.pack_propagate(True)
        self.var_entry_width = 60
        self.slider_len = 400
        # Add title
        title_label = ttk.Label(self, text="V12 Linear Meter Output Calculator", font=("Arial", 24))
        title_label.pack(pady=5)
        # Add Repeat Length widget
        self.create_repeat_length_widget()
        self.create_utilization_widget()  # Add the Utilization widget
        self.create_hours_widget()
        self.create_output_widget()
    def create_repeat_length_widget(self):
        """Creates the Repeat Length widget with slider, input box, and axis."""
        frame = ttk.LabelFrame(self, text="Repeate Length [mm]", padding=(10, 5))
        frame.pack(anchor="center")
        self.repeat_length_var = tk.DoubleVar(value=DEFAULT_REPEAT_LENGTH)
        # Manual Input Box
        input_box = ttk.Entry(frame, textvariable=self.repeat_length_var, width=self.var_entry_width, justify="center")
        input_box.grid(row=0, column=0, pady=10, sticky='n')
        input_box.bind("<Return>", lambda e: self.update_repeat_length(self.repeat_length_var.get()))
        # Label for "units"
        ttk.Label(frame, text="[ mm ]").grid(row=0, column=1, sticky='w')
        # Slider
        slider = ttk.Scale(frame, from_=0, to=MAX_REPEAT_LENGTH, orient=tk.HORIZONTAL, length=self.slider_len, variable=self.repeat_length_var, command=self.update_repeat_length)
        slider.grid(row=1, column=0,  columnspan=2, pady=10)
        ttk.Label(frame, text="[0 mm]").grid(row=2, column=0,  columnspan=2, sticky='w')
        ttk.Label(frame, text="[5330 mm]").grid(row=2, column=1, sticky='e')
    def update_repeat_length(self, value):
        """Updates repeat length based on slider or input box."""
        try:
            value = float(value)
            if 0 <= value <= MAX_REPEAT_LENGTH:
                self.repeat_length_var.set(int(value))
                self.update_output()
        except ValueError:
            pass
    def create_utilization_widget(self):
        """Creates the Utilization widget with a circular button, range axis, and labels."""
        self.circ_0 = 60    # Default value is 60%
        self.circ_gap = 5
        self.w_h = 200
        self.r = self.w_h/2
        frame = ttk.LabelFrame(self, text="Utilization [%]", padding=(10, 5))
        frame.pack(anchor='center')
        frame.config(width=self.w_h, height=self.w_h)                                                                   # Setting a specific size for the frame
        frame.grid_propagate(True)                                                                                      # prevents the frame from resizing to fit its content
        self.utilization_var = tk.DoubleVar(value=self.circ_0)  # Default value is 60%
        container_frame = ttk.Frame(frame)
        container_frame.pack(pady=10)  # or any other padding you prefer
        # Your Entry widget inside the container frame
        self.utilization_entry = ttk.Entry(container_frame, textvariable=self.utilization_var, width=self.var_entry_width, justify="center")
        self.utilization_entry.pack(side=tk.LEFT)  # packed to the left side of the container frame
        self.utilization_entry.bind("<Return>", lambda e: self.on_utilization_entry_update(self.utilization_var.get()))
        ttk.Label(container_frame, text="[ % ]").pack(side=tk.LEFT, padx=5)  # packed to the left side of the container frame, after the Entry
        # Circular Button with specified width and height
        self.utilization_button = Canvas(frame, width=self.w_h, height=self.w_h, bg="lightgray")
        # Bind the events for click-and-hold behavior
        self.utilization_button.bind("<ButtonPress-1>", self.start_tracking)
        self.utilization_button.bind("<B1-Motion>", self.update_utilization)
        self.utilization_button.bind("<ButtonRelease-1>", self.stop_tracking)
        self.utilization_button.pack(expand=True, anchor="center")
        self.update_utilization_circle()
        # Range Axis and Labels
        for i in range(30, 331, self.circ_gap):                                                                         # 5% gaps, 300-degree range
            angle_rad = np.radians(i + 90)  # Convert angle to radians and offset by +90 to start from the bottom
            x1, y1 = self.r + 45 * np.cos(angle_rad), self.r + 45 * np.sin(angle_rad)
            x2, y2 = self.r + 50 * np.cos(angle_rad), self.r + 50 * np.sin(angle_rad)
            self.utilization_button.create_line(x1, y1, x2, y2, fill="black")
            if i == 30:  # Label for 0%
                x_label, y_label = self.r + 60 * np.cos(angle_rad), self.r + 60 * np.sin(angle_rad)
                self.utilization_button.create_text(x_label, y_label, text="0%")
            elif i == 105:  # Label for 25%
                x_label, y_label = self.r + 60 * np.cos(angle_rad), self.r + 60 * np.sin(angle_rad)
                self.utilization_button.create_text(x_label, y_label, text="25%")
            elif i == 180:  # Label for 50%
                x_label, y_label = self.r + 60 * np.cos(angle_rad), self.r + 60 * np.sin(angle_rad)
                self.utilization_button.create_text(x_label, y_label, text="50%")
            elif i == 255:  # Label for 75%
                x_label, y_label = self.r + 60 * np.cos(angle_rad), self.r + 60 * np.sin(angle_rad)
                self.utilization_button.create_text(x_label, y_label, text="75%")
            elif i == 330:  # Label for 100%
                x_label, y_label = self.r + 60 * np.cos(angle_rad), self.r + 60 * np.sin(angle_rad)
                self.utilization_button.create_text(x_label, y_label, text="100%")
    def on_utilization_entry_update(self, event):
        """Validates and updates the value from the Entry widget."""
        try:
            value = float(self.utilization_var.get())
            if 0 <= value <= 100:
                self.update_utilization_circle()
            else:
                messagebox.showwarning("Invalid Value", "Please enter a value between 0 and 100.")
                self.utilization_var.set(self.circ_0)  # Reset to default value
                self.update_utilization_circle()
        except ValueError:
            messagebox.showwarning("Invalid Input", "Please enter a valid number.")
            self.utilization_var.set(self.circ_0)  # Reset to default value
            self.update_utilization_circle()
        self.update_output()
    def start_tracking(self, event):
        """Initiate the tracking of mouse movement."""
        self.is_tracking = True
        self.update_utilization(event)
    def stop_tracking(self, event):
        """Stop the tracking of mouse movement."""
        self.is_tracking = False
        self.hide_hours_tooltip()
    def update_utilization(self, event):
        # Compute the difference between the event location and the center of the canvas
        dx = event.x - self.r
        dy = event.y - self.r
        # Compute the angle in radians
        angle_rad = np.arctan2(dy, dx)
        # Convert the angle to degrees and normalize it
        angle_deg = (np.degrees(angle_rad)) % 360
        if angle_deg < 90:
            angle_deg = 360+min(60, min(420, angle_deg))
            value = (angle_deg - 120) / 3
        elif angle_deg > 90:
            angle_deg = max(120, min(420, angle_deg))
            value = (angle_deg - 120) / 3
        else:
            angle_deg = 360 + (np.degrees(angle_rad))
            value = (angle_deg - 120) / 3
        self.utilization_var.set(round(value, 2))
        self.update_utilization_circle()
        self.update_output()
    def update_utilization_circle(self):
        """Updates the circle pointer on the Utilization widget."""
        self.r = self.w_h/2
        self.circ_rad = 5
        self.utilization_button.delete("pointer")  # Remove previous pointer
        angle_deg = 120 + self.utilization_var.get() * 3
        angle_rad = np.radians(angle_deg)
        x, y = self.r + 40 * np.cos(angle_rad), self.r + 40 * np.sin(angle_rad)
        self.utilization_button.create_oval(x - self.circ_rad, y - self.circ_rad, x + self.circ_rad, y + self.circ_rad,fill="black", tags="pointer")
    def create_hours_widget(self):
        """Creates the Number of Hours widget with slider, axis, and preset buttons."""
        frame = ttk.LabelFrame(self, text="Number of Hours", padding=(10, 5))
        frame.pack(anchor="center")
        self.default_interval = 1
        self.max_hours = 25
        # Entry widget for numeric input
        self.hours_var = tk.DoubleVar(value=self.default_interval)  # Default value is 1 hour
        self.hours_entry = ttk.Entry(frame, textvariable=self.hours_var, width=self.var_entry_width, justify="center")
        self.hours_entry.grid(row=0, column=0, columnspan=self.max_hours, pady=5, sticky='ew')
        # self.hours_entry.bind("<Return>", self.on_hours_entry_update)  # Triggered when user presses Enter key
        self.hours_entry.bind("<Return>", lambda e: self.on_hours_entry_update())

        # Label for "units"
        ttk.Label(frame, text="[ hours ]").grid(row=0, column=24, sticky='e')
        # Slider
        self.slider = ttk.Scale(frame, from_=0, to=25, orient=tk.HORIZONTAL, length=self.slider_len, variable=self.hours_var, command=self.on_hours_entry_update)
        self.slider.grid(row=1, column=0, columnspan=25, pady=10, sticky='n')
        # Preset buttons
        button_frame = ttk.Frame(frame)
        button_frame.grid(row=4, column=0, columnspan=25, pady=5)
        presets = [("1 HOUR", 1), ("SINGLE SHIFT", 8), ("DOUBLE SHIFTS", 16), ("TRIPLE SHIFTS", 24)]
        for index, (text, value) in enumerate(presets):
            btn = ttk.Button(button_frame, text=text, command=lambda v=value: self.set_hours(v))
            btn.grid(row=0, column=index, padx=5)
        # Bind the events for click-and-hold behavior
        self.slider.bind("<ButtonPress-1>", self.hours_start_tracking)
        self.slider.bind("<B1-Motion>", self.move_hours_tooltip)
        self.slider.bind("<ButtonRelease-1>", self.hours_stop_tracking)
    def hours_start_tracking(self, event):
        """Initiate the tracking of mouse movement."""
        self.is_tracking = True
        self.update_hours_tooltip()
    def hours_stop_tracking(self, event):
        """Stop the tracking of mouse movement."""
        self.is_tracking = False
    def set_hours(self, value):
        """Sets the hours based on the preset buttons."""
        self.hours_var.set(int(value))
        self.move_hours_tooltip()
    def update_hours_tooltip(self):
        """Updates the tooltip to show the current hours value."""
        value = self.hours_var.get()  # Convert to integer
        self.hours_var.set(round(value, 2))
        if hasattr(self, "hours_tooltip_label"):
            self.hours_tooltip_label.destroy()
    def show_hours_tooltip(self, event):
        """Displays the tooltip when the mouse hovers over the slider."""
        pass
    def move_hours_tooltip(self, event=None):
        """Updates the tooltip's position when the slider moves."""
        # First round the value to two decimal points
        current_value = self.hours_var.get()
        rounded_value = round(current_value, 2)
        self.hours_var.set(rounded_value)
        if hasattr(self, "hours_tooltip_label"):
            slider_position = int(self.hours_var.get() / 24.0 * self.slider_len)
            self.hours_tooltip_label.place(x=slider_position + self.slider.winfo_rootx() - self.winfo_rootx() - 20,
                                           y=self.slider.winfo_rooty() - self.winfo_rooty() - 30)
        self.on_hours_entry_update()

    def hide_hours_tooltip(self):
        """Hides the tooltip."""
        if hasattr(self, "hours_tooltip_label"):
            self.hours_tooltip_label.destroy()
    def on_hours_entry_update(self, event=None):
        """Validates and updates the value from the Entry widget."""
        try:
            value = self.hours_var.get()
            if 0 <= value <= 24:
                self.hours_var.set(round(value, 2))
                self.update_hours_tooltip()
            else:
                messagebox.showwarning("Invalid Value", "Please enter a value between 0 and 24.")
                self.hours_var.set(self.default_interval)  # Reset to default value
                self.update_hours_tooltip()
        except ValueError:
            messagebox.showwarning("Invalid Input", "Please enter a valid number.")
            self.hours_var.set(self.default_interval)  # Reset to default value
            self.update_hours_tooltip()
        self.update_output()
    def calculate_output(self):
        util_hour = self.utilization_var.get() * self.hours_var.get()  # Utilization multiply by the number of hours
        k_rl = self.repeat_length_var.get() / MAX_REPEAT_LENGTH
        calc = k_rl * MAX_PROCESS_SPEED * util_hour * 60 * (1/100_000)
        return calc, k_rl , util_hour
    def update_output(self):
        res, k_rl_res, util_hour_res = self.calculate_output()
        self.OUTPUT.set(round(res, 2))
        if res != 0:
            self.t_0_var.set(f"{int(res / (res / k_rl_res) * 100)}% of Repeat Length")
            self.t_1_var.set(f"25% of Absolute Utilization: {0.25 * (res / k_rl_res):.2f} [km]")
            self.t_2_var.set(f"50% of Absolute Utilization: {0.5 * (res / k_rl_res):.2f} [km]")
            self.t_3_var.set(f"100% of Absolute Utilization: {(res / k_rl_res):.2f} [km]")
        else:
            self.t_0_var.set("0% of Repeat Length")
            self.t_1_var.set(f"25% of Absolute Utilization: {0.00:.2f} [km]")
            self.t_2_var.set(f"500% of Absolute Utilization: {0.00:.2f} [km]")
            self.t_3_var.set(f"100% of Absolute Utilization: {0.00:.2f} [km]")
    def create_output_widget(self):
        frame = ttk.LabelFrame(self, text="", padding=(10, 5))
        frame.pack(anchor="center")
        # Parent frame for output and unit
        label_frame = ttk.Frame(frame)
        label_frame.pack(pady=5)
        self.OUTPUT = tk.StringVar()
        self.title_label = ttk.Label(label_frame, textvariable=self.OUTPUT, font=("Arial", 24))
        self.title_label.pack(side=tk.LEFT, padx=5)
        # Units label
        units_label = ttk.Label(label_frame, text="[ KM ]", font=("Arial", 18))
        units_label.pack(side=tk.LEFT)
        # Targets
        target_frame = ttk.Frame(frame)
        target_frame.pack(pady=5)
        self.t_0_var = tk.StringVar()
        self.t_1_var = tk.StringVar()
        self.t_2_var = tk.StringVar()
        self.t_3_var = tk.StringVar()
        ttk.Label(frame, textvariable=self.t_0_var, font=("Arial", 8)).pack(pady=5)
        ttk.Label(frame, textvariable=self.t_1_var, font=("Arial", 8)).pack(pady=5)
        ttk.Label(frame, textvariable=self.t_2_var, font=("Arial", 8)).pack(pady=5)
        ttk.Label(frame, textvariable=self.t_3_var, font=("Arial", 8)).pack(pady=5)
        # Initial update
        self.update_output()

app = MeterOutputCalculator()
app.mainloop()
