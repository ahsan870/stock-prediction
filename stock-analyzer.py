import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from prophet import Prophet
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings

warnings.filterwarnings('ignore')

# Configure page
st.set_page_config(page_title="Stock Analysis & Prediction App", layout="wide")

def get_stock_data(ticker, period='2y'):
    """Fetch stock data using yfinance"""
    stock = yf.Ticker(ticker)
    df = stock.history(period=period)
    return stock, df

def calculate_technical_indicators(df):
    """Calculate technical indicators"""
    # Moving averages
    df['MA20'] = df['Close'].rolling(window=20).mean()
    df['MA50'] = df['Close'].rolling(window=50).mean()

    # RSI
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))

    return df

def predict_stock_price(df):
    """Predict future stock prices using Prophet"""
    # Prepare data for Prophet
    prophet_df = df.reset_index()[['Date', 'Close']].rename(
        columns={'Date': 'ds', 'Close': 'y'})

    # Remove timezone information from the 'ds' column
    prophet_df['ds'] = prophet_df['ds'].dt.tz_localize(None)

    # Create and fit model
    model = Prophet(daily_seasonality=True, weekly_seasonality=True)
    model.fit(prophet_df)

    # Make future dataframe for prediction (1 year = 365 days)
    future = model.make_future_dataframe(periods=365)
    forecast = model.predict(future)

    return forecast



def calculate_fair_value(stock):
    """Calculate a simple fair value estimate and provide valuation signal"""
    try:
        # Get financial data
        pe_ratio = stock.info.get('forwardPE', None)
        eps = stock.info.get('forwardEps', None)
        current_price = stock.history(period='1d')['Close'][-1]

        # Simple fair value calculation
        if pe_ratio and eps:
            industry_avg_pe = 15  # This is a simplified assumption
            fair_value = eps * industry_avg_pe

            # Determine valuation signal
            if current_price < fair_value:
                signal = "Undervalued"
            elif current_price > fair_value:
                signal = "Overvalued"
            else:
                signal = "Fairly Valued"

            return fair_value, signal

        return None, "Data not available"
    except Exception as e:
        return None, str(e)


def main():
    st.title("📈 Stock Analysis & Prediction App")

    # User input
    ticker = st.text_input("Enter Stock Ticker:", "AAPL").upper()

    # Select period for stock data
    period = st.selectbox("Select period:", ['1mo', '3mo', '6mo', '1y', '2y', '5y'], index=4)

    if st.button("Analyze"):
        with st.spinner('Analyzing stock data...'):
            # Get stock data
            stock, df = get_stock_data(ticker, period=period)

            # Calculate indicators
            df = calculate_technical_indicators(df)

            # Create columns for layout
            col1, col2 = st.columns([2, 1])

            with col1:
                # Stock price chart
                fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                                    vertical_spacing=0.03, row_heights=[0.7, 0.3])

                # Candlestick chart
                fig.add_trace(
                    go.Candlestick(
                        x=df.index,
                        open=df['Open'],
                        high=df['High'],
                        low=df['Low'],
                        close=df['Close'],
                        name='OHLC'
                    ),
                    row=1, col=1
                )

                # Add Moving Averages
                fig.add_trace(
                    go.Scatter(
                        x=df.index,
                        y=df['MA20'],
                        name='MA20',
                        line=dict(color='orange', width=2)
                    ),
                    row=1, col=1
                )

                fig.add_trace(
                    go.Scatter(
                        x=df.index,
                        y=df['MA50'],
                        name='MA50',
                        line=dict(color='blue', width=2)
                    ),
                    row=1, col=1
                )

                # Add RSI
                fig.add_trace(
                    go.Scatter(
                        x=df.index,
                        y=df['RSI'],
                        name='RSI',
                        line=dict(color='purple', width=2)
                    ),
                    row=2, col=1
                )

                # Update layout
                fig.update_layout(
                    title=f'{ticker} Stock Analysis',
                    title_font=dict(size=24),  # Adjust title font size
                    yaxis_title='Stock Price (USD)',
                    yaxis2_title='RSI',
                    xaxis_rangeslider_visible=False,
                    height=800,
                    margin=dict(l=0, r=0, t=80, b=40)
                )

                # Add RSI lines
                fig.add_hline(y=70, line_dash="dash", line_color="red", row=2, col=1)
                fig.add_hline(y=30, line_dash="dash", line_color="green", row=2, col=1)

                st.plotly_chart(fig, use_container_width=True)

                # Display stock data table
                st.dataframe(df.tail())

            with col2:
                # Prophet stock prediction
                st.subheader("Stock Price Prediction (Next 1 Year)")

                forecast = predict_stock_price(df)

                fig2 = go.Figure()

                # Add historical data
                fig2.add_trace(go.Scatter(
                    x=df.index, y=df['Close'], name='Historical',
                    mode='lines', line=dict(color='blue', width=2),
                    hovertemplate="<b>Date:</b> %{x}<br><b>Price:</b> $%{y:.2f}<extra></extra>"
                ))

                # Add forecast data
                fig2.add_trace(go.Scatter(
                    x=forecast['ds'], y=forecast['yhat'], name='Forecast',
                    mode='lines', line=dict(color='green', width=2, dash='dash'),
                    hovertemplate="<b>Forecast Date:</b> %{x}<br><b>Predicted Price:</b> $%{y:.2f}<extra></extra>"
                ))

                # Add upper bound (yhat_upper) for confidence interval
                fig2.add_trace(go.Scatter(
                    x=forecast['ds'], y=forecast['yhat_upper'], name='Upper Bound',
                    mode='lines', line=dict(color='rgba(0, 255, 0, 0.2)', width=0),
                    showlegend=False, hoverinfo='skip'
                ))

                # Add lower bound (yhat_lower) for confidence interval
                fig2.add_trace(go.Scatter(
                    x=forecast['ds'], y=forecast['yhat_lower'], name='Lower Bound',
                    mode='lines', fill='tonexty', fillcolor='rgba(0, 255, 0, 0.1)',
                    line=dict(color='rgba(0, 255, 0, 0.2)', width=0),
                    showlegend=False, hoverinfo='skip'
                ))

                # Customize layout to make it more attractive
                fig2.update_layout(
                    xaxis=dict(
                        title="Date",
                        tickformat="%B",  # Display month names
                        showgrid=True, gridcolor='rgba(200, 200, 200, 0.2)',  # Light grid lines
                    ),
                    yaxis=dict(
                        title="Stock Price (USD)",
                        showgrid=True, gridcolor='rgba(200, 200, 200, 0.2)',  # Light grid lines
                    ),
                    title={
                        'text': f"{ticker} Stock Price Prediction for Next 1 Year",
                        'y': 0.9,
                        'x': 0.5,
                        'xanchor': 'center',
                        'yanchor': 'top',
                        'font': dict(size=24, color='darkblue')  # Title styling
                    },
                    legend=dict(
                        orientation="h",  # Horizontal legend
                        yanchor="bottom", y=1.02, xanchor="center", x=0.5,
                        bgcolor='rgba(255, 255, 255, 0.7)', bordercolor='rgba(0, 0, 0, 0.1)',
                        borderwidth=1
                    ),
                    hovermode="x",  # Hover mode to show details on the x-axis
                    plot_bgcolor='rgba(0, 0, 0, 0)',  # Transparent background
                    paper_bgcolor='rgba(0, 0, 0, 0)',  # Transparent background
                    height=600  # Adjust height
                )

                # Display the chart
                st.plotly_chart(fig2, use_container_width=True)


if __name__ == "__main__":
    main()
