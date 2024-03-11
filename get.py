import os
import yfinance as yf
import csv
from datetime import datetime

def fetch_stock_data(stock_code):
  try:
    stock = yf.Ticker(f"{stock_code}.AX")  # Append ".AX" for ASX listings
    data = stock.history(period="1d")
    return data
  except Exception as e:
    print(f"Error fetching data for {stock_code}: {e}")
    return None

def save_stock_data(stock_code, data):
  if data is not None:
    filename = f"data/{stock_code}/stock_data.csv"

    # Open file in append mode
    with open(filename, 'a', newline='') as f:
      writer = csv.writer(f)

      # Write header only if file is empty
      if not os.path.exists(filename) or os.stat(filename).st_size == 0:
        writer.writerow(['date', 'price'])

      # Convert data to a list of lists for easier writing
      data_list = [[date.strftime('%Y-%m-%d'), price] for date, price in data['Close'].items()]
      writer.writerows(data_list)

    print(f"Appended data for {stock_code} to {filename}")

def update_stock_data():
  data_directory = "data"
  for stock_code in os.listdir(data_directory):
    if os.path.isdir(os.path.join(data_directory, stock_code)):
      stock_data = fetch_stock_data(stock_code)
      save_stock_data(stock_code, stock_data)

def main():
  update_stock_data()

if __name__ == "__main__":
  main()
