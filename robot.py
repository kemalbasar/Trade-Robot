import pandas as pd
import ftx
import ccxt
import time
import trade



data_frame : pd.DataFrame

class RobotA:

    def __init__(self, api_key, secret_key) -> None:

        self.mylist = ['XLM-PERP', 'XRP-PERP', 'DOGE-PERP']
        self.api_key = api_key
        self.secret_key = secret_key
        self.instance1 = self.login()
        self.instance2 = self.loginccxt()
        self.a = time.time()
        self.historical_prices = {}
        self.price_frame = self.grabhistory(5)
        self.length_of_frame = len(self.price_frame.columns)
        self.d = None

    def change_instrument(self):
        self.mylist= ('XLM-PERP', 'XRP-PERP', 'DOGE-PERP')

    def login(self):
        a = ftx.FtxClient(api_key=self.api_key,
                          api_secret=self.secret_key)
        return a

    def loginccxt(self):
        b = ccxt.ftx()
        b.apiKey = self.api_key
        b.secret = self.secret_key
        return b

    #pull historical prices from exchange data base before start trading.
    def grabhistory(self , period):
        pricedata = {}
        dictionaryoflistofopen = {}
        dictionaryoflistofclose = {}
        dictionaryoflistofhigh = {}
        dictionaryoflistoflow = {}


        self.a = self.a - self.a % (60 * period) - 1
        b = self.a - 30000 * period


        for symbol in trade.defult_pairs:

            dictionaryoflistofclose[symbol] = []
            dictionaryoflistofhigh[symbol] = []
            dictionaryoflistoflow[symbol] = []
            dictionaryoflistofopen[symbol] = []

            pricedata[symbol] = self.instance1.get_historical_data(market_name=str(symbol),
                                                                        resolution= period * 60,
                                                                        limit=500,
                                                                        start_time=b,
                                                                        end_time=self.a
                                                                        )
            print(symbol)

            for candle in pricedata[symbol]:
                dictionaryoflistofclose[symbol].append(candle['close'])
                dictionaryoflistofhigh[symbol].append(candle['high'])
                dictionaryoflistoflow[symbol].append(candle['low'])
                dictionaryoflistofopen[symbol].append(candle['open'])

        time = []
        for candle in pricedata[trade.defult_pairs[0]]:

         t = candle['startTime'][5:10]  + ' ' +  candle['startTime'][11:16]
         time.append(t)

        n = pd.DataFrame.from_dict(dictionaryoflistofopen, orient='index')
        m = pd.DataFrame.from_dict(dictionaryoflistofhigh, orient = 'index')
        k = pd.DataFrame.from_dict(dictionaryoflistoflow, orient = 'index')
        l = pd.DataFrame.from_dict(dictionaryoflistofclose, orient = 'index')

        pieces = {"open": n, "high": m, "low": k,"close":l}
        result = pd.concat(pieces)
        result1 = result.swaplevel(0, 1, axis = 0)
        result1 = result1.sort_index(axis=0,ascending = True)
        result1.set_axis(time, 'columns' , inplace = True)
        return result1
    
    
    #Pulling prices  after the end of period.
    def addcandle(self,i,period):

        list = []
        a = self.price_frame.index.get_level_values(0)
        a = a[::4]
        for symbol in (a):

         b = self.instance1.get_historical_data(market_name=str(symbol),
                                            resolution=period*60,
                                            limit=500,
                                            start_time=self.a + 1 + 60*i*period ,
                                            end_time=self.a + 300 + 60*i*period
                                            )
         #print(b)

         list.append(b[0]['close'])
         list.append(b[0]['high'])
         list.append(b[0]['low'])
         list.append(b[0]['open'])

        t = b[0]['startTime'][5:10]  + ' ' +  b[0]['startTime'][11:16]
        self.price_frame.insert(self.length_of_frame, t , list)


        self.length_of_frame = len(self.price_frame.columns)







