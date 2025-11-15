# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

Blankly is a Python framework for rapidly building, backtesting, and deploying quantitative trading strategies across multiple exchanges (crypto, stocks, forex, futures). The same code runs in backtesting and live trading by changing a single line.

**Key Philosophy**: Write once, run anywhere - strategies are exchange-agnostic through a unified interface abstraction.

**Tech Stack**:
- **Language**: Pure Python (187+ Python files, no compiled extensions)
- **Package Management**: Legacy `setup.py` with setuptools (pre-2020 style)
- **Version**: v1.18.11-beta
- **License**: LGPL-3.0
- **Distribution**: Published to PyPI as `blankly`

**Project Structure Note**: This project uses traditional `setup.py` rather than modern `pyproject.toml` (PEP 518/621). It does NOT use UV, Poetry, or Pipenv. Dependencies are managed manually through `setup.py` without lockfiles. Consider migrating to modern tools for better dependency resolution and faster installs.

## Installation & Setup

### From PyPI (Recommended for Users)

```bash
# Install from PyPI
pip install blankly

# Initialize new project
blankly init
```

### From Source (Development)

```bash
# Clone repository
git clone https://github.com/Blankly-Finance/Blankly.git
cd blankly

# Install package in development mode (editable install)
pip install -e .

# Install testing dependencies
pip install pytest pytest-mock

# Run tests
pytest

# Run specific test file
pytest tests/test_auth_constructor.py

# Run specific test
pytest tests/test_auth_constructor.py::TestAuthConstructor::test_specific_method
```

### Optional: Using UV (Faster Alternative)

While this project doesn't officially use UV, you can use it for faster installs:

```bash
# Install with UV (if available)
uv pip install -e .
uv pip install pytest pytest-mock

# UV provides significantly faster dependency resolution and installation
```

### Configuration Files

The `blankly init` CLI command creates these files:
- `keys.json` - Exchange API credentials
- `settings.json` - Exchange-specific preferences (fees, websocket settings)
- `backtest.json` - Backtesting parameters
- `blankly.json` - Deployment settings

Test keys should be placed in `tests/config/keys.json`.

## Build & Test Commands

### Testing

```bash
# Run all tests (from repo root)
pytest

# Run with verbose output
pytest -v

# Run specific test directory
pytest tests/exchanges/
pytest tests/indicators/
pytest tests/strategy/

# Run single test file
pytest tests/test_auth_constructor.py

# Run specific test method
pytest tests/test_auth_constructor.py::TestAuthConstructor::test_method_name -v

# Generate coverage report
pytest --cov=blankly tests/

# Test with specific Python version
python3.10 -m pytest
```

### Building & Distribution

```bash
# Build distribution packages (wheel + source)
python3 -m build

# This creates:
# - dist/blankly-{version}-py3-none-any.whl
# - dist/blankly-{version}.tar.gz

# Upload to PyPI (maintainers only, requires auth)
twine upload dist/*

# Install locally built package
pip install dist/blankly-{version}-py3-none-any.whl
```

### Code Formatting

```bash
# Format code with yapf (PEP 8 style)
yapf -i blankly/**/*.py

# Check formatting without changes
yapf -d blankly/**/*.py
```

## High-Level Architecture

### Three-Layer Exchange Abstraction

```
User Code (Strategy/Model/Screener)
         ↓
Exchange Layer (Exchange/FuturesExchange)
  - Portfolio management
  - Model lifecycle
  - Authentication
         ↓
Interface Layer (ExchangeInterface/FuturesExchangeInterface)
  - Homogenized trading operations
  - Order management
  - Account queries
  - Historical data
         ↓
API Layer (Exchange-specific REST/WebSocket clients)
  - Raw exchange communication
```

**Key Files**:
- `blankly/exchanges/exchange.py` - Base exchange class for spot trading
- `blankly/exchanges/futures/futures_exchange.py` - Futures exchange wrapper
- `blankly/exchanges/interfaces/abc_exchange_interface.py` - Interface contract
- `blankly/exchanges/interfaces/exchange_interface.py` - Base interface implementation
- `blankly/exchanges/interfaces/{exchange_name}/` - Per-exchange implementations

### Strategy Framework (Event-Driven Trading)

Strategies execute callbacks in response to events (price updates, time triggers, websocket data).

**Event Types**:
- `price_event` - Periodic price checks (uses REST API)
- `bar_event` - OHLCV candlestick data
- `tick_event` - Real-time websocket price updates
- `orderbook_event` - Real-time orderbook updates
- `scheduled_event` - Time-based callbacks (no symbol)
- `arbitrage_event` - Multi-symbol price events

**Key Files**:
- `blankly/frameworks/strategy/strategy.py` - Main Strategy class
- `blankly/frameworks/strategy/strategy_state.py` - State passed to callbacks
- `blankly/frameworks/strategy/futures_strategy.py` - Futures variant

**Usage Pattern**:
```python
strategy = blankly.Strategy(exchange)
strategy.add_price_event(callback, symbol='BTC-USD', resolution='1d', init=init)
strategy.backtest(to='1y', initial_values={'USD': 10000})  # Backtesting
# strategy.start()  # Live trading
```

### Model Framework (Base Abstraction)

Abstract base class for backtestable trading systems. Strategies inherit from this.

**Key Files**:
- `blankly/frameworks/model/model.py`

**Lifecycle**:
1. `__init__` - Setup exchange connection
2. `main()` - User implements trading logic (abstract method)
3. `backtest()` / `run()` - Execute in backtest or live mode
4. `teardown()` - Cleanup

**Exchange Swapping**: Automatically swaps to paper trade for backtesting:
- `Exchange` → `PaperTrade`
- `FuturesExchange` → `FuturesPaperTrade`

### Screener Framework (Batch Symbol Processing)

For iterating through many symbols periodically, not continuous trading.

**Key Files**:
- `blankly/frameworks/screener/screener.py`
- `blankly/frameworks/screener/screener_state.py`

**Lifecycle**:
1. `init(state)` - Setup before screening
2. `evaluator(symbol, state)` - Classify each symbol
3. `formatter(results, state)` - Format output
4. `teardown(state)` - Cleanup

### Backtesting Engine

**Architecture**:
- `PaperTrade(Exchange)` wraps real exchange
- `PaperTradeInterface` wraps real interface, simulates orders
- `BackTestController` manages:
  - Price data loading and caching
  - Time simulation via `time` property
  - Event queue (sorted by time)
  - Account valuation snapshots
  - Results generation with metrics

**Key Files**:
- `blankly/exchanges/interfaces/paper_trade/paper_trade.py`
- `blankly/exchanges/interfaces/paper_trade/paper_trade_interface.py`
- `blankly/exchanges/interfaces/paper_trade/backtest_controller.py`

**Live vs Backtest Differences**:
- Time: `time.time()` → `BackTestController.time`
- Price: REST API / Websocket → CSV cache / DataReader
- Orders: Exchange execution → Simulated at bid/ask
- Sleep: `time.sleep()` → Advance backtest time

See `blankly/BACKTESTING_ENGINEERING.md` for detailed engineering considerations:
- Order filter validation (min/max size, price increments)
- Exchange-specific data (prices vary between exchanges)
- Fee accuracy (uses user's actual fee tier)
- Limit order simulation
- Short selling & margin
- Market hours (for stocks)

### Websocket Managers

Centralized management of websocket connections with callback system.

**Key Files**:
- `blankly/exchanges/managers/ticker_manager.py` - Price tick websockets
- `blankly/exchanges/managers/orderbook_manager.py` - Orderbook websockets
- `blankly/exchanges/abc_exchange_websocket.py` - Base websocket class

**Pattern**:
- `TickerManager` / `OrderbookManager` create exchange-specific websockets
- Multiple callbacks can subscribe to same feed
- Automatic lifecycle management (start, stop, restart)
- Symbol normalization per exchange

### Futures vs Spot Trading

Parallel hierarchies with shared patterns:

**Spot**: `Exchange` → `ExchangeInterface` → `Strategy` → `StrategyState`

**Futures**: `FuturesExchange` → `FuturesExchangeInterface` → `FuturesStrategy` → `FuturesStrategyState`

**Futures-Specific Features**:
- Position management: `get_position()`, `get_positions()`
- Leverage: `set_leverage()`, `get_leverage()`
- Margin type: `set_margin_type()` (CROSSED/ISOLATED)
- Hedge mode: `set_hedge_mode()` (ONE_WAY/HEDGE)
- Funding rates: `get_funding_rate()`, `get_funding_rate_history()`

**Key Files**:
- `blankly/exchanges/futures/futures_exchange.py`
- `blankly/exchanges/interfaces/futures_exchange_interface.py`
- `blankly/exchanges/interfaces/binance_futures/binance_futures_interface.py`

## Directory Structure

```
blankly/                           # Main package (187+ Python files)
├── __init__.py                    # Package exports (Exchange classes, Strategy, Model, etc.)
├── enums.py                       # Enums (Side, OrderType, OrderStatus, TimeInForce)
├── BACKTESTING_ENGINEERING.md     # Detailed backtesting design documentation
├── PENDING.md                     # Development status notes
│
├── exchanges/                     # Exchange abstraction layer
│   ├── exchange.py                # Base Exchange class for spot trading
│   ├── abc_exchange.py            # Abstract exchange base
│   ├── abc_base_exchange.py       # Root abstract class
│   ├── strategy_logger.py         # Trade logging
│   ├── interfaces/                # Per-exchange implementations
│   │   ├── abc_exchange_interface.py        # Interface contract
│   │   ├── exchange_interface.py            # Base implementation
│   │   ├── futures_exchange_interface.py    # Futures interface base
│   │   ├── coinbase_pro/          # Coinbase Pro implementation
│   │   ├── binance/               # Binance spot trading
│   │   ├── binance_futures/       # Binance futures
│   │   ├── alpaca/                # Alpaca stocks
│   │   ├── ftx/                   # FTX (deprecated)
│   │   ├── ftx_futures/           # FTX futures (deprecated)
│   │   ├── kucoin/                # KuCoin
│   │   ├── okx/                   # OKX
│   │   ├── oanda/                 # OANDA forex
│   │   ├── paper_trade/           # Backtesting implementation
│   │   │   ├── paper_trade.py
│   │   │   ├── paper_trade_interface.py
│   │   │   └── backtest_controller.py
│   │   └── keyless/               # Backtesting without API keys
│   ├── managers/                  # Real-time data managers
│   │   ├── ticker_manager.py      # Price tick websockets
│   │   ├── orderbook_manager.py   # Orderbook websockets
│   │   └── general_stream_manager.py
│   ├── futures/                   # Futures-specific base classes
│   │   ├── futures_exchange.py
│   │   └── futures_strategy_logger.py
│   ├── auth/                      # Authentication utilities
│   │   ├── auth_constructor.py
│   │   └── utils.py
│   └── orders/                    # Order management utilities
│
├── frameworks/                    # High-level trading frameworks
│   ├── strategy/                  # Event-driven strategy framework
│   │   ├── strategy.py            # Main Strategy class
│   │   ├── strategy_base.py       # Base functionality
│   │   ├── strategy_state.py      # State passed to callbacks
│   │   ├── futures_strategy.py    # Futures variant
│   │   └── futures_strategy_state.py
│   ├── model/                     # Abstract model base
│   │   └── model.py
│   ├── screener/                  # Symbol screening framework
│   │   ├── screener.py
│   │   └── screener_state.py
│   └── multiprocessing/           # Multi-core execution
│       └── blankly_bot.py
│
├── indicators/                    # Technical indicators
│   ├── moving_averages.py         # SMA, EMA, WMA, HMA
│   ├── oscillators.py             # RSI, MACD, Stochastic, ADX
│   ├── statistics.py              # Volatility, correlation, beta
│   ├── indicators.py              # Additional indicators
│   └── utils.py
│
├── metrics/                       # Portfolio metrics
│   └── portfolio.py               # Sharpe, Sortino, CAGR, max drawdown
│
├── utils/                         # Utilities
│   ├── time.py                    # Time conversion utilities
│   ├── scheduler.py               # Event scheduling (cron-like)
│   ├── time_builder.py            # Time parsing
│   ├── utils.py                   # Misc helpers (trunc, etc.)
│   └── exceptions.py              # Custom exceptions
│
├── deployment/                    # CLI and deployment tools
│   ├── new_cli.py                 # Main CLI entry point (blankly command)
│   ├── cli.py                     # Legacy CLI (blankly_old)
│   ├── deploy.py                  # Deployment logic
│   ├── api.py                     # Platform API client
│   ├── login.py                   # Authentication
│   ├── keys.py                    # API key management
│   ├── ui.py                      # CLI UI helpers
│   └── exchange_data.py           # Exchange metadata
│
├── data/                          # Data utilities
│   ├── data_reader.py             # Historical data loading
│   └── templates/                 # Project templates
│       ├── rsi_bot.py
│       ├── rsi_screener.py
│       ├── none.py
│       └── keyless.py
│
└── futures/                       # Futures utilities
    └── utils.py

tests/                             # Test suite
├── __init__.py
├── test_auth_constructor.py
├── testing_utils.py
├── exchanges/                     # Exchange tests
│   ├── test_interface_homogeneity.py
│   └── interfaces/                # Per-exchange tests
│       ├── binance/
│       ├── coinbase_pro/
│       └── ...
├── strategy/                      # Strategy framework tests
├── indicators/                    # Indicator tests
├── metrics/                       # Metrics tests
├── interface/                     # Interface tests
├── helpers/                       # Test helpers
├── websockets/                    # Websocket tests
└── config/                        # Test configuration
    └── keys.json                  # Test API keys (gitignored)

examples/                          # Complete strategy examples
├── rsi.py                         # RSI strategy
├── golden_cross.py                # Moving average crossover
├── macd.py                        # MACD strategy
├── futures_rsi.py                 # Futures RSI strategy
├── futures.py                     # Basic futures example
├── rsi_screener.py                # Screener example
├── keyless_backtest.py            # Backtesting without API keys
├── custom_model.py                # Custom Model implementation
├── take_profit.py                 # Take profit orders
├── leveragedSPY.py                # Leveraged trading example
├── multicore_bot.py               # Multi-core execution
├── mlp_model.py                   # Machine learning model
├── settings.json                  # Example settings
├── backtest.json                  # Example backtest config
└── keys_example.json              # Example API keys format

Root files:
├── setup.py                       # Package configuration
├── setup.cfg                      # Build configuration (yapf settings)
├── pytest.ini                     # Pytest configuration
├── README.md                      # Project documentation
├── CONTRIBUTING.md                # Contribution guidelines
├── CODE_OF_CONDUCT.md             # Code of conduct
├── LICENSE                        # LGPL-3.0 license
└── .gitignore                     # Git ignore rules
```

## Key Design Patterns

1. **Abstract Factory**: `Exchange.construct_interface_and_cache()` creates exchange-specific interfaces
2. **Strategy Pattern**: Different event types with same callback signature
3. **Template Method**: `Model.main()` called by `run()` and `backtest()`
4. **Decorator Pattern**: `PaperTradeInterface` wraps real interface for simulation
5. **Manager Pattern**: Centralized websocket/ticker connection management
6. **State Pattern**: `StrategyState` encapsulates callback context
7. **Observer Pattern**: Websocket callbacks with multiple subscribers
8. **Facade Pattern**: Interface layer simplifies raw exchange APIs

## Adding New Exchanges

To add a new exchange, implement:

1. Create directory: `blankly/exchanges/interfaces/{exchange_name}/`
2. Implement files:
   - `{exchange}_api.py` - Raw REST API wrapper
   - `{exchange}_interface.py` - Extend `ExchangeInterface`, implement abstract methods
   - `{exchange}_websocket.py` - Extend `ABCExchangeWebsocket`
   - `{exchange}.py` - Extend `Exchange`, implement `construct_interface_and_cache()`
3. Add to `blankly/__init__.py` imports
4. Create tests in `tests/exchanges/interfaces/{exchange_name}/`

**Interface Methods to Implement**:
- Order operations: `market_order()`, `limit_order()`, `cancel_order()`
- Queries: `get_account()`, `get_products()`, `get_order()`, `get_open_orders()`
- Data: `get_price()`, `get_product_history()`
- Properties: `account`, `orders`, `cash`

## CLI Usage

```bash
# Initialize new project
blankly init

# Login to platform
blankly login

# Deploy model to platform
blankly deploy

# Add API keys interactively
blankly keys add

# Run local backtest
python your_strategy.py
```

## Python Version Support & Dependencies

**Supported Python Versions**:
- Python 3.7, 3.8, 3.9, 3.10
- Tests run on all supported versions in CI
- Current system: Python 3.13.5 (may have compatibility issues)

**Core Dependencies** (from `setup.py`):
```python
# Trading & Exchange APIs
alpaca-trade-api >= 1.4.2     # Stock trading (Alpaca)
python-binance >= 1.0.15       # Crypto trading (Binance)

# Data & Numerical Computing
numpy >= 1.21.4                # Numerical arrays and operations
pandas >= 1.1.5                # Data manipulation and time series
newnewtulipy >= 0.4.6.3        # Technical indicators (TA-Lib fork)
dateparser >= 1.1.0            # Date/time parsing

# Networking & Real-time Data
requests >= 2.26.0             # REST API calls
websocket-client >= 1.2.1      # WebSocket connections

# UI & CLI
questionary >= 1.10.0          # Interactive CLI prompts
yaspin >= 2.1.0                # Terminal loading spinners
bokeh >= 2.4.2                 # Interactive visualizations
```

**Development Dependencies**:
```bash
pytest                          # Test runner
pytest-mock                     # Mocking for tests
python3 -m build                # Build tool for distribution
twine                          # PyPI upload tool (maintainers)
yapf                           # Code formatter (PEP 8)
```

## Testing Conventions

- Test classes inherit from `unittest.TestCase`
- Test methods named `test_*`
- Use `pytest` runner (configured in `pytest.ini`)
- Place test API keys in `tests/config/keys.json`
- Mock external calls when possible

## Common Development Tasks

### Running a Single Test
```bash
pytest tests/test_auth_constructor.py::TestAuthConstructor::test_method_name -v
```

### Testing Against Live Exchange
Add your API keys to `tests/config/keys.json`:
```json
{
  "coinbase_pro": {
    "API_KEY": "...",
    "API_SECRET": "...",
    "API_PASS": "..."
  }
}
```

### Creating a New Strategy
```python
import blankly

def price_event(price, symbol, state: blankly.StrategyState):
    # Your logic here
    pass

def init(symbol, state: blankly.StrategyState):
    # Initialize state variables
    state.variables['history'] = state.interface.history(symbol, to=150)['close']

exchange = blankly.CoinbasePro()
strategy = blankly.Strategy(exchange)
strategy.add_price_event(price_event, symbol='BTC-USD', resolution='1d', init=init)

# Backtest
results = strategy.backtest(to='1y', initial_values={'USD': 10000})

# Or go live
# strategy.start()
```

### Using Indicators
```python
import blankly

# Access built-in indicators
rsi = blankly.indicators.rsi(prices)
sma = blankly.indicators.sma(prices, period=20)
macd = blankly.indicators.macd(prices)
```

## Important Implementation Notes

### State Management
- Use `state.variables` dictionary to persist data between callbacks
- `StrategyState` is passed to all strategy callbacks
- Access interface via `state.interface`
- Get symbol info via `state.symbol`, `state.base_asset`, `state.quote_asset`

### Time Handling
- In strategies, use `state.time` (not `time.time()`)
- Use `model.sleep(seconds)` (not `time.sleep()`)
- These automatically work in both live and backtesting

### Order Validation
- All orders validated against exchange filters (min/max size, price increments)
- Use `blankly.trunc(value, decimals)` to round to exchange precision
- Check `interface.get_products()` for trading rules

### Resolution Strings
Common resolution formats: `'1m'`, `'5m'`, `'15m'`, `'1h'`, `'1d'`

### Switching Live ↔ Backtest
```python
# Backtest
results = strategy.backtest(to='1y', initial_values={'USD': 10000})

# Live (comment out backtest, uncomment start)
# strategy.start()
```

## Package Management Notes

### Current State: Legacy Setup.py

This project uses the traditional `setup.py` approach from pre-2020 Python:

**Characteristics**:
- ✅ Simple and stable
- ✅ Compatible with all pip versions
- ❌ No dependency locking (can lead to version conflicts)
- ❌ Slower dependency resolution
- ❌ Manual dependency management
- ❌ No development dependency groups

**Dependency File**: `setup.py` line 32-44 contains all runtime dependencies

### Potential Migration Paths

If modernizing this project, consider:

#### Option 1: Migrate to pyproject.toml + setuptools

```toml
[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "blankly"
version = "1.18.11-beta"
dependencies = [
    "questionary>=1.10.0",
    "yaspin>=2.1.0",
    # ... rest of dependencies
]

[project.optional-dependencies]
dev = ["pytest", "pytest-mock", "yapf"]
```

#### Option 2: Migrate to UV (Fastest)

```bash
# Convert existing setup.py to pyproject.toml
uv init --lib

# Install dependencies with lockfile
uv sync

# This would create:
# - pyproject.toml
# - uv.lock (exact dependency versions)
```

**UV Benefits**:
- 10-100x faster than pip
- Automatic lockfile generation
- Better dependency resolution
- Native support for dev dependencies

#### Option 3: Migrate to Poetry

```bash
poetry init
poetry install
```

**Poetry Benefits**:
- Comprehensive project management
- Integrated virtual environments
- Dependency groups (dev, test, docs)
- Lock file for reproducibility

### Current Recommendation

For contributors: Use the existing `setup.py` approach to maintain compatibility. If the maintainers decide to modernize, UV would provide the fastest development experience with minimal migration effort.

## Contributing

See `CONTRIBUTING.md` for contribution guidelines. Key points:
- Fork and clone the repository
- Install from source with `pip install -e .`
- Add tests for new features
- Run `pytest` before submitting PR
- Sign the CLA (required)

## Additional Resources

- **Backtesting Details**: See `blankly/BACKTESTING_ENGINEERING.md` for engineering considerations
- **Examples**: Check `examples/` directory for complete strategy examples
- **Documentation**: https://docs.blankly.finance
- **Discord**: Community support available
- **GitHub**: https://github.com/Blankly-Finance/Blankly
- **PyPI**: https://pypi.org/project/blankly/
