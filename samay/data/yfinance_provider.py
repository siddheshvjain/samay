import pickle
import sqlite3
import time
from pathlib import Path

import pandas as pd
import yfinance as yf

from samay.data.base import DataProvider

CACHE_DIR = Path.home() / ".samay"
CACHE_DB = CACHE_DIR / "cache.db"
CACHE_TTL_SECONDS = 3600


class YFinanceProvider(DataProvider):
    def __init__(self):
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        self._init_cache()

    def _init_cache(self):
        with sqlite3.connect(CACHE_DB) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS ohlcv_cache (
                    key TEXT PRIMARY KEY,
                    data BLOB,
                    cached_at REAL
                )
            """)

    def _cache_key(self, ticker: str, start: str, end: str, interval: str) -> str:
        return f"{ticker}|{start}|{end}|{interval}"

    def _get_cached(self, key: str) -> pd.DataFrame | None:
        with sqlite3.connect(CACHE_DB) as conn:
            row = conn.execute(
                "SELECT data, cached_at FROM ohlcv_cache WHERE key = ?", (key,)
            ).fetchone()
        if row is None:
            return None
        if time.time() - row[1] > CACHE_TTL_SECONDS:
            return None
        return pickle.loads(row[0])

    def _set_cached(self, key: str, df: pd.DataFrame):
        data = pickle.dumps(df)
        with sqlite3.connect(CACHE_DB) as conn:
            conn.execute(
                "INSERT OR REPLACE INTO ohlcv_cache (key, data, cached_at) VALUES (?, ?, ?)",
                (key, data, time.time()),
            )

    def get_ohlcv(
        self,
        ticker: str,
        start: str,
        end: str,
        interval: str = "1d",
    ) -> pd.DataFrame:
        key = self._cache_key(ticker, start, end, interval)
        cached = self._get_cached(key)
        if cached is not None:
            return cached

        raw = yf.download(ticker, start=start, end=end, interval=interval, progress=False)
        if raw.empty:
            raise ValueError(f"No data returned for {ticker} from {start} to {end}")

        raw.columns = [c[0].lower() if isinstance(c, tuple) else c.lower() for c in raw.columns]
        df = raw[["open", "high", "low", "close", "volume"]].copy()
        df.index = pd.to_datetime(df.index)

        self._set_cached(key, df)
        return df
