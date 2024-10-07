from alpaca.data.historical import CryptoHistoricalDataClient
from alpaca.data.requests import CryptoBarsRequest
from alpaca.data.timeframe import TimeFrame
from datetime import datetime, timedelta


def fetch_crypto_data():
    client = CryptoHistoricalDataClient()

    end_date = datetime.now()
    start_date = end_date - timedelta(days=7)

    request_params = CryptoBarsRequest(
        symbol_or_symbols=["BTC/USD"],
        timeframe=TimeFrame.Day,
        start=start_date.isoformat(),
        end=end_date.isoformat(),
    )

    # Retrieve daily bars for BTC
    btc_bars = client.get_crypto_bars(request_params)
    return btc_bars.df


if __name__ == "__main__":
    print(fetch_crypto_data())
