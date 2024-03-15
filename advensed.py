import os
import yfinance as yf
import csv
import json

def fetch_stock_data(stock_code):
    try:
        stock = yf.Ticker(f"{stock_code}.AX")  # Append ".AX" for ASX listings
        data = stock.history(period="max")  # Fetch all available historical data
        return data
    except Exception as e:
        print(f"Error fetching data for {stock_code}: {e}")
        return None

def save_stock_data(stock_code, data):
    if data is not None:
        filename = f"stock_data/{stock_code}.csv"

        # Write data to CSV file
        data.to_csv(filename)

        print(f"Saved data for {stock_code} to {filename}")

def update_stock_data_from_portfolio(portfolio_file):
    try:
        with open(portfolio_file, 'r') as file:
            portfolio = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        raise FileNotFoundError(f"Portfolio file '{portfolio_file}' could not be loaded: {e}")

    for stock_code in portfolio:
        stock_data = fetch_stock_data(stock_code)
        if stock_data is not None:
            save_stock_data(stock_code, stock_data)

def main():
    portfolio_file = "portfolio.json"
    update_stock_data_from_portfolio(portfolio_file)

if __name__ == "__main__":
    main()
