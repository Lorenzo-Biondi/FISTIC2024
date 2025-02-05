import streamlit as st
from meteostat import Point, Daily
import geopy
import matplotlib.pyplot as plt
import datetime

start = datetime(2019, 1, 1)
end = datetime(2025, 1, 21)

cities = {'Foggia':[41.461761,15.54502]}

def get_city():
    cities = {'Foggia':[41.461761,15.54502]}
    city = Point(list(cities.values())[0][0],list(cities.values())[0][1], 20)

    data = Daily(city, start, end)
    data = data.fetch()
    data['city'] = list(cities.keys())[0]

def main():
    # Set up the Streamlit page
    st.set_page_config(page_title="FO(ggia)casting", layout="wide")
    st.title("🚀 Che tempo fa a Foggia")
    st.markdown("""
        Real time data retrieval e forecasting di temperatura
    """)

    # Sidebar for user inputs
    with st.sidebar:
        st.header("Impostazioni")

        city_choice = st.selectbox("Scegli la città", [
            "Foggia"
        ])

    # Display the current portfolio
    st.subheader("📊 Attuale temperatura")
    col1, col2, col3 = st.columns(2)
    with col1:
        st.markdown("Città selezionata", f"{list(cities.keys())[0]}")
    with col2:
        st.metric("Current USD Balance", f"${st.session_state.bot.current_balance:.2f}")

    # Display Key Metrics and Performance Metrics in two columns
    st.subheader("📈 Metrics")
    col1, col2 = st.columns(2)

    with col1:
        # Key Metrics
        st.markdown("### Key Metrics")

    with col2:
        # Performance Metrics
        st.markdown("### Performance Metrics")

    # Display the price chart
    st.subheader("📈 BTC Price Over Time")
    chart_placeholder = st.empty()

    # Placeholder for transaction history
    transaction_history_placeholder = st.empty()

    # Simulate trades and update the chart
    while True:
        # Fetch the current price
        current_price = get_current_price()
        if current_price is not None:
            st.session_state.prices.append(current_price)
            st.session_state.timestamps.append(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

            # Update the bot's price history
            st.session_state.bot.price_history = st.session_state.prices

            # Calculate Bollinger Bands for the entire price history
            if len(st.session_state.prices) >= 20:  # Ensure enough data for Bollinger Bands
                upper_band, ma, lower_band = bollinger_bands(st.session_state.prices)
            else:
                upper_band, ma, lower_band = None, None, None

            # Update the chart
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=st.session_state.timestamps, y=st.session_state.prices, mode='lines', name='BTC Price'))
            
            # Add Bollinger Bands to the chart
            if upper_band is not None and ma is not None and lower_band is not None:
                fig.add_trace(go.Scatter(x=st.session_state.timestamps[-len(upper_band):], y=upper_band, mode='lines', name='Upper Band'))
                fig.add_trace(go.Scatter(x=st.session_state.timestamps[-len(ma):], y=ma, mode='lines', name='Moving Average'))
                fig.add_trace(go.Scatter(x=st.session_state.timestamps[-len(lower_band):], y=lower_band, mode='lines', name='Lower Band'))
            
            fig.update_layout(
                title="BTC Price Trend Over Time",
                xaxis_title="Time",
                yaxis_title="Price in USD",
                template="plotly_dark"
            )
            chart_placeholder.plotly_chart(fig, use_container_width=True)

            # Update transaction history
            with transaction_history_placeholder.container():
                st.subheader("📜 Transaction History")
                if st.session_state.bot.transactions:
                    st.table(st.session_state.bot.transactions)
                else:
                    st.info("No transactions yet.")

            # Simulate a trade
            st.session_state.bot.simulate_trade(investment_amount)

        # Wait for 1 second before the next update
        time.sleep(1)

# Run the Streamlit app
if __name__ == "__main__":
    main()