# Binance Trading Bot 

A simple trading bot built with Python that connects to the Binance **Futures Testnet** using the official Binance API. This bot allows users to place market and limit buy/sell orders via a command-line interface simulated in a Google Colab notebook.

---

##  Features

-  Uses Binance Futures Testnet for safe trading practice
-  Place **Market** and **Limit** orders
-  Supports both **Buy** and **Sell** sides
-  Accepts user inputs for symbol, order type, quantity, and price
-  Logs all requests, responses, and errors to a local log file
-  Built using the `python-binance` SDK

---

##  Installation

1. **Clone this repository:**

   ```bash
   git clone https://github.com/CyberC137/Binance_Trading_Bot.git
   cd Binance_Trading_Bot
   ```

2. **Open the notebook in Google Colab:**

   - [Open in Google Colab](https://colab.research.google.com/)

3. **Install required dependencies in Colab:**

   ```python
   !pip install python-binance
   ```

---

##  Setup Binance Futures Testnet

1. Register on the [Binance Futures Testnet](https://testnet.binancefuture.com/).
2. Generate an API Key and Secret.
3. Replace the placeholder strings in the notebook:

   ```python
   api_key = 'YOUR_TESTNET_API_KEY'
   api_secret = 'YOUR_TESTNET_API_SECRET'
   ```

---

##  Usage

Run each cell in the notebook sequentially. When prompted:

- Input the trading **symbol** (e.g., `BTCUSDT`)
- Choose the **order type**: `MARKET` or `LIMIT`
- Enter **BUY** or **SELL** for the order side
- Provide the **quantity**
- If LIMIT order, input the **price**

The bot will place the order and print the execution details. Logs are saved in `bot.log`.

---

##  File Structure

```
📦 Binance_Trading_Bot/
├── Binance_Trading_Bot.ipynb   # Main notebook
├── bot.log                     # Log file (auto-generated)
└── README.md                   # This file
```

---

##  Notes

- This bot only works on the **Futures Testnet**, not the live environment.
- Orders are simulated and carry no financial risk.
- Built for educational and interview evaluation purposes.

---

##  Disclaimer

This project is for demonstration and educational use only. Use responsibly and do not deploy with real funds without proper testing.

---
