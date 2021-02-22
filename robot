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
        self.Start_Time = time.time()
        self.historical_prices = {}
        self.price_frame = self.grabhistory()
        self.length_of_frame = len(self.price_frame.columns)
        self.i=0


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

    def checkstatus(self):

        print(
            "Trade Session has just started at " + self.Start_Time.strftime("%c")) if self.instance1.get_account_info() \
            else print('wrong keys')


    def grabhistory(self):
        pricedata = {}
        dictionaryoflistoftime = {}
        dictionaryoflistofopen = {}
        dictionaryoflistofclose = {}
        dictionaryoflistofhigh = {}
        dictionaryoflistoflow = {}
        dictionaryoflistofema = {}
        dictionaryoflistofrsi = {}



        for symbol in trade.defult_pairs:
            self.a=float(time.time())
            b=self.a-126000
            dictionaryoflistofclose[symbol] = []
            dictionaryoflistofhigh[symbol] = []
            dictionaryoflistoflow[symbol] = []
            dictionaryoflistofopen[symbol] = []
            dictionaryoflistoftime[symbol] = []


            pricedata[symbol] = self.instance1.get_historical_data(market_name=str(symbol),
                                                                        resolution=60,
                                                                        limit=500,
                                                                        start_time=b,
                                                                        end_time=self.a
                                                                        )
            print(symbol)

            for candle in pricedata[symbol]:
                dictionaryoflistofclose[symbol].append(candle['close'])
                dictionaryoflistofhigh[symbol].append(candle['high'])
                dictionaryoflistoflow[symbol].append(candle['low'])
                dictionaryoflistoftime[symbol].append(candle['time'])
                dictionaryoflistofopen[symbol].append(candle['open'])

        n = pd.DataFrame.from_dict(dictionaryoflistofopen, orient='index')
        m = pd.DataFrame.from_dict(dictionaryoflistofhigh, orient = 'index')
        k = pd.DataFrame.from_dict(dictionaryoflistoflow, orient = 'index')
        l = pd.DataFrame.from_dict(dictionaryoflistofclose, orient = 'index')


        pieces = {"open": n, "high": m, "low": k,"close":l}
        result = pd.concat(pieces)
        result1 = result.swaplevel(0, 1, axis=0)
        result1 = result1.sort_index(axis=0,ascending=True)
        return result1


    def addcandle(self):

        self.price_frame[self.length_of_frame] = 0
        for symbol in ('XLM-PERP', 'XRP-PERP', 'DOGE-PERP'):

         b = self.instance1.get_historical_data(market_name=str(symbol),
                                            resolution=60,
                                            limit=500,
                                            start_time=self.Start_Time + 60*self.i,
                                            end_time=self.Start_Time + 60*(self.i+1)
                                            )
         #print(b)

         self.price_frame.loc[(symbol,'close'),self.length_of_frame] = b[0]['close']
         self.price_frame.loc[(symbol,'high'),self.length_of_frame] = b[0]['high']
         self.price_frame.loc[(symbol,'low'),self.length_of_frame] = b[0]['low']
         self.price_frame.loc[(symbol,'open'),self.length_of_frame] = b[0]['open']

        self.length_of_frame = len(self.price_frame.columns)




