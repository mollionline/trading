import logging
import pandas as pd

from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder

from project.trades.schemas import PeriodsData

trade_router = APIRouter()

logger = logging.getLogger(__name__)


# Calculate EMA
def calculate_ema(data, length):
    ema_values = []
    for i in range(len(data)):
        if i < length:
            ema_values.append(None)
        else:
            ema = sum(data[i - length:i]) / length  # Simplified EMA calculation
            ema_values.append(ema)
    return ema_values


@trade_router.post("/send_request/")
def form_example_get(request_body: PeriodsData):
    # Load trades data from the CSV file
    body = jsonable_encoder(request_body)
    trades_df = pd.read_csv('uploads/prices.csv')

    # Define candlestick interval (e.g., 5 minutes)
    candlestick_interval = pd.Timedelta(minutes=body['candlestick_intl_per_minutes'])

    # Initialize an empty list to store candlesticks
    candlesticks = []

    # Iterate through trades and form candlesticks
    current_candlestick = None
    for index, trade in trades_df.iterrows():
        timestamp = pd.Timestamp(trade['TS'])
        if current_candlestick is None or timestamp >= current_candlestick['timestamp'] + candlestick_interval:
            if current_candlestick is not None:
                candlesticks.append(current_candlestick)
            current_candlestick = {
                'timestamp': timestamp,
                'open': trade['PRICE'],
                'high': trade['PRICE'],
                'low': trade['PRICE'],
                'close': trade['PRICE']
            }
        else:
            current_candlestick['high'] = max(current_candlestick['high'], trade['PRICE'])
            current_candlestick['low'] = min(current_candlestick['low'], trade['PRICE'])
            current_candlestick['close'] = trade['PRICE']

    # Calculate EMA for Close prices
    close_prices = [candle['close'] for candle in candlesticks]
    ema_14_periods = calculate_ema(close_prices, body['ema_interval'])

    # Print candlesticks and EMA values
    result = []
    for i, candle in enumerate(candlesticks):
        result.append({
            'candlestick': candle,
            f'ema_{body["ema_interval"]}_periods': ema_14_periods[i]
        })
    return {"message": result}
