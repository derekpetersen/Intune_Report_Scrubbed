import tkinter as tk
from tkinter import filedialog, ttk
from data_processing import data_processing


class GetFilePath:
    """
    Class to create an input and file explorer button to retrieve report files
    """

    def __init__(self, name, row):
        self.filename = None
        self.entry = ttk.Entry(widgets_frame, width=20, textvariable=tk.StringVar())
        self.entry.insert(0, f"{name} File Path")
        self.entry.bind("<FocusIn>", lambda e: self.entry.delete('0', 'end'))
        self.entry.grid(column=0, row=row, padx=5, pady=(0, 5))
        self.button = ttk.Button(widgets_frame, text=f'Browse {name} Report', width=20, command=self.get_file_path)
        self.button.grid(column=1, row=row, padx=5, pady=(0, 5))

    def get_file_path(self, event=None):
        """
        Activated by a button. Launches file explorer window to select file, then places it in the input text box
        :param event:
        :return:
        """
        self.filename = filedialog.askopenfilename()
        self.entry.delete('0', 'end')
        self.entry.insert(0, self.filename)


def display_data(data_frame):
    """
    Takes dataframe as an input and displays it in Tkinter treeview
    :param data_frame:
    :return:
    """
    # Gets the headings for the data and displays them
    for col_name in data_frame:
        tree_view.heading(col_name, text=col_name)

    # Gets the values of the data and displays it
    for value in data_frame.values.tolist():
        tree_view.insert('', tk.END, values=value)


def submit_button():
    """
    Submit function that triggers the apps functionality
    :return:
    """
    # Gets the filepath from the text boxes, and then runs them through the cleaning process
    intune_report = data_processing.intune_data_cleaning(intune.entry.get())
    sd_report = data_processing.sd_data_cleaning(sd.entry.get())

    # Runs the comparison between the files to determine what is not in Intune
    not_in_intune = data_processing.check_devices_not_in_intune(intune_report, sd_report)

    # Takes the above and then runs through 'display_data' which renders data on the screen
    display_data(not_in_intune)


# Set up the Tkinter window
root = tk.Tk()
root.title('View "In Use" Machines not in Intune')
style = ttk.Style(root)

# Set the theme
root.tk.call("source", "forest-dark.tcl")
root.tk.call("source", "forest-light.tcl")
style.theme_use("forest-dark")

# Set up a Tkinter frame to house objects
frame = ttk.Frame(root)
frame.pack()

# Frame for all the left hand widgets
widgets_frame = ttk.LabelFrame(frame, text="Select Reports")
widgets_frame.grid(column=0, row=0, padx=20, pady=20)

# Calls the class that creates the intune/SD form
intune = GetFilePath('Intune', 0)
sd = GetFilePath('SD', 1)

# Separator line between form and submit button
separator = ttk.Separator(widgets_frame)
separator.grid(row=3, column=0, columnspan=2, padx=(20, 10), pady=10, sticky="ew")

# Submit Button
submit_btn = ttk.Button(widgets_frame, text='Submit', command=submit_button)
submit_btn.grid(column=0, row=4, columnspan=2, pady=(5, 10))

# Frame for data tree on right
tree_frame = ttk.Frame(frame)
tree_frame.grid(row=0, column=1, pady=10)
tree_scroll = ttk.Scrollbar(tree_frame)
tree_scroll.pack(side="right", fill="y")
cols = ("Machine Name", "User")
tree_view = ttk.Treeview(tree_frame, show="headings", yscrollcommand=tree_scroll.set, columns=cols, height=13)
tree_view.column("Machine Name", width=150)
tree_view.column("User", width=150)
tree_view.pack()
tree_scroll.config(command=tree_view.yview)

root.mainloop()
