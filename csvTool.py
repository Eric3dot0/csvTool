import tkinter as tk
from tkinter import filedialog
import pandas as pd
from tkinter import scrolledtext
import re


# Global variable to store the loaded DataFrame
loaded_df = None

# Global variable to store the selected columns for display
selected_display_columns = []

# Function to read CSV file and update the column names list
def load_csv():
    global loaded_df  # Use the global DataFrame
    file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if file_path:
        loaded_df = read_csv(file_path)
        if loaded_df is not None:
            update_column_list(loaded_df)
            create_column_checkboxes()

# Function to update the column names list
def update_column_list(df):
    column_names_listbox.delete(0, tk.END)
    for column in df.columns:
        column_names_listbox.insert(tk.END, column)

# Function to read CSV file
def read_csv(file_path):
    try:
        df = pd.read_csv(file_path)
        return df
    except Exception as e:
        return None

# Function to create checkboxes for column selection
def create_column_checkboxes():
    if loaded_df is not None:
        for column in loaded_df.columns:
            var = tk.IntVar()
            column_vars[column] = var
            checkbox = tk.Checkbutton(column_selection_frame, text=column, variable=var, command=update_display_columns)
            checkbox.pack()

# Function to perform the search and display selected columns
# Function to perform the search and display selected columns
def execute_search():
    global loaded_df  # Use the global DataFrame
    global selected_display_columns  # Use the global selected columns

    # Get the selected column names for search
    selected_columns = [column_names_listbox.get(idx) for idx in column_names_listbox.curselection()]

    # Get user input for criteria
    criteria1 = value1_entry.get()
    criteria2 = value2_entry.get()

    # Perform the search with the selected columns and criteria
    if not selected_columns:
        result_text.delete(1.0, tk.END)  # Clear any previous results
        result_text.insert(tk.END, "Please select at least one column to search.")
    elif loaded_df is None:
        result_text.delete(1.0, tk.END)  # Clear any previous results
        result_text.insert(tk.END, "No CSV file loaded. Please use the 'Load CSV' button.")
    else:
        # Handle wildcard search
        criteria1 = criteria1.strip()  # Remove leading/trailing spaces
        criteria2 = criteria2.strip()  # Remove leading/trailing spaces

        if criteria1 == "*":
            criteria1 = ".*"  # Replace '*' with regex pattern for any text
        else:
            criteria1 = re.escape(criteria1)  # Escape special characters in the input

        if criteria2 == "*":
            criteria2 = ".*"  # Replace '*' with regex pattern for any text
        else:
            criteria2 = re.escape(criteria2)  # Escape special characters in the input

        # Perform the search with the selected columns and criteria
        result_text.delete(1.0, tk.END)  # Clear any previous results

        if not loaded_df.empty:
            filtered_df = loaded_df
            if criteria1 != "":
                filtered_df = filtered_df[filtered_df[selected_columns[0]].str.contains(criteria1, case=False, na=False, regex=True)]
            if criteria2 != "":
                filtered_df = filtered_df[filtered_df[selected_columns[1]].str.contains(criteria2, case=False, na=False, regex=True)]

            # Filter and display selected columns
            if selected_display_columns:
                filtered_df = filtered_df[selected_display_columns]

            # Insert cleaned lines with stripped whitespace and a line of whitespace between results
            for line in filtered_df.to_string(index=False).split('\n'):
                result_text.insert(tk.END, line.strip() + '\n')
                result_text.insert(tk.END, '\n')  # Add a line of whitespace between results

            # Set the insertion point to the beginning
            result_text.mark_set(tk.INSERT, "1.0")
        else:
            result_text.insert(tk.END, "No rows match the given criteria.")

# Function to convert value to int or bool
def try_convert(value):
    try:
        return int(value)
    except ValueError:
        return convert_to_bool(value)

# Function to convert value to bool
def convert_to_bool(value):
    if isinstance(value, str) and value.lower() in ['true', '1', 'yes', 'y']:
        return True
    elif isinstance(value, str) and value.lower() in ['false', '0', 'no', 'n']:
        return False
    else:
        return value

# Function to update selected display columns
def update_display_columns():
    global selected_display_columns  # Use the global selected columns
    selected_display_columns = [column for column, var in column_vars.items() if var.get() == 1]


# Create the main window
root = tk.Tk()
root.title("CSV Data Search Tool")

# Create and place GUI elements
load_csv_button = tk.Button(root, text="Load CSV", command=load_csv)
load_csv_button.pack()

column_names_label = tk.Label(root, text="Available Columns:")
column_names_label.pack()

column_names_listbox = tk.Listbox(root, selectmode=tk.MULTIPLE)
column_names_listbox.pack()

criteria1_label = tk.Label(root, text="Criteria 1:")
criteria1_label.pack()
value1_entry = tk.Entry(root)
value1_entry.pack()

criteria2_label = tk.Label(root, text="Criteria 2:")
criteria2_label.pack()
value2_entry = tk.Entry(root)
value2_entry.pack()

# Add a label for the checkbox section
checkbox_label = tk.Label(root, text="Select which columns to output:")
checkbox_label.pack()

#Create a frame for column selection with a scrollbar
column_vars = {}  # Dictionary to store checkbox variables
column_selection_frame = tk.Frame(root)
column_selection_frame.pack()

column_frame = tk.Frame(root)
column_frame.pack()

column_canvas = tk.Canvas(column_frame, height=150)  # Set the desired height
column_scrollbar = tk.Scrollbar(column_frame, orient=tk.VERTICAL, command=column_canvas.yview)
column_canvas.config(yscrollcommand=column_scrollbar.set)
column_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
column_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Create a frame for checkboxes inside the canvas
column_frame_inside_canvas = tk.Frame(column_canvas)
column_canvas.create_window((0, 0), window=column_frame_inside_canvas, anchor=tk.NW)

# Function to update the canvas scroll region
def update_canvas_scroll_region(event):
    column_canvas.configure(scrollregion=column_canvas.bbox("all"))

# Bind the update function to configure event
column_frame_inside_canvas.bind("<Configure>", update_canvas_scroll_region)

# Create checkboxes for column selection inside the frame inside the canvas
def create_column_checkboxes():
    if loaded_df is not None:
        for column in loaded_df.columns:
            var = tk.IntVar()
            column_vars[column] = var
            checkbox = tk.Checkbutton(column_frame_inside_canvas, text=column, variable=var, command=update_display_columns)
            checkbox.pack(anchor='w')

create_column_checkboxes()

# Update the canvas scroll region initially
column_canvas.update_idletasks()
column_canvas.configure(scrollregion=column_canvas.bbox("all"))

search_button = tk.Button(root, text="Search", command=execute_search)
search_button.pack()

result_text = tk.Text(root, height=10, width=50)
result_text.pack()

# Run the GUI main loop
root.mainloop()
