import time
from market import get_current_stock_price
from orders import buy_stock, sell_stock

symbol = "TSLA"
buy_price = 235.35
sell_price = 238.21
quantity = 1


def trade():
    while True:
        current_price = get_current_stock_price(symbol)

        if current_price <= buy_price:
            print(f"Buying {symbol} at {current_price}")
            buy_stock(symbol=symbol, quantity=quantity)

        elif current_price >= sell_price:
            print(f"Selling {symbol} at {current_price}")
            sell_stock(symbol=symbol, quantity=quantity)

        time.sleep(60)


if __name__ == "__main__":
    trade()
