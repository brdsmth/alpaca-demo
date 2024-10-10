from datetime import datetime, timedelta
from alpaca.data.historical import OptionHistoricalDataClient
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import GetAssetsRequest
from alpaca.trading.enums import AssetClass, AssetStatus, AssetExchange
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.historical import OptionHistoricalDataClient
from alpaca.data.requests import (
    OptionBarsRequest,
    OptionChainRequest,
    StockLatestTradeRequest,
)
from alpaca.data.timeframe import TimeFrame
from config.config import Config
from log.log import logfn
import pytz
import pandas as pd

"""
This is currently an isolated program
These functions should be separated out into different packages for easier reuse
"""

alpacaOptions = OptionHistoricalDataClient(
    api_key=Config.APCA_API_KEY_ID, secret_key=Config.APCA_API_SECRET_KEY
)

alpacaTrading = TradingClient(
    api_key=Config.APCA_API_KEY_ID, secret_key=Config.APCA_API_SECRET_KEY
)

alpacaMarket = StockHistoricalDataClient(
    api_key=Config.APCA_API_KEY_ID,
    secret_key=Config.APCA_API_SECRET_KEY,
)


def fetch_option_bars(symbol, lookback_for_dataset_days):

    # We set an interval - lookback_for_dataset_days - for which to get trading bar data
    # The timeframe for each bar is set below as 1 hour (TimeFrame.Hour)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=lookback_for_dataset_days)

    request_params = OptionBarsRequest(
        symbol_or_symbols=symbol,
        timeframe=TimeFrame.Hour,
        start=start_date.isoformat(),
        end=end_date.isoformat(),
    )

    option_bars = alpacaOptions.get_option_bars(request_params)

    return option_bars


def fetch_options_chain(symbol, current_price):
    now = datetime.now()
    three_months_from_now = now + timedelta(days=90)
    # one_year_from_now = now + timedelta(days=365)

    request_params = OptionChainRequest(
        underlying_symbol=symbol.upper(),
        type="call",
        expiration_date_lte=three_months_from_now.strftime("%Y-%m-%d"),
        strike_price_gte=current_price,
    )

    options_chain = alpacaOptions.get_option_chain(request_params)

    return options_chain


def scan_for_valid_contracts(num_of_assets_to_scan, lookback_for_dataset_days):

    search_params = GetAssetsRequest(
        asset_class=AssetClass.US_EQUITY,
        status=AssetStatus.ACTIVE,
        attributes="has_options",
        exchange=AssetExchange.NASDAQ,
    )
    assets = alpacaTrading.get_all_assets(search_params)

    valid_dataframes = []

    asset_counter = 0
    for asset in assets:
        logfn("\n---> count", asset_counter)
        logfn("---> asset\n", asset.symbol)

        request_params = StockLatestTradeRequest(symbol_or_symbols=asset.symbol)
        latest_trade = alpacaMarket.get_stock_latest_trade(
            request_params=request_params
        )
        current_price = latest_trade.get(asset.symbol).price
        logfn("---> current price", current_price)
        options_chain = fetch_options_chain(asset.symbol, current_price=current_price)

        if len(options_chain) == 0:
            logfn("---> no chain data for", asset.symbol)
            continue

        available_strike_prices = options_chain.keys()

        for strike_price in available_strike_prices:
            logfn("---> strike price", strike_price)
            option_bars = fetch_option_bars(strike_price, lookback_for_dataset_days)
            option_bars_df = option_bars.df

            if option_bars_df.size == 0:
                logfn(
                    "---> no option bars for %s in last %d days"
                    % (strike_price, lookback_for_dataset_days)
                )
                continue

            valid_dataframes.append(option_bars_df)

        asset_counter += 1

        # Just here to control the number of assets we're scanning
        if asset_counter > num_of_assets_to_scan:
            break

    if len(valid_dataframes) == 0:
        print("---> no valid dataframes, asset sample size too small")
        return

    combined_dataframe = pd.concat(valid_dataframes)

    # Calculate average volume for the number of days set at lookback_for_dataset_days
    # We reset the index so that we have clean grouping
    combined_dataframe = combined_dataframe.reset_index()
    combined_dataframe["average_volume"] = combined_dataframe.groupby("symbol")[
        "volume"
    ].transform("mean")

    logfn("---> combined dataframes \n", combined_dataframe)

    return combined_dataframe


def calculate_relative_volume(
    contracts_df: pd.DataFrame, start_date, end_date, lookback_for_volume_change_hours
):
    print("---> calculate relative volume")
    print("---> lookback start", start_date)
    print("---> lookback end", end_date)

    # Filter dataframe for the lookback interval
    lookback_df = contracts_df.loc[contracts_df["timestamp"] >= start_date].copy()

    if lookback_df.size == 0:
        print(
            "---> no valid contracts within %d last hours"
            % lookback_for_volume_change_hours
        )
        return

    # Calculate relative change in volume for lookback time compared to average
    lookback_df["relative_volume_change"] = (
        lookback_df["volume"] - lookback_df["average_volume"]
    ) / lookback_df["average_volume"]

    return lookback_df


def filter_df_by_relative_volume(lookback_df, relative_volume_threshold):
    print("---> filter by relative volume")

    # Filter the DataFrame where relative_volume_change is greater than the threshold
    filtered_df = lookback_df.loc[
        lookback_df["relative_volume_change"] >= relative_volume_threshold
    ]

    return filtered_df


def option_volume_scanner(
    reading_from_csv,
    num_of_assets_to_scan,
    relative_volume_threshold,
    lookback_for_dataset_days,
    lookback_for_volume_change_hours,
    end_date,
    start_date,
):

    # Testing is sometimes easier by reading from csv
    # We use this flag to bypass the scan and read from a prescanned csv
    if reading_from_csv != True:
        valid_contracts = scan_for_valid_contracts(
            num_of_assets_to_scan, lookback_for_dataset_days
        )
        valid_contracts.to_csv("dev/data/valid_contracts.csv")
    else:
        valid_contracts = pd.read_csv("dev/data/valid_contracts.csv", index_col=0)
        valid_contracts["timestamp"] = pd.to_datetime(valid_contracts["timestamp"])

    if valid_contracts is not None:

        lookback_df = calculate_relative_volume(
            start_date=start_date,
            end_date=end_date,
            contracts_df=valid_contracts,
            lookback_for_volume_change_hours=lookback_for_volume_change_hours,
        )

        if lookback_df is not None:
            logfn("---> lookback df\n", lookback_df)
            filtered_df = filter_df_by_relative_volume(
                lookback_df=lookback_df,
                relative_volume_threshold=relative_volume_threshold,
            )

            if filtered_df.size == 0:
                print(
                    "---> no valid contracts above %d percent increase"
                    % (relative_volume_threshold * 100)
                )
            else:
                print("---> filtered df\n", filtered_df)

    else:
        print("---> no valid contracts to calculate volume change")


if __name__ == "__main__":

    reading_from_csv = False
    num_of_assets_to_scan = 5
    relative_volume_threshold = (
        # 2  # e.g. 200% increase in volume compared to average
        0.5  # e.g. 50% increase in volume compare to average
    )

    lookback_for_dataset_days = 7
    lookback_for_volume_change_hours = 24
    end_date = datetime.now(pytz.UTC)
    start_date = end_date - timedelta(hours=lookback_for_volume_change_hours)

    option_volume_scanner(
        reading_from_csv=reading_from_csv,
        num_of_assets_to_scan=num_of_assets_to_scan,
        relative_volume_threshold=relative_volume_threshold,
        lookback_for_dataset_days=lookback_for_dataset_days,
        lookback_for_volume_change_hours=lookback_for_volume_change_hours,
        end_date=end_date,
        start_date=start_date,
    )
