# Import necessary modules from the lumibot library for algorithmic trading
from lumibot.brokers import Alpaca  # Broker module for Alpaca API
from lumibot.backtesting import YahooDataBacktesting  # Module for backtesting with Yahoo Finance data
from lumibot.strategies.strategy import Strategy  # Base Strategy class for creating custom trading strategies
from lumibot.traders import Trader  # Trader class for executing strategies
from datetime import datetime  # Module for handling dates and times
from alpaca_trade_api import REST  # Alpaca API's REST client
from timedelta import Timedelta  # Module for handling time differences
from finbert_utils import estimate_sentiment  # Function to estimate sentiment from text (e.g., news headlines)

# Define API credentials for Alpaca
API_KEY = "YOUR API KEY" 
API_SECRET = "YOUR SECRET" 
BASE_URL = "YOUR ENDPOINT"

# Dictionary containing Alpaca API credentials and configuration for paper trading
ALPACA_CREDS = {
    "API_KEY": API_KEY, 
    "API_SECRET": API_SECRET, 
    "PAPER": True  # Indicates use of paper trading (simulated trading)
}

# Custom trading strategy class inheriting from the base Strategy class
class MLTrader(Strategy): 
    # Initialization method for the strategy
    def initialize(self, symbol: str = "SPY", cash_at_risk: float = 0.5): 
        self.symbol = symbol  # Stock symbol to trade (default is SPY)
        self.sleeptime = "24H"  # Time to wait between iterations
        self.last_trade = None  # Keeps track of the last trade action (buy/sell)
        self.cash_at_risk = cash_at_risk  # Percentage of cash to risk per trade
        self.api = REST(base_url=BASE_URL, key_id=API_KEY, secret_key=API_SECRET)  # Alpaca API client

    # Method to calculate position sizing (amount of stock to buy/sell)
    def position_sizing(self): 
        cash = self.get_cash()  # Get available cash
        last_price = self.get_last_price(self.symbol)  # Get the last price of the stock
        quantity = round(cash * self.cash_at_risk / last_price, 0)  # Calculate number of shares to buy/sell
        return cash, last_price, quantity  # Return cash, last price, and quantity

    # Method to get current date and the date three days prior
    def get_dates(self): 
        today = self.get_datetime()  # Get current date and time
        three_days_prior = today - Timedelta(days=3)  # Calculate date three days prior
        return today.strftime('%Y-%m-%d'), three_days_prior.strftime('%Y-%m-%d')  # Format dates as strings

    # Method to estimate sentiment from news headlines
    def get_sentiment(self): 
        today, three_days_prior = self.get_dates()  # Get current date and three days prior
        news = self.api.get_news(symbol=self.symbol, 
                                 start=three_days_prior, 
                                 end=today)  # Fetch news articles for the symbol within the date range
        news = [ev.__dict__["_raw"]["headline"] for ev in news]  # Extract headlines from news articles
        probability, sentiment = estimate_sentiment(news)  # Estimate sentiment and its probability
        return probability, sentiment  # Return the probability and sentiment

    # Core method executed on each trading iteration
    def on_trading_iteration(self):
        cash, last_price, quantity = self.position_sizing()  # Calculate position sizing
        probability, sentiment = self.get_sentiment()  # Get sentiment analysis results

        if cash > last_price:  # Check if there's enough cash to buy at least one share
            if sentiment == "positive" and probability > 0.999:  # Buy if sentiment is strongly positive
                if self.last_trade == "sell": 
                    self.sell_all()  # Close any existing sell positions
                order = self.create_order(
                    self.symbol, 
                    quantity, 
                    "buy", 
                    type="bracket",  # Use a bracket order for profit-taking and stop-loss
                    take_profit_price=last_price * 1.20,  # Set take profit at 20% above the current price
                    stop_loss_price=last_price * 0.95  # Set stop loss at 5% below the current price
                )
                self.submit_order(order)  # Submit the buy order
                self.last_trade = "buy"  # Update the last trade action to 'buy'
            elif sentiment == "negative" and probability > 0.999:  # Sell if sentiment is strongly negative
                if self.last_trade == "buy": 
                    self.sell_all()  # Close any existing buy positions
                order = self.create_order(
                    self.symbol, 
                    quantity, 
                    "sell", 
                    type="bracket",  # Use a bracket order for profit-taking and stop-loss
                    take_profit_price=last_price * 0.8,  # Set take profit at 20% below the current price
                    stop_loss_price=last_price * 1.05  # Set stop loss at 5% above the current price
                )
                self.submit_order(order)  # Submit the sell order
                self.last_trade = "sell"  # Update the last trade action to 'sell'

# Set up the backtesting environment
start_date = datetime(2023, 1, 1)  # Start date for backtesting
end_date = datetime(2024, 1, 1)  # End date for backtesting
broker = Alpaca(ALPACA_CREDS)  # Create a broker instance using Alpaca API credentials
strategy = MLTrader(name='mlstrat', broker=broker, 
                    parameters={"symbol": "SPY", 
                                "cash_at_risk": 0.5})  # Instantiate the custom strategy

# Run the backtest using Yahoo Finance data
strategy.backtest(
    YahooDataBacktesting, 
    start_date, 
    end_date, 
    parameters={"symbol": "SPY", "cash_at_risk": 0.5}
)
