# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-01-01

### Added
- Core backtesting engine (Pandas-based, no zipline/backtrader)
- yfinance data provider with SQLite cache (1-hour TTL)
- AI strategy generation via Claude with skill-aware prompting
- Metrics: Sharpe, CAGR, Sortino, max drawdown, Calmar ratio, profit factor, win rate
- Rich terminal reporting with ASCII equity curves and color-coded metrics
- Broker adapters: Alpaca (paper), Zerodha, Interactive Brokers
- CLI: research, backtest, report, paper (stub), pull, publish, serve, leaderboard
- MCP server for Claude Desktop integration
- Community strategy registry with auto-verified CI
- Knowledge sharing: skills (momentum, mean-reversion, india-specific, risk-mgmt, value)
- Lessons: empirical discoveries backed by backtests
- Graveyard: honest failures and lessons learned
- GitHub Actions: CI testing + auto-verify strategy contributions
