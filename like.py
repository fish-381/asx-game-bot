import os
import json
import tkinter as tk
from tkinter import ttk

# Define data directory path
data_dir = "data"

# Define database file path
data_file = "data_records.json"

def get_folders():
    """
    Retrieves a list of folders in the data directory.
    """
    folders = [f for f in os.listdir(data_dir) if os.path.isdir(os.path.join(data_dir, f))]
    return folders

def load_data():
    """
    Loads data from the database file (if it exists).
    """
    if not os.path.exists(data_file):
        return {}
    with open(data_file, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            # Handle potential errors in existing data
            data = {}
    return data

def save_data(data):
    """
    Saves data to the database file.
    """
    with open(data_file, 'w') as f:
        json.dump(data, f, indent=4)

def update_ui(data):
    """
    Updates the user interface with the latest data.
    """
    folder_list.delete(0, tk.END)  # Clear existing items in the listbox
    for folder, info in data.items():
        folder_list.insert(tk.END, folder)

def on_like_click():
    folder = folder_list.get(folder_list.curselection())
    data[folder]["liked"] = like_var.get()
    save_data(data)
    update_ui(data)

def on_has_it_click():
    folder = folder_list.get(folder_list.curselection())
    data[folder]["has_it"] = has_it_var.get()
    save_data(data)
    update_ui(data)

def main():
    # Load data
    global data
    data = load_data()

    # Populate folder list
    folders = get_folders()
    for folder in folders:
        if folder not in data:
            data[folder] = {"liked": 0, "has_it": 0}
            save_data(data)

    # Create main window
    window = tk.Tk()
    window.title("Data Folder Database")

    # Folder list frame
    folder_list_frame = ttk.Frame(window)
    folder_list_frame.pack(padx=10, pady=10)

    # Folder list label
    folder_list_label = ttk.Label(folder_list_frame, text="Folders:")
    folder_list_label.pack(anchor=tk.W)

    # Folder list
    global folder_list
    folder_list = tk.Listbox(folder_list_frame, selectmode=tk.SINGLE)
    folder_list.pack(fill=tk.BOTH, expand=True)

    # Scrollbar for folder list
    scrollbar = ttk.Scrollbar(folder_list_frame, orient=tk.VERTICAL, command=folder_list.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    folder_list.config(yscrollcommand=scrollbar.set)

    # Like/Has It buttons frame
    button_frame = ttk.Frame(window)
    button_frame.pack(padx=10, pady=10)

    # Like button
    global like_var
    like_var = tk.IntVar()
    like_button = ttk.Button(button_frame, text="Like", command=on_like_click)
    like_button.pack(side=tk.LEFT, padx=5)

    # Has It button
    global has_it_var
    has_it_var = tk.IntVar()
    has_it_button = ttk.Button(button_frame, text="Have It", command=on_has_it_click)
    has_it_button.pack(side=tk.LEFT, padx=5)

    # Update UI with initial data
    update_ui(data)

    window.mainloop()

if __name__ == "__main__":
    main()
