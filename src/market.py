from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockLatestBarRequest
from alpaca.data.timeframe import TimeFrame
from datetime import datetime, timedelta
from config import Config

stock_client = StockHistoricalDataClient(
    api_key=Config.APCA_API_KEY_ID,
    secret_key=Config.APCA_API_SECRET_KEY,
)


def get_current_stock_price(symbol):

    request_params = StockLatestBarRequest(
        symbol_or_symbols=[symbol],
    )

    stock_bar = stock_client.get_stock_latest_bar(request_params=request_params)
    bar = stock_bar[symbol]

    return bar.vwap


if __name__ == "__main__":
    get_current_stock_price("TSLA")
