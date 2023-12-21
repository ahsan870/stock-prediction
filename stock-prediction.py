import streamlit as st

def calculate_profit(buy_price, sell_price, quantity):
    buying_cost = buy_price * quantity
    selling_revenue = sell_price * quantity
    profit = selling_revenue - buying_cost
    return profit

def main():
    st.title("Stock Profit Calculator")

    # User input for buying and selling prices
    buy_price = st.text_input("Enter Buying Price:", "0.00")
    sell_price = st.text_input("Enter Selling Price:", "0.00")

    # Convert input values to float
    buy_price = float(buy_price)
    sell_price = float(sell_price)

    # User input for quantity
    quantity = st.number_input("Enter Quantity:", min_value=1, step=1)

    # Calculate profit
    profit = calculate_profit(buy_price, sell_price, quantity)

    # Display results
    st.subheader("Results:")
    st.write(f"Buying Price: ${buy_price:.2f}")
    st.write(f"Selling Price: ${sell_price:.2f}")
    st.write(f"Quantity: {quantity}")
    st.write(f"Total Cost: ${buy_price * quantity:.2f}")
    st.write(f"Total Revenue: ${sell_price * quantity:.2f}")
    st.write(f"Profit: ${profit:.2f}")

if __name__ == "__main__":
    main()
