from AlgorithmImports import *

"""
This is a strategy that buys at 12pm and closes the position at 2pm if the 10am and 11am candles are green.
It sells at 12pm and closes the position at 2pm if the 10am and 11am candles are red.
The idea is that the first 2 hours of the London session have predictive power over the rest of the day given there are
major news releases.
This Strategy shows potential. It needs optimization. A few suggestions for optimization.
1) Do not trade pairs that have a correlation greater than 60%.
2) Do not place trades on days when there is 3 bull data.
A few more will come with time. I couldn't backtest from 2010 to 2023 because the data points
exceeded the 10,000 data point limit for the free tier. I need a paid tier to get on with this.
"""

class MyAlgorithm(QCAlgorithm):

    def Initialize(self):
        # Set the start and end dates for the backtest
        self.SetStartDate(2010, 1, 1)
        self.SetCash(100000)
        
        # Set Brokerage Model
        #self.SetBrokerageModel(BrokerageName.InteractiveBrokersBrokerage, AccountType.Margin)

        # Define the currency pairs to trade
        self.currency_pairs = ["EURUSD", "GBPUSD", "AUDUSD", "NZDUSD", "USDCAD", "USDJPY", "USDCHF", "EURGBP",
                               "EURJPY", "EURCHF", "EURAUD", "EURCAD", "EURNZD", "GBPJPY", "GBPCAD", "GBPCHF",
                               "CHFJPY", "AUDCAD", "AUDNZD", "AUDCHF", "AUDJPY", "NZDJPY", "NZDCHF", "NZDCAD"]
        
        # Add Forex data for each currency pair with the resolution of one minute
        for symbol in self.currency_pairs:
            self.AddForex(symbol, Resolution.Minute).Symbol
        
        # Set the time zone to Kampala time
        self.SetTimeZone("Africa/Kampala")
        
        # Define the schedule for the algorithm
        self.Schedule.On(self.DateRules.EveryDay(), self.TimeRules.At(12, 0), self.Trade)
        self.Schedule.On(self.DateRules.EveryDay(), self.TimeRules.At(14, 0), self.Close)
        
    def Trade(self):
        # Check if the 10:00 AM and 11:00 AM candles are green or red
        for symbol in self.currency_pairs:
            history = list(self.History(QuoteBar, symbol, timedelta(hours = 1)))
            if len(history) >= 2:
                # Get the candles at 10:00 AM and 11:00 AM
                candle_10am = history[-2]
                candle_11am = history[-1]
                
                # Buy or short based on the color of the candles
                if self.IsGreenCandle(candle_10am) and self.IsGreenCandle(candle_11am):
                    # Buy 5 units of the currency pair at the current market price
                    self.MarketOrder(symbol, 5)
                elif not self.IsGreenCandle(candle_10am) and not self.IsGreenCandle(candle_11am):
                    # Short 5 units of the currency pair at the current market price
                    self.MarketOrder(symbol, -5)
        
    def Close(self):
        # Close all holdings of the currency pairs at the current market price
        for symbol in self.currency_pairs:      
            self.Liquidate(symbol)
        
    def IsGreenCandle(self, candle):
        # Check if the candle is green
        return candle[0] > candle[1]
