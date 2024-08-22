# ML-Driven Trading Strategy with FinBERT Sentiment Analysis

**Created By Aws Ali, 2024-08-21**

The ML-Driven Trading Strategy is a tool designed to execute and backtest trading strategies based on financial news sentiment analysis. It uses a pre-trained FinBERT model to analyze news articles and make informed trading decisions via the Alpaca trading platform.

The project features sentiment analysis using the FinBERT model to assess the overall sentiment of financial news, automated trading integrated with the Alpaca API to execute buy/sell orders based on sentiment analysis results, backtesting using historical data to refine and optimize performance, and configurable parameters allowing users to adjust settings such as the stock symbol to monitor, the percentage of cash to risk per trade, and backtesting timeframes.

## Requirements

- Windows, macOS, or Linux
- An internet connection for interacting with Alpaca and fetching news
- Python 3.8 or later
- Pytorch 2.2 or later
- Transformers
- Lumibot
- Alpaca-trade-api

## Setup and Installation

1. **Clone the Repository**: Clone the repository to your local machine using the command:

   ```bash
   git clone https://github.com/AwsAli05/Python-trading-bot.git
   ```

2. **Install Dependencies**: Navigate to the project directory and install the required Python packages using the command:

   ```bash
   pip install -r requirements.txt
   ```

3. **API Configuration**: Update the `ALPACA_CREDS` dictionary in the `trading_strategy.py` file with your Alpaca API key and secret. Example:

   ```python
   ALPACA_CREDS = {
       "API_KEY": "your_api_key",
       "API_SECRET": "your_api_secret",
       "PAPER": True  # Set to False for live trading
   }
   ```

## Usage

To use the ML-Driven Trading Strategy, follow these steps:

1. **Configure the Strategy**: Open the `tradingbot.py` file and adjust the parameters such as the stock symbol (`symbol`) and the cash-at-risk percentage (`cash_at_risk`).

2. **Run the Strategy**: Execute the trading strategy by running the `tradingbot.py` script:

   ```bash
   python tradingbot.py
   ```

The program will execute the trading strategy based on the configured parameters, perform sentiment analysis on relevant news articles, and make buy/sell decisions accordingly. The results, including trade orders and backtesting performance, will be displayed in the console.

## Customization

- **Modifying Parameters**: Adjust the parameters in the `trading_strategy.py` file to customize the trading strategy according to your preferences. For example, you can change the stock symbol, alter the risk level, or update the backtesting timeframe.

## Support

If you encounter any issues or have questions, please feel free to contact the support team at [aliaws123@outlook.com].

## License

This software is provided under the [MIT License](LICENSE).
