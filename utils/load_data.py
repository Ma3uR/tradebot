import pandas as pd
import numpy as np
from binance.client import Client
from binance.enums import HistoricalKlinesType
from datetime import datetime

symbol = "BTCUSDT"
interval = "1m"
start_date = "2019-10-01T00:00:00"
end_date = "2023-10-01T00:00:00"
klines_type = HistoricalKlinesType.FUTURES
days = (datetime.strptime(end_date, '%Y-%m-%dT%H:%M:%S')
        - datetime.strptime(start_date, '%Y-%m-%dT%H:%M:%S')).days
client = Client()
klines = client.get_historical_klines(symbol, interval, start_date, end_date, klines_type=klines_type)

df = pd.DataFrame(klines, columns=[
    "Timestamp", "Open", "High", "Low", "Close", "Volume", "CloseTime", "QuoteVolume", "NumberOfTrades",
    "TakerBuyBaseVolume", "TakerBuyQuoteVolume", "Ignore",
])

df["DateTime"] = pd.to_datetime(df["Timestamp"], unit='ms').dt.strftime('%Y-%m-%d %H:%M')
df.set_index("DateTime", inplace=True)
print(f"{df=}")

df.to_csv(f'data/test_data{symbol}_{interval}_{start_date[:-9]}_{days}days.csv')
