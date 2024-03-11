from datetime import datetime
import tkinter as tk
from tkinter import ttk  # Optional for themed widgets
import csv
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Specify the data directory path (modify as needed)
data_dir = "data"
companies_file = "companies.csv"  # Path to the companies file
output_file = "output.txt"  # Path to the output file

# Define the number of recent entries to consider (2 in this case)
num_recent_entries = 2

# Function to parse dates with flexible format handling
def parse_date(date_str):
    formats = ['%Y-%m-%d', '%Y-%m-%d %H:%M:%S%z']  # Add more formats if needed
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt).date()
        except ValueError:
            continue
    raise ValueError(f"Unable to parse date: {date_str}")

# Function to read company names from the companies file
def read_company_names():
    company_names = {}
    with open(companies_file, 'r') as file:
        reader = csv.reader(file, delimiter=',', quotechar='"')
        for row in reader:
            if len(row) == 2:
                print(f"Reading company code: {row[0]}, Company name: {row[1]}")
                company_names[row[0]] = row[1]
    return company_names


# Function to calculate percentage decrease
def calculate_percentage_decrease(old_price, new_price):
    return ((old_price - new_price) / old_price) * 100

# Get company names
company_names_dict = read_company_names()

# Open the output file for writing
with open(output_file, 'w') as output:
    # Loop through each folder in the data directory
    for folder in os.listdir(data_dir):
        folder_path = os.path.join(data_dir, folder)
        if os.path.isdir(folder_path):  # Check if it's a directory

            # Define the data file path
            data_file = os.path.join(folder_path, "stock_data.csv")

            # Check if the file exists
            if os.path.exists(data_file):

                try:
                    # Open the file for reading
                    with open(data_file, 'r') as file:
                        reader = csv.reader(file)

                        # Skip header row (assuming the first row is header)
                        next(reader, None)

                        # Track recent dates and prices
                        recent_entries = []

                        for row in reader:
                            # Extract date and price from the row (modify this based on your data format)
                            try:
                                current_date = parse_date(row[0])
                                current_price = float(row[1])  # Assuming price is in the second column
                            except (ValueError, IndexError) as e:  # Handle potential formatting issues or index errors
                                print(f"Error parsing data in {data_file}: {e}")
                                continue

                            # Add current entry to recent entries
                            recent_entries.append((current_date, current_price))

                            # Keep only the last num_recent_entries entries
                            if len(recent_entries) > num_recent_entries:
                                recent_entries.pop(0)

                        # Check if the older entry has a higher price than the latest one
                        if len(recent_entries) == num_recent_entries:
                            older_date, older_price = recent_entries[0]
                            latest_date, latest_price = recent_entries[1]
                            if older_price > latest_price:
                                # Get the company name from the folder name
                                company_code = folder
                                company_name = company_names_dict.get(company_code, "Unknown")
                                # Calculate percentage decrease
                                percentage_decrease = calculate_percentage_decrease(older_price, latest_price)
                                # Write to output file
                                output_line = f"Folder: {company_code} ({company_name}), Percentage Decrease: {percentage_decrease:.2f}%\n"
                                output.write(output_line)

                except (IOError, csv.Error) as e:
                    print(f"Error processing file {data_file}: {e}")

            else:
                print(f"File not found: {data_file}")

# Print a message indicating that the output has been written to the file
print(f"Output has been written to {output_file}")
