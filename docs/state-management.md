# Blankly -- State Management

## Strategy State Machine

```mermaid
stateDiagram-v2
    [*] --> Initialized: Strategy(exchange)
    Initialized --> EventsRegistered: add_price_event() / add_bar_event()
    
    EventsRegistered --> Backtesting: backtest()
    EventsRegistered --> LiveTrading: start()
    
    state Backtesting {
        [*] --> PaperTradeWrapped
        PaperTradeWrapped --> DataLoading
        DataLoading --> TimeSimulation
        TimeSimulation --> EventDispatch
        EventDispatch --> CallbackExecution
        CallbackExecution --> OrderSimulation
        OrderSimulation --> PortfolioUpdate
        PortfolioUpdate --> TimeSimulation: Next time step
        PortfolioUpdate --> ResultGeneration: End of data
    }
    
    state LiveTrading {
        [*] --> ExchangeConnected
        ExchangeConnected --> WebSocketOpen
        WebSocketOpen --> EventListening
        EventListening --> CallbackTriggered
        CallbackTriggered --> OrderSubmitted
        OrderSubmitted --> EventListening: Continue
    }
    
    Backtesting --> Completed: BacktestResult returned
    LiveTrading --> Stopped: stop()
    Completed --> [*]
    Stopped --> [*]
```

## StrategyState Lifecycle

The `StrategyState` object is passed to every strategy callback, providing access to:

| Property | Type | Description |
|----------|------|-------------|
| `variables` | `dict` | Persistent state between callbacks |
| `interface` | `ABCExchangeInterface` | Trading operations |
| `symbol` | `str` | Current symbol |
| `base_asset` | `str` | Base currency (e.g., BTC) |
| `quote_asset` | `str` | Quote currency (e.g., USD) |
| `time` | `float` | Current time (works in both live and backtest) |
| `resolution` | `int` | Event resolution in seconds |

## Model Lifecycle

```mermaid
stateDiagram-v2
    [*] --> Created: Model(exchange)
    Created --> Running: run(args)
    Created --> BacktestMode: backtest(args)
    
    state BacktestMode {
        [*] --> ExchangeSwapped: Exchange -> PaperTrade
        ExchangeSwapped --> MainExecuting: main() called
        MainExecuting --> ExchangeRestored: Backtest complete
        ExchangeRestored --> [*]
    }
    
    state Running {
        [*] --> ThreadStarted
        ThreadStarted --> MainExecuting2: main() called
        MainExecuting2 --> [*]: Thread exits
    }
    
    BacktestMode --> ResultReturned
    Running --> Teardown: teardown()
    ResultReturned --> [*]
    Teardown --> [*]
```

## Order State Machine

```mermaid
stateDiagram-v2
    [*] --> Pending: Submit order
    Pending --> Open: Exchange accepts
    Open --> PartiallyFilled: Partial execution
    PartiallyFilled --> Filled: Complete execution
    Open --> Filled: Full execution
    Open --> Cancelled: cancel_order()
    PartiallyFilled --> Cancelled: cancel_order()
    Pending --> Rejected: Validation fails
    Filled --> [*]
    Cancelled --> [*]
    Rejected --> [*]
```

## BackTestController State

The BackTestController manages simulated time and portfolio state:

```mermaid
stateDiagram-v2
    [*] --> Idle: Controller created
    Idle --> Configured: Set initial values, date range
    Configured --> DataLoaded: Load historical prices
    DataLoaded --> Running: Start simulation
    
    state Running {
        [*] --> ProcessEvent
        ProcessEvent --> EvaluateOrders: Check pending orders
        EvaluateOrders --> SnapshotPortfolio: Record values
        SnapshotPortfolio --> AdvanceTime: Move to next event
        AdvanceTime --> ProcessEvent: More events
        AdvanceTime --> Complete: No more events
    }
    
    Running --> ResultsGenerated: Compute metrics
    ResultsGenerated --> [*]
```

## Time Management

Blankly handles time differently in live vs backtest mode:

| Operation | Live Mode | Backtest Mode |
|-----------|-----------|---------------|
| Current time | `time.time()` | `BackTestController.time` |
| Sleep | `time.sleep(n)` | Advance simulated time by n |
| State access | `state.time` | `state.time` (unified) |

Users should always use `state.time` and `model.sleep()` to ensure code works in both modes.

## WebSocket Connection State

```mermaid
stateDiagram-v2
    [*] --> Disconnected
    Disconnected --> Connecting: open()
    Connecting --> Connected: WebSocket established
    Connected --> Streaming: Subscribed to feeds
    Streaming --> Reconnecting: Connection lost
    Reconnecting --> Connected: Reconnect successful
    Streaming --> Disconnected: close()
    Reconnecting --> Disconnected: Max retries exceeded
    Disconnected --> [*]
```

---
## See Also
- [README](README.md) — Project overview and quick start
- [Architecture](architecture.md) — System design and components
- [Workflow](workflow.md) — Event flows and processing pipelines
- [Development](development.md) — Development guide and best practices
