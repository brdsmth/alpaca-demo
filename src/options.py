from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.historical import OptionHistoricalDataClient
from alpaca.data.requests import OptionBarsRequest, OptionChainRequest
from alpaca.data.timeframe import TimeFrame
from datetime import datetime, timedelta
from config.config import Config


def fetch_options_data(symbol):
    client = OptionHistoricalDataClient(
        api_key=Config.APCA_API_KEY_ID, secret_key=Config.APCA_API_SECRET_KEY
    )

    end_date = datetime.now()
    start_date = end_date - timedelta(days=7)

    request_params = OptionBarsRequest(
        symbol_or_symbols=symbol,
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


def get_option_contracts_df(symbol, timeframe):
    client = OptionHistoricalDataClient(
        api_key=Config.APCA_API_KEY_ID, secret_key=Config.APCA_API_SECRET_KEY
    )

    end_date = datetime.now()
    start_date = end_date - timedelta(days=7)

    request_params = OptionBarsRequest(
        symbol_or_symbols=symbol,
        timeframe=timeframe,
        start=start_date.isoformat(),
        end=end_date.isoformat(),
    )

    # Retrieve option bars
    stock_bars = client.get_option_bars(request_params)
    df = stock_bars.df
    return df


def get_available_strike_prices(asset: str, expiration: datetime):
    client = OptionHistoricalDataClient(
        api_key=Config.APCA_API_KEY_ID, secret_key=Config.APCA_API_SECRET_KEY
    )

    # Create request parameters for the option chain
    request_params = OptionChainRequest(
        underlying_symbol=asset.upper(),
        expiration_date_lte=expiration.strftime(
            "%Y-%m-%d"
        ),  # Expiration formatted as YYYY-MM-DD
        type="call",
    )

    try:
        # Fetch all available option contracts (chain) for the asset and expiration date
        option_chain = client.get_option_chain(request_params)

        return option_chain.keys()

    except Exception as e:
        print(f"Error fetching available strike prices: {e}")
        return []


if __name__ == "__main__":
    # print(fetch_options_data())

    asset = "TSLA"  # Stock symbol
    expiration = datetime(2024, 10, 11)
    strike_prices = get_available_strike_prices(asset, expiration)

    print("available strike prices", strike_prices)
    print(list(strike_prices)[0])
    first_strike_price = list(strike_prices)[0]
    print("sample volume spike", fetch_options_data(first_strike_price))
