#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "backtest_engine.h"

namespace py = pybind11;

PYBIND11_MODULE(samay_backtest_cpp, m) {
    m.doc() = "Low-latency C++ backtest engine for samay";

    // Trade struct binding
    py::class_<Trade>(m, "Trade")
        .def(py::init<>())
        .def_readwrite("ticker", &Trade::ticker)
        .def_readwrite("entry_idx", &Trade::entry_idx)
        .def_readwrite("exit_idx", &Trade::exit_idx)
        .def_readwrite("entry_price", &Trade::entry_price)
        .def_readwrite("exit_price", &Trade::exit_price)
        .def_readwrite("pnl", &Trade::pnl)
        .def_readwrite("duration_days", &Trade::duration_days);

    // Config binding
    py::class_<FastBacktestEngine::Config>(m, "BacktestConfig")
        .def(py::init<>())
        .def_readwrite("initial_capital", &FastBacktestEngine::Config::initial_capital)
        .def_readwrite("commission", &FastBacktestEngine::Config::commission)
        .def_readwrite("slippage", &FastBacktestEngine::Config::slippage);

    // Engine binding
    py::class_<FastBacktestEngine>(m, "BacktestEngine")
        .def(py::init<const FastBacktestEngine::Config&>())
        .def("simulate", &FastBacktestEngine::simulate,
             "Fast backtesting simulation with C++",
             py::arg("opens"),
             py::arg("closes"),
             py::arg("signals"),
             py::arg("capital"),
             py::arg("trades_out"));
}
