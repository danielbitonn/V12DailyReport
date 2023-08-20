from src.scripts.system.applogger import APPLOGGER
from src.scripts.gui.windows.win_utility import SHARE_DATA, BaseWindow

import tkinter as tk
from tkcalendar import Calendar, DateEntry
class Window_3(BaseWindow):
    def __init__(self, root, manager, shared_data=None, relation=None, extra_width=0, extra_height=0):
        super().__init__(root, manager, shared_data, relation, extra_width, extra_height)
        self.T = "Window_3"
        self.title(self.T)
        self.extra_width = extra_width
        self.extra_height = extra_height

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