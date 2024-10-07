# Alpaca Demo

## Running Locally

Set up virtual python environment and install requirements. Fill out a `.env` file with the environment variables in `.env.example`.

```
python src/main.py
```

To run either the `crypto` or `options` package separately, run:

```
python src/options.py
```

```
python src/crypto.py
```

# Alpaca

This project uses the [Market Data API](https://docs.alpaca.markets/docs/about-market-data-api) provided by [Alpaca](https://alpaca.markets/)

## Market Data API

[Market Data API](https://docs.alpaca.markets/docs/about-market-data-api)

### Historical API

Historical data is taken from the Market Data API.

#### Options

Contract Symbols

```

[Asset][Expiration Year][Expiration Month][Expiration Day][Call or Put][Strike Price]

```

```

[AAPL][24][12][20][C][00300000]

```

e.g.

```

AAPL241220C00300000

```

Where 00300000 equals $300.00. The first 5 digits (00300) represent the dollar amount, the last two digits representing the cents. The leading and trailing zeros are used for padding.

```

```
