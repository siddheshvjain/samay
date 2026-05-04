import pytest
import pandas as pd
import numpy as np
from datetime import datetime
from unittest.mock import patch, MagicMock

from samay.strategy.base import Strategy
from samay.backtest.engine import BacktestConfig, BacktestEngine, BacktestResult


class SimpleStrategy(Strategy):
    name = "test-strategy"
    description = "Always buys on day 1, sells on day 10"

    def generate_signals(self, data: pd.DataFrame) -> pd.Series:
        signals = pd.Series(0, index=data.index)
        if len(signals) > 0:
            signals.iloc[0] = 1
        if len(signals) > 10:
            signals.iloc[10] = -1
        return signals


def make_fake_ohlcv(n_days=30, start_price=100.0):
    dates = pd.date_range("2020-01-01", periods=n_days, freq="B")
    prices = [start_price * (1 + 0.001 * i) for i in range(n_days)]
    return pd.DataFrame({
        "open": prices,
        "high": [p * 1.01 for p in prices],
        "low": [p * 0.99 for p in prices],
        "close": prices,
        "volume": [1_000_000] * n_days,
    }, index=dates)


@patch("samay.backtest.engine.YFinanceProvider")
def test_engine_runs(MockProvider):
    fake_data = make_fake_ohlcv()
    mock_instance = MagicMock()
    mock_instance.get_ohlcv.return_value = fake_data
    MockProvider.return_value = mock_instance

    strategy = SimpleStrategy()
    config = BacktestConfig(
        strategy=strategy,
        tickers=["SPY"],
        start_date="2020-01-01",
        end_date="2020-06-01",
        initial_capital=10_000,
    )

    engine = BacktestEngine(config)
    result = engine.run()

    assert isinstance(result, BacktestResult)
    assert len(result.equity_curve) == len(fake_data)
    assert result.strategy_name == "test-strategy"


@patch("samay.backtest.engine.YFinanceProvider")
def test_engine_multi_ticker(MockProvider):
    fake_data = make_fake_ohlcv()
    mock_instance = MagicMock()
    mock_instance.get_ohlcv.return_value = fake_data
    MockProvider.return_value = mock_instance

    strategy = SimpleStrategy()
    config = BacktestConfig(
        strategy=strategy,
        tickers=["AAPL", "MSFT"],
        start_date="2020-01-01",
        end_date="2020-06-01",
        initial_capital=20_000,
    )

    engine = BacktestEngine(config)
    result = engine.run()

    assert isinstance(result, BacktestResult)
    assert result.tickers == ["AAPL", "MSFT"]


@patch("samay.backtest.engine.YFinanceProvider")
def test_initial_equity_matches_capital(MockProvider):
    fake_data = make_fake_ohlcv()
    mock_instance = MagicMock()
    mock_instance.get_ohlcv.return_value = fake_data
    MockProvider.return_value = mock_instance

    strategy = SimpleStrategy()
    config = BacktestConfig(
        strategy=strategy,
        tickers=["SPY"],
        start_date="2020-01-01",
        end_date="2020-06-01",
        initial_capital=100_000,
    )

    engine = BacktestEngine(config)
    result = engine.run()

    assert result.equity_curve.iloc[0] == pytest.approx(100_000, rel=0.01)
