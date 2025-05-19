import websocket
import json

class OrderbookData:
    latest_data = {}

def on_message(ws, message):
    data = json.loads(message)
    OrderbookData.latest_data = data

def on_error(ws, error):
    print("WebSocket Error:", error)

def on_close(ws):
    print("### WebSocket Closed ###")

def on_open(ws):
    print("WebSocket Connection Opened")

def run_websocket():
    ws = websocket.WebSocketApp(
        "wss://ws.gomarket-cpp.goquant.io/ws/l2-orderbook/okx/BTC-USDT-SWAP",
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
        on_open=on_open,
    )
    ws.run_forever()
def on_message(ws, message):
    print("Message received!")  # ADD THIS
    print(message)  # ADD THIS
