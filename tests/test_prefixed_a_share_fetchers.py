# -*- coding: utf-8 -*-
"""
Regression tests for A-share codes written as SH.600000 / SZ.000001.
"""

import unittest

import pandas as pd

from data_provider.base import DataFetcherManager
from data_provider.baostock_fetcher import BaostockFetcher
from data_provider.pytdx_fetcher import PytdxFetcher


class _RecordingDailyFetcher:
    name = "RecordingDailyFetcher"
    priority = 1

    def __init__(self) -> None:
        self.calls = []

    def get_daily_data(self, stock_code: str, *args, **kwargs) -> pd.DataFrame:
        self.calls.append(stock_code)
        return pd.DataFrame({"date": ["2026-05-22"], "close": [10.0]})


class TestDataFetcherManagerPrefixedAShareCodes(unittest.TestCase):
    def test_get_daily_data_preserves_dotted_exchange_prefix_before_fetcher(self) -> None:
        fetcher = _RecordingDailyFetcher()
        manager = DataFetcherManager(fetchers=[fetcher])

        df, source = manager.get_daily_data("SH.000001", days=1)

        self.assertFalse(df.empty)
        self.assertEqual(source, "RecordingDailyFetcher")
        self.assertEqual(fetcher.calls, ["SH.000001"])


class TestBaostockPrefixedAShareCodes(unittest.TestCase):
    def test_convert_stock_code_accepts_dotted_exchange_prefix(self) -> None:
        fetcher = BaostockFetcher()

        self.assertEqual(fetcher._convert_stock_code("601888"), "sh.601888")
        self.assertEqual(fetcher._convert_stock_code("sh.601888"), "sh.601888")
        self.assertEqual(fetcher._convert_stock_code("SH.601888"), "sh.601888")
        self.assertEqual(fetcher._convert_stock_code("SZ.000001"), "sz.000001")

    def test_convert_stock_code_preserves_suffix_exchange_hint(self) -> None:
        fetcher = BaostockFetcher()

        self.assertEqual(fetcher._convert_stock_code("600519.SH"), "sh.600519")
        self.assertEqual(fetcher._convert_stock_code("000001.SZ"), "sz.000001")


class TestPytdxPrefixedAShareCodes(unittest.TestCase):
    def test_get_market_code_accepts_dotted_exchange_prefix(self) -> None:
        fetcher = PytdxFetcher(hosts=[])

        self.assertEqual(fetcher._get_market_code("601888"), (1, "601888"))
        self.assertEqual(fetcher._get_market_code("sh.601888"), (1, "601888"))
        self.assertEqual(fetcher._get_market_code("SH.601888"), (1, "601888"))
        self.assertEqual(fetcher._get_market_code("SZ.000001"), (0, "000001"))

    def test_get_market_code_preserves_suffix_exchange_hint(self) -> None:
        fetcher = PytdxFetcher(hosts=[])

        self.assertEqual(fetcher._get_market_code("600519.SH"), (1, "600519"))
        self.assertEqual(fetcher._get_market_code("000001.SZ"), (0, "000001"))


if __name__ == "__main__":
    unittest.main()
