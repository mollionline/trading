import matplotlib.pyplot as plt
import mplfinance as mpf
import pandas as pd

df = pd.read_csv("uploads/response.csv", header=[0, 1], index_col=[0])
df.index = pd.to_datetime(df.index)
ema_period = int(df["ema_period"].values[0][0])
mpf.plot(
    df["PRICE"],
    type="line",
    style="yahoo",
    title="Candlestick Chart with EMA",
    ylabel="Price",
    mav=(ema_period,),
)
plt.xticks(rotation=45)
plt.title("Candlestick Chart with EMA")
plt.xlabel("Timestamp")
plt.ylabel("Price")
plt.plot(
    df.index, df["EMA"], label=f"EMA ({ema_period} periods)", color="blue"
)  # noqa E 501
plt.legend()
plt.tight_layout()
plt.show()
