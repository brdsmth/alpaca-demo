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

## Algorithms

### Scan Options For Relative Volume Delta

To run this algorithm we need to make sure that the `PYTHONPATH=` variable is set in the shell:

`PYTHONPATH=src python3 src/scanners/options_volume.py`

# Alpaca

This project uses data provided by [Alpaca](https://alpaca.markets/)

## Market Data API

[Market Data API](https://docs.alpaca.markets/docs/about-market-data-api)

## Trading API

[Trading API](https://docs.alpaca.markets/docs/trading-api)

Trading functionality currently located in `orders.py` and `positions.py`. To view portfolio run:

`python3 src/positions.py`

### Algorithmic Trading

An example algorithmic trade implementation can be found in `algorithm.py`. To run this algorithm run:

`python3 src/algorithm.py`

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

### Notes

- Python Virtual Environment

`python3 -m venv venv`

`source venv/bin/activate`

`pip install -r requirements.txt`

`deactivate`
