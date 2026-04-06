# Blankly -- Workflow

## Strategy Execution Flow

```mermaid
sequenceDiagram
    participant U as User Code
    participant S as Strategy
    participant E as Exchange
    participant I as Interface
    participant BTC as BackTestController

    U->>S: add_price_event(callback, symbol, resolution)
    U->>S: backtest(to='1y', initial_values)

    Note over S,BTC: Backtesting Mode
    S->>E: Wrap with PaperTrade
    S->>BTC: Initialize time simulation
    BTC->>I: Load historical data
    
    loop For each time step
        BTC->>BTC: Advance simulated time
        BTC->>S: Trigger scheduled events
        S->>U: callback(price, symbol, state)
        U->>I: market_order() / limit_order()
        I->>BTC: Simulate execution
        BTC->>BTC: Update portfolio values
    end
    
    BTC->>U: Return BacktestResult
```

## Live Trading Flow

```mermaid
sequenceDiagram
    participant U as User Code
    participant S as Strategy
    participant E as Exchange
    participant WS as WebSocket
    participant API as Exchange API

    U->>S: add_price_event(callback, symbol, resolution)
    U->>S: start()

    S->>E: Connect to exchange
    E->>WS: Open WebSocket connection
    E->>API: Authenticate

    loop Continuous trading
        alt Price Event (REST polling)
            S->>API: GET /history (at resolution interval)
            API-->>S: Price data
            S->>U: callback(price, symbol, state)
        else Tick Event (WebSocket)
            WS-->>S: Real-time price update
            S->>U: callback(tick, symbol, state)
        else Orderbook Event (WebSocket)
            WS-->>S: Orderbook update
            S->>U: callback(orderbook, symbol, state)
        else Scheduled Event (cron)
            S->>U: callback(state)
        end
        U->>API: Submit orders
    end
```

## Strategy Event Types

| Event Type | Data Source | Trigger | Use Case |
|-----------|------------|---------|----------|
| `price_event` | REST API | Periodic polling | Simple strategies, daily/hourly |
| `bar_event` | REST API | OHLCV bar close | Candlestick-based strategies |
| `tick_event` | WebSocket | Real-time price | Scalping, HFT |
| `orderbook_event` | WebSocket | Orderbook change | Market making |
| `scheduled_event` | Timer | Cron schedule | Portfolio rebalancing |
| `arbitrage_event` | REST/WS | Multi-symbol | Cross-pair arbitrage |

## Screener Workflow

```mermaid
sequenceDiagram
    participant U as User Code
    participant SC as Screener
    participant I as Interface

    U->>SC: Screener(exchange, evaluator, symbols)
    SC->>SC: init(state) - setup

    loop For each screening cycle
        loop For each symbol
            SC->>I: Get price / history
            SC->>U: evaluator(symbol, state)
            U-->>SC: Classification result
        end
        SC->>U: formatter(results, state)
    end

    SC->>SC: teardown(state) - cleanup
```

## Backtest Data Flow

```mermaid
graph LR
    subgraph "Data Sources"
        CSV[CSV Cache]
        DR[DataReader]
        API[Exchange API]
    end

    subgraph "BackTestController"
        EQ[Event Queue]
        TS[Time Simulator]
        PV[Portfolio Valuator]
    end

    subgraph "Results"
        BR[BacktestResult]
        MT[Metrics]
        CH[Charts]
    end

    CSV --> DR
    API --> DR
    DR --> EQ
    EQ --> TS
    TS --> PV
    PV --> BR
    BR --> MT
    BR --> CH
```

## Order Execution Flow

```mermaid
sequenceDiagram
    participant U as User Code
    participant I as Interface
    participant V as Validator
    participant E as Exchange API

    U->>I: market_order(symbol, side, size)
    I->>V: Validate against exchange filters
    V->>V: Check min/max size
    V->>V: Check price increments
    V->>V: Check account balance
    
    alt Validation passes
        I->>E: Submit order
        E-->>I: Order confirmation
        I-->>U: Order result
    else Validation fails
        V-->>U: Raise InvalidOrder
    end
```

---
## See Also
- [README](README.md) — Project overview and quick start
- [Architecture](architecture.md) — System design and components
- [State Management](state-management.md) — State lifecycle and data models
- [Development](development.md) — Development guide and best practices
