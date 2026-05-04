import numpy as np
import pandas as pd


def calculate_metrics(equity_curve: pd.Series, trades: pd.DataFrame) -> dict:
    if len(equity_curve) < 2:
        return {}

    initial_value = equity_curve.iloc[0]
    final_value = equity_curve.iloc[-1]

    total_return_pct = (final_value / initial_value - 1) * 100

    days = (equity_curve.index[-1] - equity_curve.index[0]).days
    years = days / 365.25
    cagr_pct = ((final_value / initial_value) ** (1 / years) - 1) * 100 if years > 0 else 0.0

    daily_returns = equity_curve.pct_change().dropna()

    risk_free_daily = 0.05 / 252
    excess_returns = daily_returns - risk_free_daily
    sharpe = (
        (excess_returns.mean() / excess_returns.std()) * np.sqrt(252)
        if excess_returns.std() > 0
        else 0.0
    )

    downside = excess_returns[excess_returns < 0]
    sortino = (
        (excess_returns.mean() / downside.std()) * np.sqrt(252)
        if len(downside) > 0 and downside.std() > 0
        else 0.0
    )

    rolling_max = equity_curve.cummax()
    drawdown = (equity_curve - rolling_max) / rolling_max
    max_drawdown_pct = drawdown.min() * 100

    in_drawdown = drawdown < 0
    max_dd_duration = _max_drawdown_duration(in_drawdown)

    calmar = cagr_pct / abs(max_drawdown_pct) if max_drawdown_pct != 0 else 0.0

    num_trades = len(trades)
    win_rate_pct = 0.0
    avg_duration = 0.0
    profit_factor = 0.0

    if num_trades > 0:
        winning = trades[trades["pnl"] > 0]
        losing = trades[trades["pnl"] <= 0]
        win_rate_pct = len(winning) / num_trades * 100
        avg_duration = trades["duration_days"].mean()
        gross_profit = winning["pnl"].sum() if len(winning) > 0 else 0
        gross_loss = abs(losing["pnl"].sum()) if len(losing) > 0 else 0
        profit_factor = gross_profit / gross_loss if gross_loss > 0 else float("inf")

    return {
        "total_return_pct": round(total_return_pct, 2),
        "cagr_pct": round(cagr_pct, 2),
        "sharpe_ratio": round(sharpe, 3),
        "sortino_ratio": round(sortino, 3),
        "max_drawdown_pct": round(max_drawdown_pct, 2),
        "max_drawdown_duration_days": max_dd_duration,
        "win_rate_pct": round(win_rate_pct, 2),
        "num_trades": num_trades,
        "avg_trade_duration_days": round(avg_duration, 1),
        "profit_factor": round(profit_factor, 3) if profit_factor != float("inf") else "inf",
        "calmar_ratio": round(calmar, 3),
    }


def _max_drawdown_duration(in_drawdown: pd.Series) -> int:
    max_duration = 0
    current_duration = 0
    for val in in_drawdown:
        if val:
            current_duration += 1
            max_duration = max(max_duration, current_duration)
        else:
            current_duration = 0
    return max_duration
