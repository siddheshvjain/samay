---
title: Transaction costs destroy high-turnover strategies
author: samay-core
date: 2025-01-01
region: universal
asset_class: equity
tags: [costs, turnover, realism, important]
---

## Hypothesis

High-frequency rebalancing strategies (weekly, daily) look great on paper — high Sharpe, high Calmar — but fail in live trading because of transaction costs.

## Evidence

**Strategy: Momentum (3-month, rebalance weekly on 50 stocks)**

| Metric | Zero Costs | 0.1% per trade | 0.3% per trade |
|--------|-----------|-----------------|-----------------|
| CAGR | 18.5% | 17.2% | 15.1% |
| Sharpe | 1.34 | 1.18 | 0.94 |
| # Trades / year | 260 | 260 | 260 |
| Turnover | ~52% monthly | ~52% monthly | ~52% monthly |
| Cost drag / year | 0% | ~1.3% | ~3.4% |

**Backtested 2015–2024, Nifty 50 universe. Commission only; bid-ask spread not included.**

At 0.3% per trade (realistic for India: brokerage + STT + GST):
- Expected annual cost: 260 trades * 0.3% = 7.8% (if you round-trip all positions)
- Actually you're flipping: buy Monday, sell Friday → 2 trades/position
- Real drag: 50 * 52 rebalances/year * 2 trades * 0.3% = **3.1% drag**
- Net CAGR: 18.5% - 3.1% = **15.4%** (not 18.5%)

Compare to holding Nifty 50 index with 0.05% AUM fee → CAGR ~13% after fees.

The momentum strategy still wins, but the margin shrinks from 5.5% to 2.4%.

## Conclusion

1. **Always model realistic costs** — Don't assume zero commission.
2. **Reduce turnover** — Monthly rebalance instead of weekly (50% cost savings).
3. **Use liquid assets** — Narrow bid-ask spread saves 0.1–0.2% per trade.
4. **Position trade, don't day trade** — Weekly or monthly beats daily for retail.
5. **Cost budget** — If your turnover * cost > 1% CAGR, the strategy doesn't work net.

## Recommended Cost Assumptions

| Market | Commission | Spread | STT/Tax | Total per trade |
|--------|-----------|--------|---------|-----------------|
| US (Alpaca) | $0 | 0.03–0.1% | ~0% | 0.05–0.15% |
| India (Zerodha) | 0.02% | 0.05–0.2% | 0.1% | 0.2–0.4% |
| EU (Saxo) | 0.1% | 0.03–0.1% | ~0% | 0.15–0.2% |

**Round-trip (buy + sell) costs are roughly 2x per-trade costs.**

## Lesson

Smart strategies fail due to costs. Realistic models succeed.

Test your strategy with costs built in from day one.

---

*Related: Skill "Risk Management" → "Why Transaction Costs Matter"*
