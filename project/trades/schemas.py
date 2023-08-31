from pydantic import BaseModel


class PeriodsData(BaseModel):
   candlestick_intl_per_minutes: int = 5
   ema_interval: int = 14