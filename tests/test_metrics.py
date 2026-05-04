import pytest
import pandas as pd
import numpy as np

from samay.backtest.metrics import calculate_metrics


def make_equity_curve(returns: list[float], initial: float = 100_000) -> pd.Series:
    dates = pd.date_range("2020-01-01", periods=len(returns) + 1, freq="B")
    values = [initial]
    for r in returns:
        values.append(values[-1] * (1 + r))
    return pd.Series(values, index=dates)


def make_trades(pnls: list[float]) -> pd.DataFrame:
    records = []
    for i, pnl in enumerate(pnls):
        records.append({
            "ticker": "SPY",
            "entry_date": pd.Timestamp(f"2020-{i%12+1:02d}-01"),
            "exit_date": pd.Timestamp(f"2020-{i%12+1:02d}-15"),
            "entry_price": 100.0,
            "exit_price": 100.0 + pnl / 10,
            "pnl": pnl,
            "duration_days": 14,
        })
    return pd.DataFrame(records)


def test_total_return_positive():
    equity = make_equity_curve([0.01] * 252)
    trades = make_trades([100] * 10)
    metrics = calculate_metrics(equity, trades)
    assert metrics["total_return_pct"] > 0


def test_total_return_negative():
    equity = make_equity_curve([-0.005] * 252)
    trades = make_trades([-50] * 10)
    metrics = calculate_metrics(equity, trades)
    assert metrics["total_return_pct"] < 0


def test_sharpe_positive_returns():
    equity = make_equity_curve([0.001] * 500)
    trades = make_trades([100] * 5)
    metrics = calculate_metrics(equity, trades)
    assert metrics["sharpe_ratio"] > 0


def test_max_drawdown_is_negative():
    returns = [0.01] * 100 + [-0.05] * 10 + [0.01] * 100
    equity = make_equity_curve(returns)
    trades = make_trades([100, -500, 100])
    metrics = calculate_metrics(equity, trades)
    assert metrics["max_drawdown_pct"] < 0


def test_win_rate_all_winners():
    equity = make_equity_curve([0.001] * 252)
    trades = make_trades([100, 200, 50, 75])
    metrics = calculate_metrics(equity, trades)
    assert metrics["win_rate_pct"] == 100.0


def test_win_rate_all_losers():
    equity = make_equity_curve([-0.001] * 252)
    trades = make_trades([-100, -200, -50])
    metrics = calculate_metrics(equity, trades)
    assert metrics["win_rate_pct"] == 0.0


def test_num_trades():
    equity = make_equity_curve([0.001] * 252)
    trades = make_trades([100] * 7)
    metrics = calculate_metrics(equity, trades)
    assert metrics["num_trades"] == 7


def test_empty_trades():
    equity = make_equity_curve([0.001] * 252)
    trades = pd.DataFrame(columns=["ticker", "entry_date", "exit_date", "entry_price", "exit_price", "pnl", "duration_days"])
    metrics = calculate_metrics(equity, trades)
    assert metrics["num_trades"] == 0
    assert metrics["win_rate_pct"] == 0.0
