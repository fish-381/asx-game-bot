import os
import yfinance as yf
import pandas as pd
from datetime import datetime

def fetch_stock_data(stock_code):
    try:
        stock = yf.Ticker(f"{stock_code}.AX")  # Append ".AX" for ASX listings
        data = stock.history(period="7d")
        return data
    except Exception as e:
        print(f"Error fetching data for {stock_code}: {e}")
        return None

def save_stock_data(stock_code, data):
    if data is not None:
        filename = f"data/{stock_code}/stock_data.csv"

        # If file exists, check if dates match. If yes, don't save new data.
        if os.path.exists(filename):
            existing_data = pd.read_csv(filename, index_col='date')
            if existing_data.index.isin(data.index).all():  # Check if all dates in new data are already in existing data
                print(f"All dates in {stock_code} data already present. Keeping file unchanged.")
                return
            else:
                # Dates don't match completely, proceed with appending new data
                data = pd.concat([existing_data, data]).drop_duplicates(keep='last')
                data = data.dropna(how='all')

        data.to_csv(filename, columns=['Close'], header=['price'], index_label='date')
        print(f"Saved data for {stock_code} to {filename}")

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
