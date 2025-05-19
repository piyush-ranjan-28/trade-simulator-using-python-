import streamlit as st
import asyncio
import websockets
import json
import time

from models import estimate_slippage, estimate_market_impact, calculate_fee, predict_maker_taker_probability
from utils import measure_latency, calculate_spread, format_timestamp

# --- UI: Left Panel ---
st.set_page_config(page_title="GoQuant Trade Simulator", layout="wide")
st.title("📈 Real-Time Crypto Trade Simulator")

with st.sidebar:
    st.header("Trade Input Parameters")
    exchange = st.selectbox("Exchange", ["OKX"])
    asset = st.selectbox("Spot Asset", ["BTC-USDT-SWAP"])
    order_type = st.selectbox("Order Type", ["Market"])
    order_size = st.slider("Order Size (USD)", min_value=10, max_value=1000, step=10, value=100)
    volatility = st.slider("Volatility (0-0.1)", min_value=0.0, max_value=0.1, step=0.005, value=0.02)
    fee_tier = st.selectbox("Fee Tier", ["Regular", "VIP", "Pro"])

# --- UI: Right Panel Outputs ---
col1, col2 = st.columns(2)
with col1:
    slippage_placeholder = st.metric("Expected Slippage (USD)", "Waiting...")
    fees_placeholder = st.metric("Expected Fee (USD)", "Waiting...")
    market_impact_placeholder = st.metric("Expected Market Impact (USD)", "Waiting...")
with col2:
    net_cost_placeholder = st.metric("Net Cost (USD)", "Waiting...")
    proportion_placeholder = st.metric("Maker / Taker Probability", "Waiting...")
    latency_placeholder = st.metric("Latency per Tick (ms)", "Waiting...")

# --- WebSocket Connection ---
async def consume_orderbook():
    url = "wss://ws.gomarket-cpp.goquant.io/ws/l2-orderbook/okx/BTC-USDT-SWAP"

    async with websockets.connect(url) as ws:
        while True:
            try:
                start_time = time.time()
                msg = await ws.recv()
                data = json.loads(msg)

                timestamp = format_timestamp(data["timestamp"])
                asks = data["asks"]
                bids = data["bids"]

                # --- Model Calculations ---
                slippage = estimate_slippage(order_size, asks)
                spread = calculate_spread(asks, bids)
                fee = calculate_fee(order_size, fee_tier)
                market_impact = estimate_market_impact(order_size, volatility)
                net_cost = round(slippage + fee + market_impact, 6)

                maker_taker = predict_maker_taker_probability(
                    [volatility, order_size, spread, fee]
                )
                latency = measure_latency(start_time)

                # --- Update UI ---
                slippage_placeholder.metric("Expected Slippage (USD)", slippage)
                fees_placeholder.metric("Expected Fee (USD)", fee)
                market_impact_placeholder.metric("Expected Market Impact (USD)", market_impact)
                net_cost_placeholder.metric("Net Cost (USD)", net_cost)
                proportion_placeholder.metric("Maker / Taker Probability", f'{maker_taker["maker"]} / {maker_taker["taker"]}')
                latency_placeholder.metric("Latency per Tick (ms)", latency)

            except Exception as e:
                st.error(f"WebSocket Error: {e}")
                break

# --- Run Streamlit App with Async Loop ---
async def run_app():
    await consume_orderbook()

# Start the WebSocket listener
asyncio.run(run_app())
