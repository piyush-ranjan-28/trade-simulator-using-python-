import asyncio
import streamlit as st
import time
from websocket_client import OrderbookData
from utils import measure_latency, calculate_spread, format_timestamp

st.set_page_config(page_title="GoQuant Trade Simulator", layout="wide")

# --- Streamlit Placeholders ---
st.title("📈 GoQuant Real-Time Crypto Trade Simulator")

col1, col2, col3 = st.columns(3)
spread_placeholder = col1.metric("Spread (USD)", "Loading...")
latency_placeholder = col2.metric("Latency per Tick (ms)", "Loading...")
timestamp_placeholder = col3.metric("Last Update Time", "Loading...")

fee_placeholder = st.metric("Expected Fee (USD)", "Loading...")
market_impact_placeholder = st.metric("Expected Market Impact (USD)", "Loading...")
net_cost_placeholder = st.metric("Net Cost (USD)", "Loading...")
proportion_placeholder = st.metric("Maker / Taker Probability", "Loading...")

# --- Consume WebSocket Data ---
async def consume_orderbook():
    while True:
        try:
            start_time = time.time()
            data = OrderbookData.latest_data

            if data and "data" in data:
                orderbook = data["data"]
                bids = orderbook.get("bids", [])
                asks = orderbook.get("asks", [])
                ts = orderbook.get("timestamp", "")

                # --- Latency ---
                end_time = time.time()
                latency = measure_latency(start_time, end_time)

                # --- Spread ---
                spread = calculate_spread(bids, asks)

                # --- Dummy calculations for example ---
                fee = round(spread * 0.002, 4)
                market_impact = round(spread * 0.015, 4)
                net_cost = round(spread + fee + market_impact, 4)
                maker_taker = {"maker": 0.65, "taker": 0.35}

                # --- Update Streamlit metrics ---
                spread_placeholder.metric("Spread (USD)", spread)
                latency_placeholder.metric("Latency per Tick (ms)", latency)
                timestamp_placeholder.metric("Last Update Time", format_timestamp(ts))
                fee_placeholder.metric("Expected Fee (USD)", fee)
                market_impact_placeholder.metric("Expected Market Impact (USD)", market_impact)
                net_cost_placeholder.metric("Net Cost (USD)", net_cost)
                proportion_placeholder.metric(
                    "Maker / Taker Probability",
                    f'{maker_taker["maker"]} / {maker_taker["taker"]}'
                )

            await asyncio.sleep(1)

        except Exception as e:
            st.error(f"WebSocket Error: {e}")
            break

# --- Run Streamlit App ---
async def run_app():
    await consume_orderbook()

# --- Start the WebSocket consumer ---
asyncio.run(run_app())
