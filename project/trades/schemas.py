from pydantic import BaseModel

"""Request body with minute and ema_period"""


class PeriodsData(BaseModel):
    candlestick_intl_per_minutes: int = 200
    ema_interval: int = 22
