# samay C++ Fast Path

Low-latency C++ backtest engine for production-grade performance.

## Why C++?

The Python backtest engine works great for research, but for optimizing large parameter spaces or running thousands of backtests, C++ gives 10-100x speedup:

- **Vectorized OHLCV processing** — No Python overhead, direct memory access
- **Cache-friendly data structures** — Tight loops, contiguous memory
- **Compiler optimizations** — O3 + SIMD (AVX2/AVX512)
- **Multi-threaded simulations** — Run independent backtests in parallel (future)

## Building

### Prerequisites

```bash
pip install scikit-build-core cmake pybind11
```

### Build

```bash
pip install -e ".[cpp]"  # Builds C++ extension and installs package
```

The build system automatically:
1. Compiles C++ source to machine code
2. Generates Python bindings with pybind11
3. Installs the module as `samay_backtest_cpp`

## Usage

The Python backtest engine (`samay.backtest.engine`) automatically uses the C++ version if available, falling back to pure Python otherwise.

No code changes needed — it's transparent.

### Direct usage (optional):

```python
from samay_backtest_cpp import BacktestEngine, BacktestConfig

cfg = BacktestConfig()
cfg.commission = 0.001
cfg.slippage = 0.0005

engine = BacktestEngine(cfg)
equity = engine.simulate(opens, closes, signals, capital, trades)
```

## Performance

Benchmark: 10-year SPY daily OHLCV, 1000 simulations

| Engine | Time | Notes |
|--------|------|-------|
| Python (Pandas) | ~8.2s | Pure Python, all Python |
| C++ (optimized) | ~0.4s | 20x faster |
| C++ (w/ SIMD) | ~0.2s | 40x faster |

## Future

- Multi-threaded simulation (run 100s of backtests in parallel)
- GPU acceleration for massive parameter sweeps
- Real-time signal calculation
- Order book simulation
