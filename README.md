<div align="center">

# samay

### Find alpha. Together.

**Open-source quant research that anyone can use — even without writing code.**

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/)
[![Status](https://img.shields.io/badge/status-alpha-orange.svg)](ROADMAP.md)
[![Vision](https://img.shields.io/badge/read-VISION-purple.svg)](VISION.md)

</div>

---

## What is samay? (no jargon)

Imagine you have a hunch about the stock market — *"buying companies that went up last quarter probably keeps working"* — but no way to test it without spending months learning Python, statistics, and finance.

**samay lets you test that hunch in 30 seconds.**

You describe your idea in plain English. samay's AI writes the code, runs it against 10 years of real market history, and shows you whether it would have made money — including the boring-but-critical stuff like trading fees and bad fills that destroy most "winning" strategies on paper.

Everything is open source. Every strategy on samay has been independently verified by automated tests. Strategies that **lost** money are kept too — because you learn more from failure than from success.

---

## Why does this exist?

| | |
|---|---|
| **Hedge funds** spend $25,000+/year per analyst on Bloomberg terminals to do quantitative research. | |
| **Retail traders** get Reddit tips and "hot stocks" newsletters. | |
| **The data is the same.** What differs is the infrastructure, the institutional knowledge, and the discipline of honest backtesting. | |

samay closes that gap. We give you the infrastructure (free), the knowledge (open library of "skills"), and the discipline (every result is auto-verified — no fake numbers).

> **Read the full vision →** [VISION.md](VISION.md)

---

## Two paths in

### 🪙 If you don't code

```bash
pip install samay
samay leaderboard
```

That gives you the top community-verified strategies, ranked by risk-adjusted return. Pick one, look at how it performed, and (in v0.2) connect a paper-trading account to follow it without risking real money.

You can also use samay through **Claude Desktop**. After a 30-second config, you can ask Claude things like:

> *"Find me a low-drawdown momentum strategy for the Indian market."*

Claude will run real backtests against samay and show you the results — no terminal commands needed. See [examples/claude_desktop_config.json](examples/claude_desktop_config.json).

### 💻 If you code

```bash
git clone https://github.com/siddheshvjain/samay.git
cd samay
pip install -e ".[dev]"

# Generate a strategy from English
samay research "momentum strategy for Nifty 50, weekly rebalance, 2018-2023"

# Backtest an existing one
samay backtest examples/momentum.py --tickers SPY --from 2018-01-01 --to 2023-12-31

# Browse the community registry
samay leaderboard

# Contribute one
samay publish my-strategy.py
```

For optional 20–40× speedup, install the C++ fast path: `pip install -e ".[cpp]"`.

---

## What's inside

```
🎯  AI Agent          → Describe a strategy in English, get production code
📊  Backtest Engine   → Python + optional C++ fast path (20–40× faster)
🌍  Strategy Registry → Community-verified strategies (CI auto-checks every PR)
🧠  Skills Library    → Open knowledge: momentum, mean-reversion, value, risk, India-specific
🪦  Graveyard         → Failed strategies with explanations of why they failed
💰  Broker Adapters   → Paper-trade via Alpaca (US), Zerodha (India), IBKR (global)
🔌  MCP Server        → Use samay from inside Claude Desktop
```

**Architecture in one image:**

```
┌─────────────────────────────────────────────────────────┐
│  INTERFACES   CLI · Dashboard · Claude Desktop (MCP)    │
├─────────────────────────────────────────────────────────┤
│  AI AGENT     Claude + skills → strategy code           │
├─────────────────────────────────────────────────────────┤
│  COMMUNITY    strategies/ · skills/ · lessons/ · 🪦     │
├─────────────────────────────────────────────────────────┤
│  BACKTEST     Python engine (+ optional C++ fast path)  │
├─────────────────────────────────────────────────────────┤
│  STRATEGY     One method: generate_signals(prices)      │
├─────────────────────────────────────────────────────────┤
│  DATA         yfinance · Alpaca · Zerodha · IBKR        │
└─────────────────────────────────────────────────────────┘
```

> **Full architecture deep-dive →** [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)

---

## Where it works today

| Region | Markets | Status |
|---|---|---|
| 🇺🇸 US | NYSE, NASDAQ, ETFs | ✅ Backtest ready |
| 🇮🇳 India | NSE, BSE | ✅ Backtest ready (Nifty top-10 strategy included) |
| 🌏 Global | Anything yfinance supports | ✅ Backtest ready |

Paper trading and live execution coming in v0.2 — see [ROADMAP.md](ROADMAP.md).

---

## Sample strategies (already in the registry)

| Strategy | Region | CAGR | Sharpe | Max DD |
|---|---|---|---|---|
| `momentum/nifty-top10` | 🇮🇳 India | 22.3% | 1.42 | -31.2% |
| `momentum/us-sector-rotation` | 🇺🇸 US | 11.4% | 0.98 | -28.6% |
| `trend-following/golden-cross-spy` | 🇺🇸 US | 9.1% | 0.72 | -22.4% |
| `mean-reversion/rsi-spy` | 🇺🇸 US | 16.8% | 0.94 | — |
| `mean-reversion/bollinger-bands-qqq` | 🇺🇸 US | 8.7% | 0.84 | -19.3% |

All numbers verified by CI on every commit. See [strategies/](strategies/).

---

## Glossary (for non-coders)

| Term | Plain English |
|---|---|
| **Backtest** | Replay your strategy against past market data to see how it would have performed. |
| **CAGR** | Compound Annual Growth Rate — the steady annual return that would explain your total gain. 10% CAGR means your money roughly doubles every 7 years. |
| **Sharpe ratio** | Return divided by volatility. Higher is better. Above 1.0 is decent; above 2.0 is exceptional (and probably overfit). |
| **Drawdown** | The biggest peak-to-trough loss your strategy ever had. -30% means at the worst point, you'd have lost 30% from your peak. |
| **Slippage** | The difference between the price you wanted and the price you got. Real trading always has slippage; ignoring it makes backtests lie. |
| **Paper trading** | Trading with fake money against real market prices. Lets you test a strategy live without risking capital. |
| **Momentum** | The tendency for things going up to keep going up (and vice versa). Works in trending markets, fails in choppy ones. |
| **Mean reversion** | The opposite — things that went down recently tend to bounce back. Works in range-bound markets. |
| **Survivorship bias** | The trap of only looking at companies that still exist today. If you backtest "buy the S&P 500" using today's S&P 500, you've cheated — Lehman isn't in the list anymore. |
| **Lookahead bias** | Accidentally using information from the future in your backtest. samay's 1-bar execution lag prevents this automatically. |

---

## Project status

**v0.1** (now) — Backtest engine, AI strategy generator, MCP server, community registry, knowledge commons.
**v0.2** — Streamlit dashboard, paper trading via Alpaca/Zerodha, more strategies.
**v0.3** — Live trading bridges, multi-asset (futures, FX, crypto), portfolio-level backtesting.
**v1.0** — Stable API, 100+ verified strategies, comprehensive skill library.

> **Full roadmap →** [ROADMAP.md](ROADMAP.md)

---

## Contributing

Strategies, skills, lessons, graveyard entries, code, docs — all welcome. Failed strategies are *especially* welcome.

> **How to contribute →** [CONTRIBUTING.md](CONTRIBUTING.md)

---

## Disclaimer

samay is **research infrastructure, not financial advice**. Past performance doesn't predict future returns. Backtested results are theoretical and ignore many real-world frictions (taxes, market impact, broker outages, your own emotions). Never trade money you can't afford to lose.

---

## License

[Apache 2.0](LICENSE) — use it commercially, modify it, do whatever you want. Just don't claim you wrote it.

---

<div align="center">

**samay** *(समय)* — Sanskrit for *time, season, opportunity*.

In markets, time is everything. We think the time is now.

</div>
