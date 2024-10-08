from alpaca.trading.client import TradingClient
from config import Config
from tabulate import tabulate

trading_client = TradingClient(
    api_key=Config.APCA_API_KEY_ID,
    secret_key=Config.APCA_API_SECRET_KEY,
)


def get_portfolio():
    # Get a list of all of our positions.
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


if __name__ == "__main__":
    get_portfolio()
