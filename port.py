import os
import pandas as pd
import json
from tqdm import tqdm
import multiprocessing

def load_data(data_dir):
    stock_data = {}
    for stock_file in os.listdir(data_dir):
        if stock_file.endswith('.csv'):
            file_path = os.path.join(data_dir, stock_file)
            try:
                data = pd.read_csv(file_path, parse_dates=['Date'])
                stock_symbol = os.path.splitext(stock_file)[0]
                stock_data[stock_symbol] = preprocess_data(data.copy())
            except FileNotFoundError:
                print(f"Error: File '{file_path}' not found.")
    return stock_data

def preprocess_data(data):
    data.dropna(inplace=True)
    data['Daily_Return'] = data['Close'].pct_change()
    return data

def analyze_data(stock_data):
    for symbol, data in tqdm(stock_data.items(), desc="Analyzing Data"):
        # Perform analysis for each stock
        # Example: Check if the stock meets certain criteria for investment
        if data['Close'].mean() > 50 and data['Close'].std() < 10:
            print(f"Stock {symbol} meets the investment criteria.")

def load_portfolio(file_path):
    try:
        with open(file_path, 'r') as file:
            portfolio = json.load(file)
        return portfolio
    except FileNotFoundError:
        print(f"Error: Portfolio file '{file_path}' not found.")
        return {}

def analyze_portfolio(portfolio, stock_data):
    if not portfolio:
        print("No portfolio data available.")
        return

    total_investment = multiprocessing.Value('d', 0)
    current_value = multiprocessing.Value('d', 0)
    processes = []

    for symbol, quantity in portfolio.items():
        if symbol in stock_data:
            process = multiprocessing.Process(target=analyze_stock, args=(symbol, quantity, stock_data, total_investment, current_value))
            processes.append(process)
            process.start()

    for process in processes:
        process.join()

    print(f"\nTotal Investment: {total_investment.value}")
    print(f"Current Value: {current_value.value}")

    if current_value.value < total_investment.value:
        print("Your portfolio is underperforming. Consider selling some stocks.")
    elif current_value.value > total_investment.value:
        print("Your portfolio is performing well. You can consider holding or even buying more.")
    else:
        print("Your portfolio value remains the same.")

def analyze_stock(symbol, quantity, stock_data, total_investment, current_value):
    stock_price = stock_data[symbol]['Close'].iloc[-1]  # Get the latest closing price
    total_investment.value += stock_price * quantity
    current_value.value += stock_price * quantity

if __name__ == "__main__":
    data_dir = 'stock_data'
    stock_data = load_data(data_dir)

    portfolio_file_path = 'portfolio.json'
    portfolio = load_portfolio(portfolio_file_path)

    analyze_data(stock_data)
    analyze_portfolio(portfolio, stock_data)

    print("\nImportant: This code should not be used to make real-world investment decisions. Consult with a financial advisor before making any investment decisions.")
