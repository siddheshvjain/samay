"""
Optional C++ fast backtest engine.
Falls back to pure Python if C++ extension not available.
"""

import pandas as pd


def get_engine():
    """Return C++ engine if available, else pure Python fallback."""
    try:
        import samay_backtest_cpp  # noqa: F401
        return "cpp"
    except ImportError:
        return "python"


def simulate_fast(
    opens: list,
    closes: list,
    signals: pd.Series,
    capital: float,
    commission: float = 0.001,
    slippage: float = 0.0005,
) -> tuple[list, list]:
    """
    Fast simulation using C++ if available.
    Returns: (equity_values, trades)
    """
    engine_type = get_engine()

    if engine_type == "cpp":
        from samay_backtest_cpp import BacktestConfig, BacktestEngine

        cfg = BacktestConfig()
        cfg.initial_capital = capital
        cfg.commission = commission
        cfg.slippage = slippage

        engine = BacktestEngine(cfg)

        signal_list = [0] * len(opens)
        for i, date in enumerate(signals.index):
            if date in signals.index:
                signal_list[i] = int(signals.loc[date])

        trades = []
        equity = engine.simulate(opens, closes, signal_list, capital, trades)
        return equity, trades
    else:
        # Fallback to pure Python (not needed if C++ available)
        return None, None
