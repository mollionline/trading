import logging

import pandas as pd
from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder

from project.trades.schemas import PeriodsData

trade_router = APIRouter()

logger = logging.getLogger(__name__)


@trade_router.post("/send_request/")
def form_example_get(request_body: PeriodsData):
    # Load trades data from the CSV file
    body = jsonable_encoder(request_body)
    # Read the CSV file into a DataFrame
    df = pd.read_csv("uploads/prices.csv")
    df["Timestamp"] = pd.to_datetime(df["TS"])
    df.set_index("Timestamp", inplace=True)

    # Resample the data to form candlesticks
    time_interval = f"{body['candlestick_intl_per_minutes']}T"  # 5 minutes
    ohlc_dict = {
        "PRICE": "ohlc",
    }
    candlesticks = df.resample(time_interval).apply(ohlc_dict).dropna()

    # Calculate Exponential Moving Average (EMA)
    ema_period = body["ema_interval"]
    candlesticks["EMA"] = (
        candlesticks["PRICE"]["close"]
        .ewm(span=ema_period, adjust=False)
        .mean()  # noqa E 501
    )
    candlesticks["ema_period"] = ema_period

    candlesticks.to_csv("uploads/response.csv")
    return {"response": "go to uploads/response.csv"}
