---
name: risk-management
description: Use this skill for position sizing, Kelly Criterion, max drawdown limits, correlation, and risk controls
tags: [risk, position-sizing, kelly-criterion, max-drawdown, correlation]
contributed_by: samay-core
---

# Risk Management

## Position Sizing Fundamentals

You can have a great strategy, but bad position sizing will blow your account.

**Fixed fractional** — Allocate the same % to each trade.
- Simple: if you have $100k, allocate $10k per position
- Risk: if positions are correlated, you can lose a lot fast

**Kelly Criterion** — Allocate based on the strategy's edge.
- Formula: f = (win% * avg_win - loss% * avg_loss) / avg_win
- Full Kelly is often too aggressive; use half-Kelly in practice
- Example: win% = 55%, avg_win = 2%, avg_loss = 1.5%
  - f = (0.55 * 2 - 0.45 * 1.5) / 2 = 0.28 (allocate 28% per trade)
  - Half-Kelly = 14% per trade (safer, lower volatility)

**Volatility-based** — Scale position size to asset volatility.
- Lower vol → larger position
- Higher vol → smaller position
- Dollar-neutral: each position has similar dollar-risk

## Max Drawdown Limits

Define your pain threshold before trading.

- **5% max drawdown** — Professional traders, hedge funds (very conservative)
- **10% max drawdown** — Serious retail traders (common benchmark)
- **20% max drawdown** — Aggressive traders (risk of ruin increases sharply)
- **> 20%** — Casino rules; you're over-leveraged

**Max consecutive losses** — Stop trading if you lose N trades in a row. Example: stop if 3 losses in a row.

**Max daily loss** — If you lose $X in a day, stop trading and reassess.

## Correlation Between Positions

You can be diversified in name but concentrated in risk.

**Example:**
- Own AAPL, MSFT, NVDA (3 different companies)
- All have beta > 1.0 to Nasdaq
- In a tech crash, all lose >20%
- You thought you were diversified; you weren't

**Solution:**
- Check correlation matrix of holdings
- Own stocks from different sectors (tech, finance, energy, healthcare)
- Or use a hedge: own some bonds, gold, or short an index

## Why Transaction Costs Matter

This is non-negotiable.

**US equities:**
- Commission: ~$0 (most brokers)
- Bid-ask spread: 0.01–0.1% depending on liquidity
- Market impact: 0.01–0.5% (larger orders move price)
- Slippage: roughly 0.05–0.1% per trade

**Indian equities (Zerodha):**
- Brokerage: flat ₹20 per trade (~0.02–0.05%)
- Securities Transaction Tax (STT): 0.1% on sells
- GST: 18% on brokerage
- Total: roughly 0.2–0.3% per trade (round trip ~0.5%)

**Impact on strategy:**
- Strategy with 50% annual return, 50% turnover = 200 trades/year
- At 0.1% commission: 200 * 0.001 = 2% drag
- Net return: 48%, not 50% — seems small but compounds
- At 0.3% commission: 6% drag → 44% net

**Rule of thumb:**
- Turnover * commission < 1% CAGR, or the strategy doesn't work

## Leverage & Margin

Leverage amplifies both gains and losses.

- **2x leverage** — Turn a 10% loss into 20%, a 10% gain into 20%
- **Margin call risk** — If your position drops 50%, the broker liquidates you (sells at the worst time)

**Avoid leverage unless:**
- You're a professional with risk controls
- You have deep capital reserves to meet margin calls
- You've stress-tested the strategy at 3x+ moves

## What to check in backtests

1. **Sharpe ratio** — Risk-adjusted return. Target > 1.0 (preferably > 1.5)

2. **Max drawdown** — The biggest peak-to-trough loss. Should be < 30% for most strategies.

3. **Calmar ratio** — CAGR / max drawdown. > 0.5 is solid.

4. **Sortino ratio** — Like Sharpe but only penalizes downside. > 1.0 is good.

5. **Rolling worst month** — Find the worst 1-month return ever. If it's < -20%, the strategy can blow up in a single month.

## See also

- Lesson: "Transaction costs destroy high-turnover strategies"
- All other skills — Apply position sizing to any strategy
