import time
from datetime import datetime

def measure_latency(start_time, end_time):
    """
    Measure latency in milliseconds.
    """
    latency_ms = (end_time - start_time) * 1000
    return round(latency_ms, 2)

def calculate_spread(bids, asks):
    """
    Calculate the spread between best ask and best bid.
    """
    if not bids or not asks:
        return 0.0

    best_bid = float(bids[0][0])
    best_ask = float(asks[0][0])
    spread = best_ask - best_bid
    return round(spread, 4)

def format_timestamp(timestamp):
    """
    Format a UNIX timestamp to human-readable time.
    """
    try:
        dt = datetime.fromtimestamp(timestamp / 1000.0)
        return dt.strftime('%Y-%m-%d %H:%M:%S')
    except:
        return "Invalid timestamp"
