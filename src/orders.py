from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce
from config import Config

# Using the Paper Trading API
trading_client = TradingClient(
    api_key=Config.APCA_API_KEY_ID, secret_key=Config.APCA_API_SECRET_KEY, paper=True
)


def place_market_order(symbol, quantity, side, time):

    market_order_data = MarketOrderRequest(
        symbol=symbol, qty=quantity, side=side, time_in_force=time
    )
    market_order = trading_client.submit_order(order_data=market_order_data)

    return market_order


def buy_stock(symbol, quantity):
    return place_market_order(
        symbol=symbol, quantity=quantity, side=OrderSide.BUY, time=TimeInForce.DAY
    )


def buy_crypto(symbol, quantity):
    return place_market_order(
        symbol=symbol, quantity=quantity, side=OrderSide.BUY, time=TimeInForce.GTC
    )


def sell_stock(symbol, quantity):
    return place_market_order(
        symbol=symbol, quantity=quantity, side=OrderSide.SELL, time=TimeInForce.DAY
    )


def sell_crypto(symbol, quantity):
    return place_market_order(
        symbol=symbol, quantity=quantity, side=OrderSide.SELL, time=TimeInForce.GTC
    )


if __name__ == "__main__":
    buy_crypto(
        symbol="ETHUSD",
        quantity="0.015",
    )
