
from src.scripts.system.config import DMD
from src.scripts.system.applogger import APPLOGGER
from src.scripts.gui.windows.win_utility import SHARE_DATA, BaseWindow, logger_explain_template, create_tooltip
import time
import datetime
import os
import threading
import inspect
from PIL import Image, ImageTk, ImageEnhance
import tkinter as tk
from tkcalendar import Calendar
from src.scripts.analysis.data_loading import data_loading
from tkinter import messagebox
class Window_4(BaseWindow):
    def __init__(self, root, manager, shared_data=None, relation=None, extra_width=0, extra_height=0):
        super().__init__(root, manager, shared_data, relation, extra_width, extra_height)
        self.T = "Window_4"
        self.title("BOTH UI")
        self.extra_width = extra_width
        self.extra_height = extra_height
        self.f0 = None
        self.middle_frame = None
        self.f1 = None
        self.f2 = None
        self.f3 = None
        self.supporter_image = None
        self.press_pc_image = None
        self.loading_label = None
        self.animate_flag = None
        self.loading_frame_index = None
        self.loading_frames = None
        self.loading_gif = None
        self.button_clicked = False
        self.create_frame_0()
        self.start_loading_animation()                                                                                  # Start Animation
        threading.Thread(target=self.design_window, daemon=True).start()                                                # Schedule the design of the window in a background thread
        APPLOGGER.info(f'The <{self.T}> which is created based on (BaseWindow class) with the relations:<{relation}>, Frames and Buttons.')
    def design_window(self):                                                                                            # Finalize the design in the main thread
        task_info = (self.finalize_window_design, f"{self.__class__.__name__} - design_window")
        SHARE_DATA.TASK_QUEUE.put(task_info)                                                                            # SHARE_DATA.TASK_QUEUE.put(self.finalize_window_design)
    def finalize_window_design(self):                                                                                   ### Design & Widgets - Create the Frames ###
        self.create_frame_2()
        self.create_frame_3()
        self.initialize_tooltips()                                                                                      # Initialize the ability for toolkit
        self.update_idletasks()                                                                                         # Update layout calculations
        self.adjust_size(self.extra_width, self.extra_height)                                                           # Adjust the window size
        return f"task {inspect.currentframe().f_code.co_name} from {self.__class__.__name__} is Done!"
    def animate_loading(self):
        if self.animate_flag and hasattr(self, 'loading_label'):                                                        # Check if the loading label still exists AND the Flag
            self.loading_frame_index = (self.loading_frame_index + 1) % len(self.loading_frames)                        # Update the image to the next frame
            self.loading_label.config(image=self.loading_frames[self.loading_frame_index])
            self.loading_label.image = self.loading_frames[self.loading_frame_index]
            self.after(50, self.animate_loading)                                                                        # Call this function again after a delay to get the next frame # 100ms delay, adjust as needed
    def start_loading_animation(self):
        animation_resize = [200, 40]
        self.animate_flag = True                                                                                        # Logic to stop the loop
        if SHARE_DATA.METADATA.get("ANIMATION_OR_PICTURE_FLAG", DMD.ANIMATION_OR_PICTURE_FLAG):
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
        except Exception as e:
            APPLOGGER.error(f'{logger_explain_template(func=_, err=e)}')
    def create_frame_0(self):
        self.f0 = tk.Frame(self)
        self.f0.pack(anchor="n", padx=10, pady=5, fill='x')
        self.left_frame = tk.Frame(self.f0)                                                                             ### Left frame ###
        self.left_frame.pack(side="left", anchor="nw")
        self.return_button = tk.Button(self.left_frame, text="Return", command=self.on_close)
        self.reset_button = tk.Button(self.left_frame, text="Reset", command=self.reset_fields)
        self.middle_frame = tk.Frame(self.f0)                                                                           ### Middle frame ###
        self.middle_frame.pack(side="left", fill='x', expand=True)                                                      # Use fill and expand to ensure this frame takes up the remaining space
        self.press_sn_values = self.get_press_sn_values()                                                               # Placeholder function to get dropdown values
        self.press_sn_default_value = self.get_default_press_sn()                                                       # Placeholder function to get default value
        self.press_sn_var = tk.StringVar(value=self.press_sn_default_value)
        self.press_sn_dropdown = tk.OptionMenu(self.middle_frame, self.press_sn_var, *self.press_sn_values)
        self.right_frame = tk.Frame(self.f0)                                                                            ### Right frame ###
        self.right_frame.pack(side="right", anchor="ne")
        self.dev_var = tk.BooleanVar()
        self.dev_checkbox = tk.Checkbutton(self.right_frame, text="Dev", variable=self.dev_var, command=self.dev_checkbox_changed)
        self.azure_var = tk.BooleanVar()
        self.azure_checkbox = tk.Checkbutton(self.right_frame, text="Azure", variable=self.azure_var, state="disabled")

        # self.radius = 5  # Circle's radius
        # self.azure_flag = False  # Default value (False == Gray)
        # self.azure_canvas = tk.Canvas(self.right_frame, width=4 * self.radius, height=4 * self.radius, bg="white", highlightthickness=0)
        # self.circle = self.azure_canvas.create_oval(self.radius, self.radius, 2 * self.radius, 2 * self.radius, fill="gray")  # Default color is gray
        # self.azure_label = tk.Label(self.right_frame, text="Azure")

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
        self.set_start_button = tk.Button(self.start_frame, text="Click to set Start Date & Time", command=self.set_start, font=("Arial", 10, "bold"), state="disable")
        self.set_start_button.pack(anchor="n")
        self.start_date_var = tk.StringVar(value=self.get_current_date())
        self.start_date_entry = tk.Entry(self.start_frame, textvariable=self.start_date_var, justify='center', width=30, state='readonly')
        self.start_date_entry.pack(anchor="n", pady=5)
        self.start_time_var = tk.StringVar(value="00:01:00")
        self.start_time_entry = tk.Entry(self.start_frame, textvariable=self.start_time_var, justify='center', width=30, state='readonly')
        self.start_time_entry.pack(anchor="n")
        ### Right side: End section ###
        self.end_frame = tk.Frame(self.right_frame)
        self.end_frame.pack(side="left", padx=10, pady=5)
        self.set_end_button = tk.Button(self.end_frame, text="Click to set End Date&Time", command=self.set_end, font=("Arial", 10, "bold"))
        self.set_end_button.pack(anchor="n")
        self.end_date_var = tk.StringVar(value=self.get_current_date())
        self.end_date_entry = tk.Entry(self.end_frame, textvariable=self.end_date_var, justify='center',  width=30, state='readonly')
        self.end_date_entry.pack(anchor="n", pady=5)
        self.end_time_var = tk.StringVar(value=self.get_current_time())
        self.end_time_entry = tk.Entry(self.end_frame, textvariable=self.end_time_var, justify='center',  width=30, state='readonly')
        self.end_time_entry.pack(anchor="n")
        APPLOGGER.info(f'The Frame <{inspect.currentframe().f_code.co_name}> has been created.')
    def create_frame_3(self):                                                                                           # Frame 3 (F3): "confirm"
        self.f3 = tk.Frame(self)
        self.f3.pack(anchor="n", padx=10, pady=5)
        image = Image.open(os.path.join('src', 'media\\supporter.png'))
        self.supporter_image = ImageTk.PhotoImage(image)
        self.dimmed_supporter_image_tk = self.dim_image(image)
        image = Image.open(os.path.join('src', 'media\\v12.png'))
        self.press_pc_image = ImageTk.PhotoImage(image)
        self.dimmed_press_pc_image_tk = self.dim_image(image)
        self.supporter_button = tk.Button(self.f3, image=self.supporter_image, text="Proceed as Supporter", font=("Arial", 10, "bold"), compound=tk.BOTTOM, command=self.supporter_action)
        self.press_pc_button = tk.Button(self.f3, image=self.press_pc_image, text="Proceed as Press-PC", font=("Arial", 10, "bold"), compound=tk.BOTTOM, command=self.press_pc_action)
        self.supporter_button.pack(side="left", padx=10)
        self.press_pc_button.pack(side="left", padx=10)
        self.activate_deactivate_pic_images(flag=False)                                                                 # Set the dimmed image to the button and disable it
        APPLOGGER.info(f'The Frame <{inspect.currentframe().f_code.co_name}> has been created.')
    @classmethod
    def create_activation_button(cls, root, command):
        text = "Activate " + cls.__name__
        return cls.create_text_button(root, command, text=text)
    def reset_fields(self):
        APPLOGGER.info(f'The <{inspect.currentframe().f_code.co_name}> has been activated.')
        current_date = self.get_current_date()                                                                          ### Resetting DateEntry and Calendar ###
        year, month, day = map(int, current_date.split('-'))
        specific_date = datetime.date(year, month, day)
        self.calendar.selection_set(specific_date)
        current_hour, current_minute = self.get_current_time().split(':')                                               ### Resetting time to current time ###
        self.hour_spin.delete(0, "end")
        self.hour_spin.insert(0, current_hour)
        self.minute_spin.delete(0, "end")
        self.minute_spin.insert(0, current_minute)
        self.second_spin.delete(0, "end")
        self.second_spin.insert(0, "00")
        self.start_date_var.set(current_date)                                                                           ### Resetting Start and End date fields ###
        self.end_date_var.set(current_date)
        self.start_time_var.set("00:01")
        self.end_time_var.set(self.get_current_time())
        self.dev_var.set(False)                                                                                         ### Resetting dev mode checkbox ###
    def initialize_tooltips(self):
        APPLOGGER.info(f'The <{inspect.currentframe().f_code.co_name}> has been activated.')
        create_tooltip(self.set_start_button, "Future Feature")
        create_tooltip(self.set_end_button, "Set the end date and time to the selected values.")
        create_tooltip(self.dev_checkbox, "Enable development mode (for debugging or advanced features).")
    def dev_checkbox_changed(self):
        if self.dev_var.get():
            self.initialize_data_from_external()                                                                        # TODO: Placeholder function
        else:
            self.root.withdraw()
    def update_azure_indicator(self, flag):
        self.azure_var.set(flag)

    def initialize_data_from_external(self):
        APPLOGGER.info(f'The <{inspect.currentframe().f_code.co_name}> has been activated!')                            # TODO: Placeholder values
    def get_press_sn_values(self):
        APPLOGGER.info(f'The <{inspect.currentframe().f_code.co_name}> has been activated!')                            # TODO: Placeholder values
        return ["..."]
    def get_default_press_sn(self):
        APPLOGGER.info(f'The <{inspect.currentframe().f_code.co_name}> has been activated!')                            # TODO: Placeholder default values
        # TODO: Check before delete!
        # return DMDD["LOCAL_METADATA"]["PREVIOUS_PRESS_SN"] if DMDD["LOCAL_METADATA"]["PREVIOUS_PRESS_SN"] != DMD.PREVIOUS_PRESS_SN else SHARE_DATA.PRESS_SN[0]          # Return local_machine if there is local METADATA_CONF.json
        return SHARE_DATA.METADATA["PREVIOUS_PRESS_SN"] if SHARE_DATA.METADATA["PREVIOUS_PRESS_SN"] != DMD.PREVIOUS_PRESS_SN else SHARE_DATA.PRESS_SN[0]          # Return local_machine if there is local METADATA_CONF.json
    def update_press_sn_dropdown(self, new_values):                                                                     # Update the dropdown values with new_values.
        _ = {inspect.currentframe().f_code.co_name}
        try:
            self.press_sn_dropdown["menu"].delete(0, "end")                                                             # Clear the current menu entries
            self.press_sn_var.set(self.press_sn_default_value if self.press_sn_default_value in new_values else new_values[0]) # Update the variable holding the current value
            for value in new_values:                                                                                    # Add new menu entries
                self.press_sn_dropdown["menu"].add_command(label=value, command=tk._setit(self.press_sn_var, value))    # When the menu entry is selected by the user, this command is executed. tk._setit is a Tkinter utility function that returns a function. When the returned function is called, it sets the associated variable (self.press_sn_var in this case) to the provided value (value).
            self.stop_loading_animation()
            self.return_button.pack(side="left")
            self.reset_button.pack(side="left", padx=10)
            self.dev_checkbox.pack(anchor="nw")

            self.azure_checkbox.pack(anchor="nw")

            self.press_sn_dropdown.config(width=50)
            self.press_sn_dropdown.pack(anchor="n")
            self.activate_deactivate_pic_images(flag=True)                                                              # Set regular image to the button enabled
            APPLOGGER.info(f'The <{_}> done - list is updated!')
        except Exception as e:
            APPLOGGER.error(f'{logger_explain_template(func=_, err=e)}')
    def get_current_date(self):
        return time.strftime('%Y-%m-%d')
    def get_current_time(self):
        return time.strftime('%H:%M:00')
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
        self.start_date_var.set(selected_date)
        self.start_time_var.set("00:01:00")
    def dim_image(self, image):
        enhancer = ImageEnhance.Brightness(image)
        dimmed_image = enhancer.enhance(0.5)                                                                            # Reduce brightness to 50%
        return ImageTk.PhotoImage(dimmed_image)
    def activate_deactivate_pic_images(self, flag):
        if flag:
            self.supporter_button.config(image=self.supporter_image, state=tk.NORMAL)
            self.press_pc_button.config(image=self.press_pc_image, state=tk.NORMAL)
        else:
            self.supporter_button.config(image=self.dimmed_supporter_image_tk, state=tk.DISABLED)                       # Set the dimmed image to the button and disable it
            self.press_pc_button.config(image=self.dimmed_press_pc_image_tk, state=tk.DISABLED)                         # Set the dimmed image to the button and disable it
    def confirm_and_proceed(self):
        print("dsjlkjaskd")
        SHARE_DATA.PRESS = self.press_sn_var.get()
        SHARE_DATA.START_DATE = self.start_date_var.get()
        SHARE_DATA.START_TIME = self.start_time_var.get()
        SHARE_DATA.END_DATE = self.end_date_var.get()
        SHARE_DATA.END_TIME = self.end_time_var.get()
        # threading.Thread(target=data_loading, daemon=True).start()
        return data_loading()
    def supporter_action(self):
        self.button_clicked = True
        if self.confirm_and_proceed():
            self.manager.hide_window(self.__class__.__name__)
            self.manager.show_window("Window_SUPPORTER")
        else:
            _err = f'No data exist!\n'
            self.custom_error_dialog(message="Data is missing\nChange Press or Date!")
            # messagebox.showerror(title="Error", message=f'Processing step', )
            pass
            # TODO: DATA LOADING ISSUES
        print("Supporter button clicked!")                                                                              # TODO: Add your logic here...SUPPORTER
    def press_pc_action(self):
        self.button_clicked = True
        print("Press-PC button clicked!")                                                                               # TODO: Add your logic here...PRESS_PC
        self.confirm_and_proceed()
    def on_close(self):
        if self.dev_var.get():                                                                                          # If development mode checked - you should work with the ROOT
            super().hide()
            self.manager.show_window("root_window")
            APPLOGGER.debug(f'<{self.T}> closed in Development mode')
        else:                                                                                                           # If development mode unchecked [Default] - The application will closed.
            self.manager.hide_window(self.__class__.__name__)
            self.manager.root.destroy()
        APPLOGGER.info(f'<{self.T}> closed!')
