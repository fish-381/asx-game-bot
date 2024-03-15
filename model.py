import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

# Function to load data from CSV file (assuming 'stock_data.csv' is in the same directory)
def load_data():
    try:
        data = pd.read_csv('stock_data.csv', index_col='Date', parse_dates=True)
        return data
    except FileNotFoundError:
        print("Error: 'stock_data.csv' file not found. Please ensure it exists in the same directory.")
        return None

# Function to preprocess data
def preprocess_data(data):
    # Fill missing values using forward fill method (adjust if needed)
    data.fillna(method='ffill', inplace=True)

    # Replace infinite values with a large finite number (carefully consider alternatives)
    data.replace([np.inf, -np.inf], 1e10, inplace=True)  # Replace with a suitable large value

    # Print summary statistics
    print("\nSummary Statistics after preprocessing:")
    print(data.describe())

    # Calculate 10-day moving average (consider more appropriate technical indicators)
    data['10_day_ma'] = data['Close'].rolling(window=10).mean()

    return data

# Function to split data into features and target
def split_data(data):
    # Drop the first 10 rows due to NaN values in the moving average
    data = data.iloc[10:]

    X = data[['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume', '10_day_ma']]
    y = data['Close']  # Predict actual closing price

    return X, y

# Function to train linear regression model
def train_model(X_train, y_train):
    model = LinearRegression()
    model.fit(X_train, y_train)
    return model

# Function to evaluate model
def evaluate_model(model, X_test, y_test):
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    print("\nMean Squared Error:", mse)
    return mse

# Main function
def main():
    # Load data
    data = load_data()
    if data is None:  # Handle potential file not found error
        return

    # Preprocess data
    data = preprocess_data(data.copy())  # Avoid modifying original data

    # Split data
    X, y = split_data(data)

    # Split data into training and testing sets (consider cross-validation for better evaluation)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train model
    model = train_model(X_train, y_train)

    # Evaluate model
    evaluate_model(model, X_test, y_test)

if __name__ == "__main__":
    main()
