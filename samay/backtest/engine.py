from dataclasses import dataclass

import pandas as pd

from samay.backtest.metrics import calculate_metrics
from samay.data.yfinance_provider import YFinanceProvider
from samay.strategy.base import Strategy


@dataclass
class BacktestConfig:
    strategy: Strategy
    tickers: list[str]
    start_date: str
    end_date: str
    initial_capital: float = 100_000.0
    commission: float = 0.001
    slippage: float = 0.0005


@dataclass
class BacktestResult:
    equity_curve: pd.Series
    trades: pd.DataFrame
    metrics: dict
    strategy_name: str
    tickers: list[str]
    start_date: str
    end_date: str


class BacktestEngine:
    def __init__(self, config: BacktestConfig, provider=None):
        self.config = config
        self.provider = provider or YFinanceProvider()

    def run(self) -> BacktestResult:
        cfg = self.config
        capital_per_ticker = cfg.initial_capital / len(cfg.tickers)

        all_equity_curves = []
        all_trades = []

        for ticker in cfg.tickers:
            data = self.provider.get_ohlcv(ticker, cfg.start_date, cfg.end_date)
            signals = cfg.strategy.generate_signals(data)
            equity_curve, trades = self._simulate(ticker, data, signals, capital_per_ticker)
            all_equity_curves.append(equity_curve)
            all_trades.extend(trades)

        combined = pd.concat(all_equity_curves, axis=1).ffill().bfill().sum(axis=1)
        trades_df = (
            pd.DataFrame(all_trades)
            if all_trades
            else pd.DataFrame(
                columns=["ticker", "entry_date", "exit_date", "entry_price", "exit_price", "pnl", "duration_days"]
            )
        )

        metrics = calculate_metrics(combined, trades_df)

        return BacktestResult(
            equity_curve=combined,
            trades=trades_df,
            metrics=metrics,
            strategy_name=cfg.strategy.name,
            tickers=cfg.tickers,
            start_date=cfg.start_date,
            end_date=cfg.end_date,
        )

    def _simulate(
        self,
        ticker: str,
        data: pd.DataFrame,
        signals: pd.Series,
        capital: float,
    ) -> tuple[pd.Series, list[dict]]:
        cfg = self.config
        cash = capital
        shares = 0.0
        entry_price = 0.0
        entry_date = None
        cash_at_entry = 0.0
        equity_values = []
        trades = []

        dates = data.index.tolist()
        opens = data["open"].tolist()
        closes = data["close"].tolist()

        for i in range(len(dates)):
            date = dates[i]
            close = closes[i]

            if i > 0:
                prev_date = dates[i - 1]
                sig = signals.get(prev_date, 0) if hasattr(signals, "get") else (signals.loc[prev_date] if prev_date in signals.index else 0)
                fill_price = opens[i]

                if sig == 1 and shares == 0:
                    buy_price = fill_price * (1 + cfg.slippage)
                    commission_cost = cash * cfg.commission
                    available = cash - commission_cost
                    if available > 0 and buy_price > 0:
                        cash_at_entry = cash
                        shares = available / buy_price
                        cash = 0.0
                        entry_price = buy_price
                        entry_date = date

                elif sig == -1 and shares > 0:
                    sell_price = fill_price * (1 - cfg.slippage)
                    gross = shares * sell_price
                    commission_cost = gross * cfg.commission
                    cash = gross - commission_cost
                    pnl = cash - cash_at_entry
                    duration = (date - entry_date).days if entry_date else 0
                    trades.append(
                        {
                            "ticker": ticker,
                            "entry_date": entry_date,
                            "exit_date": date,
                            "entry_price": entry_price,
                            "exit_price": sell_price,
                            "pnl": pnl,
                            "duration_days": duration,
                        }
                    )
                    shares = 0.0
                    entry_price = 0.0
                    entry_date = None
                    cash_at_entry = 0.0

            portfolio_value = cash + shares * close
            equity_values.append(portfolio_value)

        equity_curve = pd.Series(equity_values, index=data.index, name=ticker)
        return equity_curve, trades
