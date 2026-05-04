# Roadmap

samay evolves in phases, each unlocking new capabilities.

## v0.1.0 — Core Engine ✓

- [x] Backtest engine (Pandas-based, no external dependencies beyond data/rich)
- [x] yfinance data provider with SQLite cache
- [x] AI strategy generation (Claude Sonnet)
- [x] Broker adapters: Alpaca, Zerodha, IBKR
- [x] CLI: research, backtest, report, paper (stub), pull, publish, serve, leaderboard
- [x] MCP server for Claude Desktop
- [x] Community registry: strategies, skills, lessons, graveyard
- [x] GitHub Actions CI + auto-verify contributions

## v0.2.0 — Protocol

- [ ] CI-verified strategy contributions (full coverage)
- [ ] Leaderboard: top strategies by Sharpe ratio, region, asset class
- [ ] Strategy challenges: "beat this benchmark" monthly competitions
- [ ] `samay pull` + `samay publish` fully automated workflow
- [ ] Strategy versioning (pull specific versions)
- [ ] Performance attribution reports (which holdings drove returns)
- [ ] Skill evaluation: "which skills appear in winning strategies?"

## v0.3.0 — Multi-Asset

- [ ] Crypto support: Binance, Coinbase adapters
- [ ] Options strategies (basic: covered calls, protective puts)
- [ ] Futures support
- [ ] Portfolio-level backtesting (not just single-ticker rebalancing)
- [ ] Multi-timeframe strategies (daily + weekly rules)
- [ ] Correlation-aware position sizing

## v1.0.0 — Live Trading

- [ ] Real order execution (not just paper)
- [ ] Risk management layer: max position size, max daily loss
- [ ] Position sizing: Kelly Criterion, half-Kelly
- [ ] Live monitoring dashboard
- [ ] Slippage modeling from live fills
- [ ] Order logging + audit trail
- [ ] Graceful shutdown (close positions cleanly)
- [ ] Compliance: track and report taxes, dividends

## Beyond v1.0

- [ ] Machine learning: learn strategies from historical patterns
- [ ] Ensemble strategies: combine multiple strategies intelligently
- [ ] Real-time signal generation (not batch)
- [ ] Mobile app for monitoring live strategies
- [ ] Browser-based strategy builder (no code)
- [ ] Marketplace: buy/sell strategy performance (tokenized)
