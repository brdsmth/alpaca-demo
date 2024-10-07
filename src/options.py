from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.historical import OptionHistoricalDataClient
from alpaca.data.requests import OptionBarsRequest
from alpaca.data.timeframe import TimeFrame
from datetime import datetime, timedelta
from config import Config


def fetch_options_data():
    client = OptionHistoricalDataClient(
        api_key=Config.APCA_API_KEY_ID, secret_key=Config.APCA_API_SECRET_KEY
    )

    end_date = datetime.now()
    start_date = end_date - timedelta(days=7)

    request_params = OptionBarsRequest(
        symbol_or_symbols=["AAPL241220C00300000"],
        timeframe=TimeFrame.Day,
        start=start_date.isoformat(),
        end=end_date.isoformat(),
    )

    # Retrieve option bars
    stock_bars = client.get_option_bars(request_params)
    df = stock_bars.df

    # Volume spikes over the last 7 days
    df["volume_change"] = df["volume"].pct_change()
    # Volume spike exceeds 20%
    volume_spike_df = df[df["volume_change"] > 0.2]

    return volume_spike_df


if __name__ == "__main__":
    print(fetch_options_data())
