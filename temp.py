import tkinter as tk
from tkinter import ttk

default_values = {
    "category": "Category A",
    "start_time": "00:00",
    "middle_time": "01:00",
    "end_time": "02:00",
    "description": "Description Here..."
}
def log_action(action):
    """Simple function to log user actions."""
    print(action)
def add_row():
    """Function to add a new row of widgets to the canvas frame."""
    _row_widgets = []                                                                                                   # Initialize the list to hold this row's widgets
    categories = ["Category A", "Category B (Enables Middle Time)", "Category C"]
    category_dropdown = ttk.Combobox(frame_inside_canvas, values=categories)
    category_dropdown.set(default_values["category"])
    category_dropdown.bind("<<ComboboxSelected>>", lambda e, dd=category_dropdown: on_category_change(dd))
    category_dropdown.grid(row=len(rows), column=0, sticky='ew')
    _row_widgets.append(category_dropdown)
    ### TIMES ###
    times = ["00:00", "01:00", "02:00", "..."]
    start_time_dropdown = ttk.Combobox(frame_inside_canvas, values=times)
    start_time_dropdown.set(default_values["start_time"])
    start_time_dropdown.grid(row=len(rows), column=1, sticky='ew')
    _row_widgets.append(start_time_dropdown)
    middle_time_dropdown = ttk.Combobox(frame_inside_canvas, values=times, state="disabled")
    middle_time_dropdown.set(default_values["middle_time"])
    middle_time_dropdown.grid(row=len(rows), column=2, sticky='ew')
    _row_widgets.append(middle_time_dropdown)
    end_time_dropdown = ttk.Combobox(frame_inside_canvas, values=times)
    end_time_dropdown.set(default_values["end_time"])
    end_time_dropdown.grid(row=len(rows), column=3, sticky='ew')
    _row_widgets.append(end_time_dropdown)
    ### Description ###
    description_text = tk.Text(frame_inside_canvas, height=1, width=20)
    description_text.insert(tk.END, default_values["description"])
    description_text.grid(row=len(rows), column=4, sticky='ew')
    _row_widgets.append(description_text)
    ### Function Place-holder ###
    placeholder_btn = tk.Button(frame_inside_canvas, text="Button", command=lambda row_num=len(rows), row_widgets=_row_widgets: handle_placeholder_btn_action(row_num, row_widgets))
    placeholder_btn.grid(row=len(rows), column=5, sticky='ew')
    _row_widgets.append(placeholder_btn)
    ### Delete button ###
    del_btn = tk.Button(frame_inside_canvas, text="Delete", command=lambda row_num=len(rows): delete_row(row_num))
    del_btn.grid(row=len(rows), column=6, sticky='ew')
    _row_widgets.append(del_btn)
    ### Widget list ###
    rows.append(_row_widgets)                                                                                           # Instead of rows.append([category_dropdown, start_time_dropdown, middle_time_dropdown, end_time_dropdown, description_text, placeholder_btn, del_btn])
    ### Add Button
    add_main_btn.grid(row=len(rows), columnspan=7)                                                                      # Shift the add_main_btn below the last row (span across all columns)
    ### Resize the root window dynamically ###
    resize_window_and_scrollregion()                                                                                    # Based on the content and adjust canvas scroll region
    log_action(f"Adding row # {len(rows)} to {rows}")                                                                   # Logging
def handle_placeholder_btn_action(row_num, row_widgets):
    category = row_widgets[0].get()
    start_time = row_widgets[1].get()
    middle_time = row_widgets[2].get()
    end_time = row_widgets[3].get()
    description = row_widgets[4].get("1.0", "end-1c")                                                                   # Gets text from the Text widget
    log_action(f"Button #{row_num} Data >>> Category: {category}, Start: {start_time}, Middle: {middle_time}, End: {end_time}, Description: {description}")
def resize_window_and_scrollregion():
    if not rows:
        return                                                                                                          # Return if no rows exist
    estimated_widget_height = 30                                                                                        # Assuming an average widget height of 30 pixels
    total_content_height = estimated_widget_height * (len(rows) + 1)                                                    # +1 for some buffer space
    total_width = sum(widget.winfo_reqwidth() for widget in rows[0])                                                    # Calculate total width based on the width of all widgets in the first row. (Assuming all rows have the same width.)
    ### Account for scrollbar width. ###
    scrollbar_width = scrollbar.winfo_width()
    total_width += scrollbar_width
    ### Set maximum height and width based on the screen dimensions ###
    max_height = int(root.winfo_screenheight() * 0.5)
    max_width = int(root.winfo_screenwidth() * 0.8)
    ### Adjust the window dimensions based on content, but don't exceed the max values ###
    new_height = min(total_content_height, max_height)
    new_width = min(total_width, max_width)
    ### Configure the height of the frame_inside_canvas ###
    frame_inside_canvas.config(height=total_content_height)
    canvas.configure(scrollregion=canvas.bbox("all"))                                                                   # Update the canvas's scroll region
    root.geometry(f"{new_width}x{new_height}")
def on_category_change(category_dropdown):
    if category_dropdown.get() == "Category B (Enables Middle Time)":
        rows[category_dropdown.grid_info()["row"]][2].configure(state="normal")
    else:
        rows[category_dropdown.grid_info()["row"]][2].configure(state="disabled")
def delete_row(target_row_num):
    """Function to delete a specific row of widgets."""
    log_action(f"Deleting row # {target_row_num} from {rows}")
    for widget in rows[target_row_num]:                                                                                 # Destroy all the widgets in the target row
        widget.destroy()
    rows.pop(target_row_num)                                                                                            # Remove the row from the rows list
    for inx, row_widgets in enumerate(rows[target_row_num:], start=target_row_num):                                     # Re-grid all the widgets below the deleted row
        for j, widget in enumerate(row_widgets):
            widget.grid(row=inx, column=j, sticky='ew')
    for indx in range(target_row_num, len(rows)):                                                                       # Update the command for all delete buttons below the deleted row
        rows[indx][-1]['command'] = lambda row_num=indx: delete_row(row_num)
    add_main_btn.grid(row=len(rows), columnspan=7)                                                                      # Shift the add_main_btn below the last row (span across all columns)
    resize_window_and_scrollregion()                                                                                    # Adjust the canvas's scroll region after deleting widgets
    log_action(f"The updated rows list ({len(rows)}): {rows}")
def on_mousewheel(event):
    """
    It's called whenever the user scrolls the mouse wheel. It adjusts the scroll position of the canvas (yview
    The event.delta returns a positive value if the scroll is upwards and a negative value if the scroll is downwards.
    Multiplying by -1 ensures the scroll direction feels natural.
    Dividing by 120 normalizes this delta to handle scroll speed across different OS and devices
    :param event:
    :return:
    """
    canvas.yview_scroll(-1 * (event.delta // 120), "units")
def on_canvas_resize(event):
    # Set the width of frame_inside_canvas to be the width of canvas minus scrollbar width
    canvas_width = event.width - scrollbar.winfo_width()+7          # +7 find-tune
    canvas.itemconfig(canvas_frame, width=canvas_width)

### Start """
root = tk.Tk()
root.title("Dynamic Rows in Tkinter")

main_frame = tk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=1)

canvas = tk.Canvas(main_frame)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

scrollbar = tk.Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

canvas.configure(yscrollcommand=scrollbar.set)
canvas.bind_all("<MouseWheel>", on_mousewheel)

frame_inside_canvas = tk.Frame(canvas)
canvas_frame = canvas.create_window((0, 0), window=frame_inside_canvas, anchor="nw")
# Bind the resize event to the canvas
canvas.bind('<Configure>', on_canvas_resize)

# Configure rows and columns for resizing
"""
configures the behavior of the grid geometry manager. 
By setting the weight attribute, it ensures that when the containing widget is resized, 
each of these rows or columns also resizes proportionally.
when we have equal weight like (frame_inside_canvas and the single column of main_frame and canvas), 
so they'll expand or shrink equally when their parent widget's size changes.
"""
for i in range(7):
    frame_inside_canvas.columnconfigure(i, weight=1)
main_frame.columnconfigure(0, weight=1)
main_frame.rowconfigure(0, weight=1)
canvas.columnconfigure(0, weight=1)
canvas.rowconfigure(0, weight=1)

rows = []
# Define add_main_btn but don't grid it yet. It will be gridded in add_row()
add_main_btn = tk.Button(frame_inside_canvas, text="Add Row", command=add_row)
add_row()

root.after(100, resize_window_and_scrollregion)
root.mainloop()
