# samay — Architecture

This doc explains *what lives where* and *why*. It's written for two audiences:
1. A new contributor trying to find the right file to edit.
2. A non-coder who wants to understand how the pieces fit.

---

## The 30-second version

samay has **6 layers**, stacked from raw data at the bottom to user-facing interfaces at the top:

```
┌─────────────────────────────────────────────────────────┐
│  6. INTERFACES   CLI · Dashboard · MCP server           │  ← how you talk to samay
├─────────────────────────────────────────────────────────┤
│  5. AI AGENT     Claude + skills → strategy code        │  ← turns English into code
├─────────────────────────────────────────────────────────┤
│  4. COMMUNITY    strategies/ · skills/ · lessons/       │  ← the open knowledge commons
│                  graveyard/                              │
├─────────────────────────────────────────────────────────┤
│  3. BACKTEST     Python engine + C++ fast path          │  ← simulates trades over history
├─────────────────────────────────────────────────────────┤
│  2. STRATEGY     Strategy ABC + your subclass           │  ← the rules (when to buy/sell)
├─────────────────────────────────────────────────────────┤
│  1. DATA         yfinance · Alpaca · Zerodha · IBKR     │  ← prices, volumes, fundamentals
└─────────────────────────────────────────────────────────┘
```

Each layer only talks to the one below it. This means you can swap any layer (e.g., replace yfinance with a paid data feed) without breaking the rest.

---

## Layer 1 — Data

**Where:** `samay/data/`

**Files:**
- `base.py` — the abstract `DataProvider` (every data source must implement `get_ohlcv(ticker, start, end)`).
- `yfinance_provider.py` — wraps yfinance, caches to SQLite at `~/.samay/cache.db` with a 1-hour TTL. This is the default.

**Why a cache?** yfinance throttles aggressive callers. Caching means a re-run of the same backtest hits the local SQLite, not the internet. Backtests run in seconds instead of minutes.

**Adding a new data source** (e.g., paid Polygon.io feed): subclass `DataProvider`, implement `get_ohlcv`, register it in `__init__.py`. Nothing else needs to change.

---

## Layer 2 — Strategy

**Where:** `samay/strategy/base.py`

**The contract** — every strategy is a Python class that inherits from `Strategy` and implements one method:

```python
def generate_signals(self, data: pd.DataFrame) -> pd.Series:
    # data: OHLCV with DatetimeIndex
    # return: Series of 1 (buy), -1 (sell), 0 (hold)
```

That's it. **The entire system is built around this one method.** Everything else — backtesting, paper trading, dashboards — just feeds data into `generate_signals` and consumes its output.

This minimalism is intentional. A junior dev can write their first strategy in 10 lines.

**Where strategies live:**
- `samay/strategy/generated/` — strategies the AI agent writes (gitignored except for `.gitkeep`)
- `strategies/` (top-level) — community-contributed strategies, CI-verified
- `examples/` — reference strategies users can copy

---

## Layer 3 — Backtest

**Where:** `samay/backtest/`

**Files:**
- `engine.py` — the simulator. Takes a `Strategy`, prices, dates, capital. Runs through history bar-by-bar, tracks cash + positions, applies commissions and slippage, returns a `BacktestResult`.
- `metrics.py` — computes Sharpe, Sortino, drawdown, win-rate, profit factor, Calmar.
- `report.py` — uses `rich` to print a beautiful terminal report (ASCII equity curve + colored metrics table).
- `engine_cpp.py` — optional C++ fast path. Falls back to pure Python if C++ extension not installed.

**The 1-bar lag rule:** if a strategy emits a buy signal on day D, the engine executes at the **open of day D+1**. This prevents a class of subtle backtest bugs called "lookahead bias" where you accidentally trade using prices you couldn't have known yet.

**C++ fast path** (`cpp/`):
- Same algorithm, written in C++ with `pybind11` bindings.
- 20–40× faster on large parameter sweeps.
- Activates automatically if installed (`pip install -e ".[cpp]"`).
- Pure Python users notice nothing — same API, same results.

---

## Layer 4 — Community Commons

**Where:** `strategies/`, `skills/`, `lessons/`, `graveyard/` (all top-level dirs)

This is **the most important part of samay** and the part that doesn't exist anywhere else.

| Directory | Purpose | Format |
|---|---|---|
| `strategies/` | Working strategies, organized by category (momentum, mean-reversion, etc.) | `strategy.py` + `metadata.json` + `results.json` (CI-generated) |
| `skills/` | Domain knowledge — *what is momentum? when does it work?* | `SKILL.md` per topic |
| `lessons/` | Insights gleaned from real backtests — *transaction costs eat 3% of momentum returns* | Markdown |
| `graveyard/` | **Failed** strategies, with explanation of why they broke | Markdown |

**Why the graveyard exists:** in academia and industry, failed strategies vanish. samay treats failure as a first-class artifact because it teaches more than success.

**Verification:** every PR that touches `strategies/` triggers `.github/workflows/verify_strategies.yml`, which:
1. Imports the strategy
2. Runs a backtest
3. Posts results as a PR comment
4. Auto-generates `results.json`

This means **every claim in the registry has been independently re-run by CI**. No fake numbers.

---

## Layer 5 — AI Agent

**Where:** `samay/agent.py`

The agent does one thing: turn an English description into a `Strategy` subclass.

**The flow:**
1. User says: *"Build a momentum strategy for Indian large caps"*
2. Agent's `_load_skills()` scans the description for keywords (`momentum`, `india`, etc.) and loads relevant `SKILL.md` files into the prompt.
3. Agent calls Claude (Sonnet 4.6) with: system prompt + relevant skills + user's description.
4. Claude returns Python code for a `Strategy` subclass.
5. Agent saves it to `samay/strategy/generated/{slug}_{timestamp}.py`.
6. Agent returns the loaded class, ready for the backtest engine.

**Why skills matter:** without them, Claude generates plausible-but-wrong code (e.g., a momentum strategy that uses 2-day lookback because it doesn't know that's too short). With skills, Claude has the same context a quant analyst would have on day one.

---

## Layer 6 — Interfaces

Three ways to drive samay:

### CLI (`samay/cli.py`)
Built with Typer + Rich. Commands:
- `samay research "..."` — AI generates + backtests a strategy
- `samay backtest path/to/strategy.py` — backtest an existing strategy
- `samay leaderboard` — top community strategies by Sharpe
- `samay pull <id>` / `samay publish <name>` — interact with the registry
- `samay paper` — paper trade (v0.2.0)
- `samay serve` — start the MCP server
- `samay report` — replay last backtest

### MCP Server (`samay/server.py`)
Built with `FastMCP`. Exposes 5 tools to Claude Desktop:
- `run_backtest`, `get_last_results`, `list_strategies`, `search_strategies`, `get_leaderboard`

This means **Claude Desktop becomes a research interface**. You can ask Claude to "compare momentum vs mean-reversion on Indian large caps" and it actually runs the backtests.

### Dashboard (planned, v0.2.0)
Streamlit app for non-coders. Browse strategies, view interactive charts, generate strategies via web form.

---

## Request flow walkthrough

What happens when you run:

```bash
samay research "momentum on Nifty 50"
```

1. **`samay/cli.py:research()`** — parses args, instantiates `Agent`.
2. **`samay/agent.py:Agent.generate_strategy()`** — loads `skills/momentum/SKILL.md` and `skills/india-specific/SKILL.md` (both keywords matched), builds prompt, calls Claude.
3. Claude returns Python code → saved to `samay/strategy/generated/momentum-on-nifty-50_20260504_120000.py`.
4. Agent imports the file, returns the `Strategy` subclass.
5. **`samay/backtest/engine.py:BacktestEngine.run()`** — fetches OHLCV via `samay/data/yfinance_provider.py` (cached), runs the simulation bar-by-bar.
6. **`samay/backtest/metrics.py`** — computes Sharpe, drawdown, etc.
7. **`samay/backtest/report.py:print_report()`** — renders the terminal output with `rich`.
8. Result saved to `~/.samay/last_result.json` for later replay.

Every layer above only depends on the layer below. Swap any one piece (different LLM? different data feed? different broker?) without touching the rest.

---

## File-tree cheat sheet

```
samay/
├── samay/                     ← the Python package
│   ├── data/                  ← Layer 1: data providers
│   ├── strategy/              ← Layer 2: Strategy ABC + AI-generated strategies
│   ├── backtest/              ← Layer 3: engine, metrics, report (+ C++ wrapper)
│   ├── brokers/               ← paper-trade adapters (Alpaca, Zerodha, IBKR)
│   ├── agent.py               ← Layer 5: Claude integration
│   ├── cli.py                 ← Layer 6: CLI entry point
│   └── server.py              ← Layer 6: MCP server
├── cpp/                       ← C++ fast-path source (Layer 3)
├── strategies/                ← Layer 4: community strategy registry
├── skills/                    ← Layer 4: knowledge commons
├── lessons/                   ← Layer 4: insights from real backtests
├── graveyard/                 ← Layer 4: documented failures
├── examples/                  ← reference strategies + Claude Desktop config
├── tests/                     ← pytest suite
├── .github/workflows/         ← CI (lint+test) and CI (verify community strategies)
├── docs/ARCHITECTURE.md       ← this file
├── VISION.md                  ← the why
├── README.md                  ← the what
├── ROADMAP.md                 ← the when
└── CONTRIBUTING.md            ← the how
```

---

## Design principles

These show up everywhere in the codebase. If you're contributing, hold to them:

1. **One method, many strategies.** Adding new strategy types must not require changing the engine.
2. **Pure Python first, C++ optional.** The reference implementation must always work without compilation.
3. **Verifiable claims.** Every result.json comes from CI re-running the backtest. No human-edited metrics.
4. **Local-first.** Nothing leaves your machine unless you explicitly publish.
5. **Skills, not prompts.** Domain knowledge lives in `skills/` so anyone can audit and improve it — not buried inside `agent.py`.
