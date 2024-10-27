from alpaca.trading.client import TradingClient
from config.config import Config
from tabulate import tabulate

trading_client = TradingClient(
    api_key=Config.APCA_API_KEY_ID,
    secret_key=Config.APCA_API_SECRET_KEY,
)


# Get a list of all positions
def get_portfolio():
    portfolio = trading_client.get_all_positions()

    table_data = []
    headers = ["Symbol", "Quantity", "Market Value", "Cost Basis", "Unrealized P/L"]

    for position in portfolio:
        table_data.append(
            [
                position.symbol,
                position.qty,
                position.market_value,
                position.cost_basis,
                position.unrealized_pl,
            ]
        )

    print(tabulate(table_data, headers=headers, tablefmt="grid"))


# Get a single position
def get_position(symbol):
    position = trading_client.get_open_position(symbol)

    table_data = []
    headers = [
        "Symbol",
        "Quantity",
        "Avg. Entry Price",
        "Current Price",
        "Cost Basis",
        "Market Value",
        "Unrealized P/L",
        "Percent Profit",
    ]

    percent_profit = (
        float(position.current_price) / float(position.avg_entry_price)
    ) - 1

    table_data.append(
        [
            position.symbol,
            position.qty,
            position.avg_entry_price,
            position.current_price,
            position.cost_basis,
            position.market_value,
            position.unrealized_pl,
            percent_profit * 100,
        ]
    )

    print(tabulate(table_data, headers=headers, tablefmt="grid"))
    return position


if __name__ == "__main__":
    get_portfolio()
    # get_position("TSLA241011C00130000")
