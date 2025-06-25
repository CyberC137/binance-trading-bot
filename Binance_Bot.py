
import argparse
import logging
import sys
import time
import json
from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceRequestException

class BasicBot:
    def __init__(self, api_key: str, api_secret: str, testnet: bool = True, log_file: str = "bot.log"):
        """
        Initialize the Binance Futures client.
        :param api_key: Your API key
        :param api_secret: Your API secret
        :param testnet: If True, connect to Futures Testnet
        :param log_file: Path to log file
        """
        # Configure logging
        self.logger = logging.getLogger("BasicBot")
        self.logger.setLevel(logging.INFO)
        fmt = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
        fh = logging.FileHandler(log_file)
        fh.setFormatter(fmt)
        self.logger.addHandler(fh)
        # Also log to console
        ch = logging.StreamHandler(sys.stdout)
        ch.setFormatter(fmt)
        self.logger.addHandler(ch)

        # Initialize client
        try:
            if testnet:
                # Pass testnet=True to configure testnet endpoints (Spot, Futures, Options) :contentReference[oaicite:2]{index=2}
                self.client = Client(api_key, api_secret, testnet=True)
                # Override futures URLs if needed; python-binance’s testnet=True should route futures endpoints to testnet :contentReference[oaicite:3]{index=3}
                # But if needed explicitly:
                # self.client.FUTURES_URL = "https://testnet.binancefuture.com"
                self.logger.info("Initialized Binance Client in TESTNET mode.")
            else:
                self.client = Client(api_key, api_secret)
                self.logger.info("Initialized Binance Client in LIVE mode.")
        except Exception as e:
            self.logger.error(f"Error initializing Binance Client: {e}", exc_info=True)
            raise

    def place_market_order(self, symbol: str, side: str, quantity: float) -> dict:
        """
        Place a market order on Futures.
        :param symbol: e.g., 'BTCUSDT'
        :param side: 'BUY' or 'SELL'
        :param quantity: quantity (float)
        :return: API response dict
        """
        params = {
            "symbol": symbol,
            "side": side,
            "type": "MARKET",
            "quantity": quantity
        }
        self.logger.info(f"Placing MARKET order: {params}")
        try:
            resp = self.client.futures_create_order(**params)
            self.logger.info(f"Order response: {resp}")
            return resp
        except BinanceAPIException as e:
            # API returned error
            self.logger.error(f"BinanceAPIException when placing market order: {e.status_code} {e.message}", exc_info=True)
            raise
        except BinanceRequestException as e:
            self.logger.error(f"BinanceRequestException when placing market order: {e}", exc_info=True)
            raise
        except Exception as e:
            self.logger.error(f"Unexpected exception when placing market order: {e}", exc_info=True)
            raise

    def place_limit_order(self, symbol: str, side: str, quantity: float, price: float, time_in_force: str = "GTC") -> dict:
        """
        Place a limit order on Futures.
        :param symbol: e.g., 'BTCUSDT'
        :param side: 'BUY' or 'SELL'
        :param quantity: float
        :param price: float
        :param time_in_force: e.g., 'GTC', 'IOC', etc.
        :return: API response dict
        """
        params = {
            "symbol": symbol,
            "side": side,
            "type": "LIMIT",
            "quantity": quantity,
            "price": price,
            "timeInForce": time_in_force
        }
        self.logger.info(f"Placing LIMIT order: {params}")
        try:
            resp = self.client.futures_create_order(**params)
            self.logger.info(f"Order response: {resp}")
            return resp
        except BinanceAPIException as e:
            self.logger.error(f"BinanceAPIException when placing limit order: {e.status_code} {e.message}", exc_info=True)
            raise
        except BinanceRequestException as e:
            self.logger.error(f"BinanceRequestException when placing limit order: {e}", exc_info=True)
            raise
        except Exception as e:
            self.logger.error(f"Unexpected exception when placing limit order: {e}", exc_info=True)
            raise

    # Optional: advanced order types (example: STOP_MARKET)
    def place_stop_market_order(self, symbol: str, side: str, quantity: float, stop_price: float) -> dict:
        """
        Place a Stop Market order on Futures.
        Note: Check via exchange info if 'STOP_MARKET' is supported for symbol :contentReference[oaicite:4]{index=4}.
        :param symbol: e.g., 'BTCUSDT'
        :param side: 'BUY' or 'SELL'
        :param quantity: float
        :param stop_price: trigger price
        :return: API response dict
        """
        params = {
            "symbol": symbol,
            "side": side,
            "type": "STOP_MARKET",
            "stopPrice": stop_price,
            "closePosition": False,  # or True for closing entire position
            "quantity": quantity
        }
        self.logger.info(f"Placing STOP_MARKET order: {params}")
        try:
            resp = self.client.futures_create_order(**params)
            self.logger.info(f"Order response: {resp}")
            return resp
        except BinanceAPIException as e:
            self.logger.error(f"BinanceAPIException when placing stop market order: {e.status_code} {e.message}", exc_info=True)
            raise
        except Exception as e:
            self.logger.error(f"Unexpected exception when placing stop market order: {e}", exc_info=True)
            raise

def parse_args():
    parser = argparse.ArgumentParser(description="Basic Binance Futures Testnet Trading Bot CLI")
    parser.add_argument("--api-key", required=True, help="Binance API Key")
    parser.add_argument("--api-secret", required=True, help="Binance API Secret")
    parser.add_argument("--testnet", action="store_true", help="Use Futures Testnet (default if flag provided)")
    subparsers = parser.add_subparsers(dest="command", required=True, help="Sub-command to execute")

    # Market order subcommand
    market_parser = subparsers.add_parser("market", help="Place a market order")
    market_parser.add_argument("--symbol", required=True, type=str, help="Trading pair, e.g., BTCUSDT")
    market_parser.add_argument("--side", required=True, choices=["BUY", "SELL"], help="Order side")
    market_parser.add_argument("--quantity", required=True, type=float, help="Quantity to trade")

    # Limit order subcommand
    limit_parser = subparsers.add_parser("limit", help="Place a limit order")
    limit_parser.add_argument("--symbol", required=True, type=str, help="Trading pair, e.g., BTCUSDT")
    limit_parser.add_argument("--side", required=True, choices=["BUY", "SELL"], help="Order side")
    limit_parser.add_argument("--quantity", required=True, type=float, help="Quantity to trade")
    limit_parser.add_argument("--price", required=True, type=float, help="Limit price")
    limit_parser.add_argument("--time-in-force", default="GTC", choices=["GTC","IOC","FOK"], help="Time in Force")

    # Optional: Stop Market order
    stop_parser = subparsers.add_parser("stop-market", help="Place a stop market order")
    stop_parser.add_argument("--symbol", required=True, type=str, help="Trading pair, e.g., BTCUSDT")
    stop_parser.add_argument("--side", required=True, choices=["BUY", "SELL"], help="Order side")
    stop_parser.add_argument("--quantity", required=True, type=float, help="Quantity to trade")
    stop_parser.add_argument("--stop-price", required=True, type=float, help="Stop trigger price")

    return parser.parse_args()

def validate_symbol(symbol: str):
    # Basic validation: non-empty, uppercase alphanumeric
    if not symbol.isalnum():
        raise ValueError(f"Invalid symbol format: {symbol}")
    # Further validation against exchange info could be added:
    # e.g., client.futures_exchange_info() to check if symbol exists.
    return symbol.upper()

def main():
    args = parse_args()
    # Instantiate bot
    try:
        bot = BasicBot(api_key=args.api_key, api_secret=args.api_secret, testnet=args.testnet)
    except Exception as e:
        print(f"Failed to initialize bot: {e}")
        sys.exit(1)

    # Dispatch commands
    try:
        if args.command == "market":
            symbol = validate_symbol(args.symbol)
            side = args.side
            qty = args.quantity
            if qty <= 0:
                raise ValueError("Quantity must be positive")
            resp = bot.place_market_order(symbol=symbol, side=side, quantity=qty)
            print("Market order placed. Response:")
            print(json.dumps(resp, indent=2))

        elif args.command == "limit":
            symbol = validate_symbol(args.symbol)
            side = args.side
            qty = args.quantity
            price = args.price
            if qty <= 0 or price <= 0:
                raise ValueError("Quantity and price must be positive")
            tif = args.time_in_force
            resp = bot.place_limit_order(symbol=symbol, side=side, quantity=qty, price=price, time_in_force=tif)
            print("Limit order placed. Response:")
            print(json.dumps(resp, indent=2))

        elif args.command == "stop-market":
            symbol = validate_symbol(args.symbol)
            side = args.side
            qty = args.quantity
            stop_price = args.stop_price
            if qty <= 0 or stop_price <= 0:
                raise ValueError("Quantity and stop price must be positive")
            resp = bot.place_stop_market_order(symbol=symbol, side=side, quantity=qty, stop_price=stop_price)
            print("Stop Market order placed. Response:")
            print(json.dumps(resp, indent=2))

        else:
            print(f"Unknown command: {args.command}")
            sys.exit(1)
    except ValueError as ve:
        print(f"Input validation error: {ve}")
        sys.exit(1)
    except BinanceAPIException as bae:
        print(f"Binance API error: {bae.status_code} - {bae.message}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()