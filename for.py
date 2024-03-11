import os
import csv

# Specify the data directory path (modify as needed)
data_dir = "data"

# Loop through each folder in the data directory
for folder in os.listdir(data_dir):
    folder_path = os.path.join(data_dir, folder)
    if os.path.isdir(folder_path):  # Check if it's a directory

        # Define the data file path
        data_file = os.path.join(folder_path, "stock_data.csv")

        # Check if the file exists
        if os.path.exists(data_file):

            # Open the file for writing (overwrite mode)
            with open(data_file, 'w', newline='') as file:  # Use 'w' for overwrite
                writer = csv.writer(file)

                # Write the target header row
                writer.writerow(['date', 'price'])
                

            print(f"Rewritten {data_file} to target format")

        else:
            print(f"File not found: {data_file}")
