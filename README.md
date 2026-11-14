# Binance Futures Trading Bot (ETHBUSD)

**TLDR:** Automated Futures bot made in 2021. Turned a profit until october 2022, ethereum changed from POW to POS and traded volume fell significantly. There was no major Generative Ai easily avilable at the time of creation, This coded was conceived thorugh a lot of StackOverflow and frustration.
<br>
<br>
Automated trading bot for executing futures orders on Binance, focused on the **ETHBUSD** pair.
The script operates based on technical analysis signals from **TradingView** and flow indicators (volume/rate) from the Binance API, executing market orders at short intervals.

---

## Important Security Notice

**The Binance API keys are hardcoded in the file.**

> **Note:** The keys present in the source code are **expired/revoked** and no longer represent a security risk. They are kept in the code for reference purposes only.

Before running, **replace them with your own keys** and, ideally, move them to environment variables or a `.env` file. Never share or version active API keys in public repositories.

---

## Features

- **Automated Technical Analysis**: consumes TradingView recommendations (BUY, SELL, NEUTRAL) for the ETHBUSD pair on the 15-minute timeframe.
- **Order Execution**: sends market orders (MARKET) on Binance Futures, with support for long and short positions.
- **Position Management**: checks current position, mark price, and dynamically calculates order size based on available balance and configured leverage.
- **Flow Filter**: uses volume/rate data from 1h Binance k-lines to determine if the market has enough flow to operate.
- **Continuous Loop**: runs indefinitely with automatic reconnection in case of errors.
- **Logging**: records all orders and errors via `logging`.

---

## Requirements

- Python 3.8+
- Binance account with **Futures enabled**
- API keys with read and futures trading permissions

---

## Dependencies

Install the required libraries via pip:

```bash
pip install pandas requests python-binance tradingview-ta
```

Libraries used:
- `python-binance` – Binance API integration (spot and futures)
- `pandas` – price data manipulation
- `requests` – HTTP requests to Binance endpoints
- `tradingview-ta` – retrieval of TradingView technical signals

---

## Configuration

1. **Clone or copy** the `futures.py` file to your local environment.
2. **Set up your API keys** (recommended via environment variables):

```bash
export BINANCE_API_KEY="your_api_key"
export BINANCE_API_SECRET="your_api_secret"
```

3. **Adjust the parameters in the script** if necessary:
   - `leverage = 5` – leverage used (default: 5x)
   - `symbol = "ETHBUSD"` – traded pair
   - Volume/rate thresholds for bot activation
   - Sleep intervals and data refresh timing

---

## Usage

Run the bot directly from the terminal:

```bash
python futures.py
```

The bot will start by checking your current position, balance, and market price, entering a continuous loop of:
1. Querying TradingView technical signals
2. Checking flow/volume via the Binance API
3. Executing or reversing positions according to the signal and current position

To stop, use `Ctrl+C`.

---

## Code Structure

| Function | Description |
|----------|-------------|
| `te()` | Tests connectivity with the Binance futures API |
| `search()` | Searches for balance of specific assets in the account |
| `simbolo()` | Gets quantity precision for the ETHUSD_PERP pair |
| `a()` | Returns available BUSD balance in the futures account |
| `compra()` | **(Not used)** Sends a sell (short) market order – legacy code |
| `liquida()` | **(Not used)** Sends a buy order to reduce a short position – legacy code |
| `b()` | Identifies whether the current position is long, short, or neutral |
| `preco()` | Returns the mark price of the ETHBUSD position |
| `quantidade()` | Calculates order size based on balance, leverage, and price |
| `pegaposicao()` | Updates the global variable for the current position |
| `mudanca()` | Executes orders according to the new signal (buy/sell/neutral) – **main flow** |
| `vendertudo()` | Intelligently closes open positions (reduceOnly) – **main flow** |
| `verifica()` | Compares current position with the latest signal and triggers reversal if needed – **main flow** |
| `pegafluxo()` | Fetches candles (klines) from 1h and 15m for volume analysis |
| `ping()` | Main loop: evaluates signals, flow, and executes orders – **main flow** |
| `attempts()` | Reconnection wrapper with exception handling – **main flow** |

> **Note on unused functions:** `compra()` and `liquida()` are defined in the code but **are never called** during execution. The active order execution logic is entirely contained within `mudanca()` and `vendertudo()`, which are invoked by the main flow via `verifica()` → `ping()` → `attempts()`.

---

## Operation Flow

1. **Initialization**: checks current position and calculates base quantity.
2. **Data Collection**: fetches 1h and 15m candles from Binance, the data frame is valid for 2 minutes than its refreshed to save bandwidth.
3. **Flow Analysis**: if volume/rate is above the threshold, proceeds.
4. **Technical Signal**: queries TradingView recommendation.
5. **Execution**:
   - If the signal differs from the current position, closes the open position and opens the new one.
   - If flow is insufficient or the signal is neutral, holds or closes positions.
6. **Waits 5 seconds** and repeats the cycle.

---

## Error Handling

- Binance exceptions are caught and logged via `logging.error`.
- Connectivity failures or timeouts trigger a retry after 5 seconds.
- The main loop is protected by `attempts()` to prevent the bot from stopping due to temporary errors.

---

## Notes and Limitations

- The bot was designed to operate **exclusively with ETHBUSD**; adaptations for other pairs require adjustments to the `symbol` parameter and quantity precision.
- The liquidation quantity (`vendertudo()`) is partially hardcoded in some flows (e.g., `quantity=10`) – review according to your capital.
- The code uses global variables for state control (`posicao`, `last_order`, `response`, etc.).
- **Legacy functions:** `compra()` and `liquida()` are dead code (orphan functions) that are not part of the current execution flow. They may be removed or reactivated if you choose to refactor the order execution structure.
- Extensive testing on **testnet** is recommended before operating with real capital.

---

## License

This project is for personal and educational use.
The author is not responsible for financial losses. Use at your own risk.
