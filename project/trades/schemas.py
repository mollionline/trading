from pydantic import BaseModel


class PeriodsData(BaseModel):
    candlestick_intl_per_minutes: int = 200
    ema_interval: int = 22
