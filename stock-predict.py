import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


# Function to load stock data and company info
def load_data(ticker):
    stock = yf.Ticker(ticker)
    data = stock.history(period="5y")
    if data.empty:
        raise ValueError(f"No data found for ticker {ticker}.")
    data.reset_index(inplace=True)
    return data, stock.info


# Function to prepare the data
def prepare_data(data):
    data['Date'] = pd.to_datetime(data['Date'])
    data['Date_ordinal'] = data['Date'].map(pd.Timestamp.toordinal)
    X = data[['Date_ordinal']]
    y = data['Close']
    return X, y, data['Date']


# Function to train the model
def train_model(X, y):
    if len(X) > 1:
        model = LinearRegression()
        model.fit(X, y)
        return model
    else:
        raise ValueError("Not enough data points to train the model.")


# Function to plot predictions including future dates
def plot_predictions(model, X, y, dates, days_to_predict=365):
    y_pred = model.predict(X)

    # Extend the date range into the future
    future_dates = pd.date_range(dates.iloc[-1], periods=days_to_predict, freq='D')
    future_X = np.array(future_dates.map(pd.Timestamp.toordinal)).reshape(-1, 1)
    future_pred = model.predict(future_X)

    # Plot results
    plt.figure(figsize=(10, 6))
    plt.plot(dates, y, label="Close Price", color="blue")
    plt.plot(dates, y_pred, label="Predicted Prices", color="orange")
    plt.plot(future_dates, future_pred, label="Future Predictions", color="green", linestyle='dashed')
    plt.title("Stock Price Prediction")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.legend()

    # Improve date formatting on x-axis
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=6))
    plt.gcf().autofmt_xdate()  # Rotate date labels to fit

    plt.grid(True)
    st.pyplot(plt)


# Function to evaluate stock valuation
def evaluate_stock(info, current_price):
    try:
        pe_ratio = info.get('forwardPE')
        avg_price_5y = info.get('fiftyTwoWeekHigh') * 0.7  # Simplified assumption

        if pe_ratio and current_price < avg_price_5y and pe_ratio < 15:
            valuation = "Undervalued"
            advice = "The stock appears to be undervalued based on its P/E ratio and historical price. It might be a good time to buy."
        elif current_price > avg_price_5y:
            valuation = "Overvalued"
            advice = "The stock appears to be overvalued based on its historical price. It might be a good idea to wait for a better entry point."
        else:
            valuation = "Fairly valued"
            advice = "The stock appears to be fairly valued. Consider buying if you believe in the company's future prospects."

        return valuation, advice
    except Exception as e:
        return "Unknown", f"An error occurred during evaluation: {e}"


# Function to calculate moving averages
def calculate_moving_averages(data, short_window=20, long_window=50):
    data['Short_MA'] = data['Close'].rolling(window=short_window).mean()
    data['Long_MA'] = data['Close'].rolling(window=long_window).mean()
    return data


# Function to plot moving averages
def plot_moving_averages(data, ticker):
    plt.figure(figsize=(10, 6))
    plt.plot(data['Date'], data['Close'], label="Close Price", color="blue")
    plt.plot(data['Date'], data['Short_MA'], label=f"Short-Term ({short_window}-day) MA", color="orange")
    plt.plot(data['Date'], data['Long_MA'], label=f"Long-Term ({long_window}-day) MA", color="green")
    plt.title(f"Moving Average Analysis for {ticker.upper()}")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.legend()

    # Improve date formatting on x-axis
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=6))
    plt.gcf().autofmt_xdate()  # Rotate date labels to fit

    plt.grid(True)
    st.pyplot(plt)


# Main layout
st.set_page_config(layout="wide")
st.title("Stock Analysis Tool")

# Sidebar for navigation
st.sidebar.title("Navigation")
option = st.sidebar.radio("Choose a function:", ("Stock Price Prediction", "Moving Average Analysis"))

# Content area layout
col1, col2 = st.columns([1, 3])

if option == "Stock Price Prediction":
    col1.subheader("Stock Price Prediction")
    ticker = col1.text_input("Enter Stock Ticker (e.g., AAPL, MSFT):")  # Input field for the stock ticker

    if col1.button("Predict"):  # Button to trigger the prediction
        if ticker:
            try:
                # Load and prepare data
                data, info = load_data(ticker)

                if data.empty or len(data) < 2:
                    raise ValueError("Not enough data available to make predictions.")

                X, y, dates = prepare_data(data)

                # Train the model
                model = train_model(X, y)

                # Display predictions
                col2.subheader(f"Stock Price Prediction for {ticker.upper()}")
                plot_predictions(model, X, y, dates)

                # Display valuation analysis
                current_price = data['Close'].iloc[-1]
                valuation, advice = evaluate_stock(info, current_price)
                col2.subheader(f"Current Stock Price: ${current_price:.2f}")
                col2.subheader(f"Valuation: {valuation}")
                col2.write(advice)
            except Exception as e:
                col1.error(f"An error occurred: {e}")
        else:
            col1.warning("Please enter a valid stock ticker symbol.")

elif option == "Moving Average Analysis":
    col1.subheader("Moving Average Analysis")
    ticker = col1.text_input("Enter Stock Ticker for Analysis (e.g., AAPL, MSFT):")

    if col1.button("Analyze"):
        if ticker:
            try:
                # Load data and calculate moving averages
                data, _ = load_data(ticker)
                if data.empty:
                    raise ValueError("No data available for the given ticker.")

                short_window = col1.slider("Short-Term Moving Average Window", min_value=5, max_value=50, value=20)
                long_window = col1.slider("Long-Term Moving Average Window", min_value=20, max_value=200, value=50)

                data = calculate_moving_averages(data, short_window, long_window)

                # Plot moving averages
                col2.subheader(f"Moving Average Analysis for {ticker.upper()}")
                plot_moving_averages(data, ticker)
            except Exception as e:
                col1.error(f"An error occurred: {e}")
        else:
            col1.warning("Please enter a valid stock ticker symbol.")
