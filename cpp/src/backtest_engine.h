#pragma once

#include <vector>
#include <string>
#include <unordered_map>
#include <cmath>

struct Trade {
    std::string ticker;
    int entry_idx;
    int exit_idx;
    double entry_price;
    double exit_price;
    double pnl;
    int duration_days;
};

class FastBacktestEngine {
public:
    struct Config {
        double initial_capital = 100000.0;
        double commission = 0.001;
        double slippage = 0.0005;
    };

    FastBacktestEngine(const Config& cfg) : config(cfg) {}

    std::vector<double> simulate(
        const std::vector<double>& opens,
        const std::vector<double>& closes,
        const std::vector<int>& signals,
        double capital,
        std::vector<Trade>& trades_out
    );

private:
    Config config;
};
