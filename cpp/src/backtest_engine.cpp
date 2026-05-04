#include "backtest_engine.h"
#include <algorithm>

std::vector<double> FastBacktestEngine::simulate(
    const std::vector<double>& opens,
    const std::vector<double>& closes,
    const std::vector<int>& signals,
    double capital,
    std::vector<Trade>& trades_out
) {
    std::vector<double> equity_values;
    equity_values.reserve(opens.size());

    double cash = capital;
    double shares = 0.0;
    double entry_price = 0.0;
    int entry_idx = -1;
    double cash_at_entry = 0.0;

    for (size_t i = 0; i < opens.size(); ++i) {
        double close_price = closes[i];

        if (i > 0) {
            int sig = signals[i - 1];
            double fill_price = opens[i];

            if (sig == 1 && shares == 0.0) {
                // BUY signal
                double buy_price = fill_price * (1.0 + config.slippage);
                double commission_cost = cash * config.commission;
                double available = cash - commission_cost;

                if (available > 0.0 && buy_price > 0.0) {
                    cash_at_entry = cash;
                    shares = available / buy_price;
                    cash = 0.0;
                    entry_price = buy_price;
                    entry_idx = i;
                }
            } else if (sig == -1 && shares > 0.0) {
                // SELL signal
                double sell_price = fill_price * (1.0 - config.slippage);
                double gross = shares * sell_price;
                double commission_cost = gross * config.commission;
                cash = gross - commission_cost;
                double pnl = cash - cash_at_entry;
                int duration = static_cast<int>(i - entry_idx);

                trades_out.push_back({
                    "",  // ticker filled by caller
                    entry_idx,
                    static_cast<int>(i),
                    entry_price,
                    sell_price,
                    pnl,
                    duration
                });

                shares = 0.0;
                entry_price = 0.0;
                entry_idx = -1;
                cash_at_entry = 0.0;
            }
        }

        // Track portfolio value
        double portfolio_value = cash + shares * close_price;
        equity_values.push_back(portfolio_value);
    }

    return equity_values;
}
