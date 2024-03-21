import pandas as pd
import os
import json
import numpy as np
import matplotlib.pyplot as plt  # Optional for visualization

def load_data(data_dir):
    """
    Loads data from multiple CSV files within a given directory.

    Args:
        data_dir (str): Path to the directory containing stock data folders.

    Returns:
        dict: A dictionary where keys are stock symbols and values are DataFrames
              containing their preprocessed data.
    """

    stock_data = {}
    for stock_folder in os.listdir(data_dir):
        if os.path.isdir(os.path.join(data_dir, stock_folder)):  # Check if it's a directory
            file_path = os.path.join(data_dir, stock_folder, 'stock_data.csv')
            try:
                data = pd.read_csv(file_path, index_col='date', parse_dates=True)
                stock_data[stock_folder] = preprocess_data(data.copy())  # Avoid modifying original data
            except FileNotFoundError:
                print(f"Error: File '{file_path}' not found.")

    return stock_data


def preprocess_data(data):
    """
    Preprocesses data including calculating returns.

    Args:
        data (pd.DataFrame): Data to preprocess.

    Returns:
        pd.DataFrame: Preprocessed data.
    """

    # Handle missing values, outliers, etc. (replace with your preferred methods)
    data.fillna(method='ffill', inplace=True)  # Adjust as needed
    data.replace([np.inf, -np.inf], 1e10, inplace=True)  # Replace with a suitable large value

    # Calculate returns
    data['returns'] = data['price'].pct_change()

    # Reset index to ensure it's unique
    data.reset_index(inplace=True)

    # Print summary statistics (writing to a file)
    with open("summary_stats.txt", "w") as summary_file:
        summary_file.write("\nSummary Statistics after preprocessing:\n")
        summary_file.write(str(data.describe()))

    # Feature engineering (add relevant indicators)
    # ... (consider technical indicators, fundamental analysis, etc.)

    return data


def analyze_data(stock_data):
    """
    Analyzes data for each stock using various methods (consideration of appropriate
    techniques needed).

    Args:
        stock_data (dict): Dictionary containing preprocessed data for each stock.
    """

    invest_stocks = []  # List to store stocks to invest in

    with open("shouldbuy.txt", "w") as recommendations_file:
        for stock_symbol, data in stock_data.items():
            # Perform analysis for each stock
            # Example: Check if the stock meets certain criteria for investment
            if data['price'].mean() > 50 and data['price'].std() < 10:
                invest_stocks.append(stock_symbol)
                recommendations_file.write(f"{stock_symbol}\n")

        # Print stocks to consider investing in (writing to file)
        if invest_stocks:
            recommendations_file.write("Stocks to consider investing in:\n")
        else:
            recommendations_file.write("No stocks meet the investment criteria.\n")


def load_portfolio(file_path):
    """
    Loads the user's portfolio holdings from a JSON file.

    Args:
        file_path (str): Path to the JSON file containing portfolio holdings.

    Returns:
        dict: A dictionary where keys are stock symbols and values are the quantity held.
    """

    try:
        with open(file_path, 'r') as file:
            portfolio = json.load(file)
            return portfolio
    except FileNotFoundError:
        print(f"Error: Portfolio file '{file_path}' not found.")
        return {}
def analyze_portfolio(portfolio, stock_data):
    """
    Analyzes the user's portfolio in relation to the stock data.

    Args:
        portfolio (dict): Dictionary containing the user's portfolio holdings.
        stock_data (dict): Dictionary containing preprocessed data for each stock.
    """

    if not portfolio:
        print("No portfolio data available.")
        return

    # Calculate portfolio metrics
    total_value = 0
    for symbol, quantity in portfolio.items():
        if symbol in stock_data:
            stock_price = stock_data[symbol]['price'].iloc[-1]  # Get the latest price
            total_value += stock_price * quantity

    # Write portfolio metrics to a file
    with open("portfolio_metrics.txt", "w") as metrics_file:
        metrics_file.write("\nPortfolio Metrics:\n")
        metrics_file.write(f"Total Portfolio Value: ${total_value:.2f}\n")

    try:
        from scipy.stats import norm  # Assuming a normal distribution for simplicity
        alpha = 0.05  # Confidence level (5%)

        # Calculate portfolio daily returns
        portfolio_returns = pd.Series(0, index=stock_data[list(portfolio.keys())[0]].index)
        for symbol, quantity in portfolio.items():
            if symbol in stock_data:
                portfolio_returns += quantity * stock_data[symbol]['returns']

        # Calculate VaR and write to file
        var = -norm.ppf(alpha) * portfolio_returns.std()
        with open("var_analysis.txt", "w") as var_file:
            var_file.write(f"\nValue at Risk (VaR) at {(1 - alpha) * 100}% confidence level: ${var:.2f}\n")

        # Calculate CVaR and write to file
        cvar = portfolio_returns[portfolio_returns <= var].mean()
        with open("cvar_analysis.txt", "w") as cvar_file:
            cvar_file.write(f"\nConditional Value at Risk (CVaR) at {(1 - alpha) * 100}% confidence level: ${cvar:.2f}\n")

    except ImportError:
        print("Note: SciPy is required for VaR and CVaR calculations.")

    # Check if any stock quantity exceeds a threshold and suggest selling
    sell_threshold = 100  # Example threshold, adjust as needed
    stocks_to_sell = [symbol for symbol, quantity in portfolio.items() if quantity > sell_threshold]

    # Write suggestions to file
    with open("portfolio_suggestions.txt", "w") as suggestions_file:
        if stocks_to_sell:
            suggestions_file.write("\nSuggestions:\n")
            for symbol in stocks_to_sell:
                suggestions_file.write(f"Suggestion: Consider selling some shares of {symbol}. Quantity held: {portfolio[symbol]}\n")
        else:
            suggestions_file.write("No suggestions to sell.")

    # Perform additional analysis or visualization as needed


if __name__ == "__main__":
    # Path to the directory containing stock data folders (replace with actual path)
    data_dir = 'data'  # Replace with the actual path to your data directory

    # Load data from multiple files
    stock_data = load_data(data_dir)

    # Load user's portfolio from JSON file
    portfolio_file_path = 'portfolio.json'  # Replace with the path to your portfolio JSON file
    portfolio = load_portfolio(portfolio_file_path)

    # Analyze data for each stock
    analyze_data(stock_data)

    # Analyze the user's portfolio
    analyze_portfolio(portfolio, stock_data)

    # Disclaimer: This analysis is for educational purposes only and does not constitute investment advice.
    print("\nImportant: This code should not be used to make real-world investment decisions. Consult with a financial advisor before making any investment decisions.")
