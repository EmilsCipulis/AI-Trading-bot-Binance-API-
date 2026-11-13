import io
import runpy
import sys
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, call, patch


class RequestTimeout(Exception):
    pass


class TradingBotTest(unittest.TestCase):
    def test_polling_recovers_after_binance_times_out(self):
        exchange = Mock(spec_set=["fetch_ticker"])
        exchange.fetch_ticker.side_effect = [
            RequestTimeout("Binance ticker request timed out"),
            {"last": 45000},
        ]
        ccxt = SimpleNamespace(
            binance=Mock(return_value=exchange),
            RequestTimeout=RequestTimeout,
        )
        sleep = Mock(side_effect=[None, KeyboardInterrupt])
        output = io.StringIO()
        script_path = Path(__file__).with_name("trading_bot.py")

        with patch.dict(sys.modules, {"ccxt": ccxt}), patch("time.sleep", sleep):
            with redirect_stdout(output), self.assertRaises(KeyboardInterrupt):
                runpy.run_path(str(script_path), run_name="__main__")

        self.assertEqual(exchange.mock_calls, [call.fetch_ticker("BTC/USDT")] * 2)
        self.assertEqual(sleep.call_args_list, [call(5), call(5)])
        self.assertEqual(
            output.getvalue().splitlines(),
            [
                "Timed out fetching BTC/USDT price. Retrying in 5 seconds.",
                "Current BTC/USDT Price: 45000",
            ],
        )
