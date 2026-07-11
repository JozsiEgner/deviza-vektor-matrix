# Trading framework integrations

This repository now includes reference adapters for:

- PyBroker
- LumiBot
- NautilusTrader
- QuantConnect LEAN

These adapters use the Deviza-Vektor Matrix as a **risk and anomaly gate**. They do not claim to predict guaranteed returns and should not be connected directly to live order blocking without validation.

## Common decision mapping

- `ALLOW` -> full configured position size
- `REVIEW` -> reduced position size, default multiplier `0.25`
- `BLOCK` -> no new risk, default multiplier `0.0`

## Required inputs

Each adapter needs:

- symbol
- normalized fundamental vector
- current price
- previous price
- observation interval
- target or equilibrium price
- optional threshold configuration

## PyBroker

Use `integrations.pybroker_adapter.py` from an execution function. The adapter returns a position multiplier and DVM metadata.

## LumiBot

Use `integrations.lumibot_adapter.py` inside `on_trading_iteration()`. The adapter can stop a new order or scale its size.

## NautilusTrader

Use `integrations.nautilus_adapter.py` before order submission. The adapter produces `block_order`, `reduce_only` and `size_multiplier` fields.

## QuantConnect LEAN

LEAN is primarily C#. Use `integrations.lean_bridge.py` as a JSON process or HTTP bridge. The bridge accepts a JSON snapshot and returns the DVM decision.

## Production requirements

Before live deployment:

1. backtest on out-of-sample data;
2. measure false positives and false negatives;
3. version every model configuration and data source;
4. log all decisions and reasons;
5. deploy in shadow mode;
6. use manual review for `REVIEW` and `BLOCK` states;
7. set independent position and loss limits;
8. include a fail-open or fail-safe policy for missing data.

## External repositories

The adapters are maintained here because this account does not have write permission to the upstream repositories. A maintainer can later open a focused pull request after each adapter is validated against the relevant framework version.
