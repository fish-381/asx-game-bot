import tkinter as tk
from tkinter import ttk  # Optional for themed widgets
import csv
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def load_data(filename):
    companies = []
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row
        for row in reader:
            companies.append({"name": row[0], "code": row[1]})
    return companies


def display_details(company):
    details_label.config(text=f"Name: {company['name']}\nCode: {company['code']}")


def create_folder(code):
    folder_path = f"data/{code}"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        


def on_select(event):
    if company_listbox.curselection():
        selected_index = company_listbox.curselection()[0]
        selected_company = companies[selected_index]
        display_details(selected_company)
        plot_data(selected_company['code'])  # Call plot function with updated code


def search_company():
    search_term = search_entry.get().strip().lower()
    for i, company in enumerate(companies):
        if search_term in company["name"].lower():
            company_listbox.selection_clear(0, tk.END)
            company_listbox.selection_set(i)
            company_listbox.see(i)
            display_details(company)
            plot_data(company['code'])
            break
    else:
        details_label.config(text="Company not found.")


def plot_data(code):
    folder_path = f"data/{code}"
    try:
        # Clear previous plot widgets before creating a new one
        for widget in details_frame.winfo_children():
            if isinstance(widget, tk.Canvas):  # Check if it's the canvas holding the plot
                widget.destroy()

        # Assuming data file exists and has specific format (modify as needed)
        with open(f"{folder_path}/stock_data.csv", 'r') as file:
            reader = csv.DictReader(file)
            dates, prices = [], []
            for row in reader:
                dates.append(row['date'])
                prices.append(float(row['price']))

            fig, ax = plt.subplots()
            ax.plot(dates, prices, marker='o')
            ax.set_title(f"{code} Stock Data")
            ax.set_xlabel("Date")
            ax.set_ylabel("Price")
            ax.tick_params(axis='x', rotation=45)

            canvas = FigureCanvasTkAgg(fig, master=details_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    except FileNotFoundError:
        # Handle case where data file is missing (optional)
        pass


# Main program
root = tk.Tk()
root.title("Company Analysis")

companies = load_data("companies.csv")

company_listbox = tk.Listbox(root, width=50, height=20)
for company in companies:
    company_listbox.insert(tk.END, company["name"])
company_listbox.bind("<<ListboxSelect>>", on_select)
company_listbox.pack(side=tk.LEFT, padx=10, pady=10)

details_frame = tk.Frame(root)
details_frame.pack(side=tk.LEFT, padx=10, pady=10)

details_label = tk.Label(details_frame, text="")
details_label.pack()

search_frame = tk.Frame(root)
search_frame.pack(side=tk.TOP, padx=10, pady=10)
search_entry = tk.Entry(search_frame, width=40)
search_entry.pack(side=tk.LEFT)
search_button = tk.Button(search_frame, text="Search", command=search_company)
search_button.pack(side=tk.LEFT)

root.mainloop()