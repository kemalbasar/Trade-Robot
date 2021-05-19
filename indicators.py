import pandas as pd
from trade import Trade
import trade
from robot import RobotA

APIKEY = '*****'
SECRETKEY = '*****'




class CheckSignal():

  def __init__(self):
    self.indicators_frame: pd.DataFrame
    self.trade_agent:Trade
    self.side = ['long', 'short']
    self.last_close_price = float(0.000000)
    self.marketcop: RobotA
    self.D = dict.fromkeys(trade.defult_pairs)
    for symbol in trade.defult_pairs:
        self.D[symbol] = {'ema5': [], 'ema10': [], 'ema20': [], 'rsi': []}
    self.ema_gain = {'DOGE-PERP': [],'XRP-PERP': [],'XLM-PERP': []}
    self.ema_loss = {'DOGE-PERP': [],'XRP-PERP': [],'XLM-PERP': []}


  def create_market_cop(self):

      self.marketcop = RobotA(APIKEY,SECRETKEY)

  def create_trade_agent(self):

      self.trade_agent = Trade()

  #ema is calculated in this method which takes input as price data , time period and previus ema datas , 
  def ema(self,data,ema_list,period):
      if len(ema_list) == 0 :
          ema_list.append(data[0])
          lenx=len(data)-1
      else: lenx=len(data)-1

      x=0
      multiplier = (2 / ((period) + 1))

      while  x<lenx :
         EMA = ((data[x+1] - ema_list[x]) * multiplier + ema_list[x])
         ema_list.append(EMA)
         x = x + 1
      a=ema_list[-1]
      ema_list.clear()
      ema_list.append(a)

      return a

  #Method which set ema values with using ema function.
  def ema_setter(self):
    
      for symbol in trade.defult_pairs:
        if len(self.D[symbol]['ema5']) == 0:
         a = self.marketcop.price_frame.loc[symbol, 'close']
         self.D[symbol]['ema5'].append(self.ema(data=a, ema_list=[], period=5))
         self.D[symbol]['ema10'].append(self.ema(data=a, ema_list=[], period=10))
         self.D[symbol]['ema20'].append(self.ema(data=a, ema_list=[], period=20))
        else:
         b = self.marketcop.price_frame.loc[symbol,'close']
         a = [b[self.marketcop.length_of_frame-2] , b[self.marketcop.length_of_frame-1]]
         self.D[symbol]['ema5'].append(self.ema(data=a, ema_list=[self.D[symbol]['ema5'][-1]], period=5))
         self.D[symbol]['ema10'].append(self.ema(data=a, ema_list=[self.D[symbol]['ema10'][-1]], period=10))
         self.D[symbol]['ema20'].append(self.ema(data=a, ema_list=[self.D[symbol]['ema20'][-1]], period=20))
  
  #Method whic calculates rsi data.
  def rsi(self):

    for symbol in trade.defult_pairs:
        rsi_list_of_gain = []
        rsi_list_of_loss = []
        tpfc = self.marketcop.price_frame.loc[symbol, 'close']
        tpfo = self.marketcop.price_frame.loc[symbol, 'open']

        if len(self.D[symbol]['rsi']) == 0:
            None
        else:
            tpfc = [tpfc[self.marketcop.length_of_frame-2], tpfc[self.marketcop.length_of_frame-1]]
            tpfo = [tpfo[self.marketcop.length_of_frame-2], tpfo[self.marketcop.length_of_frame-1]]
        c = len(tpfc)

        for i in range(c - 1):
            if tpfc[c - i - 1] > tpfo[c - i - 1]:
                a = tpfc[c - i - 1] - tpfo[c - i - 1]
            else:
                a = 0
            rsi_list_of_gain.insert(0,a)

        for i in range(c - 1):
            if tpfc[c - i - 1] < tpfo[c - i - 1]:
                a = tpfo[c - i - 1] - tpfc[c - i - 1]
            else:
                a = 0
            rsi_list_of_loss.insert(0,a)

        self.ema_gain[symbol][0] = self.ema(data=rsi_list_of_gain, ema_list=self.ema_gain[symbol], period=14)
        self.ema_loss[symbol][0] = self.ema(data=rsi_list_of_loss, ema_list=self.ema_loss[symbol], period=14)

        RS = self.ema_gain[symbol][0] / self.ema_loss[symbol][0]
        RSI = 100 - 100 / (1 + RS)
        self.D[symbol]['rsi'].append(RSI)


  #Method which uses ema and rsi data for creating trade signal.
  def trend(self,symbol):

        five=self.D[symbol]['ema5']
        ten=self.D[symbol]['ema10']
        tweny=self.D[symbol]['ema20']
        
        if (five > ten) & (ten > tweny):

          print('OK: Trend going UP ,CheckingRSI\n')
          print('\n')

           if self.D[symbol]['rsi'][-1] < 70:
            self.trade_agent.execution(symbol,'buy')
            print('RSI is not overbougt.Creating trade.. \n')
            print('\n')

        elif (five < ten) & (ten < tweny):


          print('OK: Trend going DOWN,CheckingRSI\n')
          print('\n')
          
           if self.D[symbol]['rsi'][-1] > 30:
            print('RSI is not oversold.Creating trade.. \n')
            self.trade_agent.execution(symbol,'sell')
            print('\n')

        else:
            print('Trend not clear, waiting...\n')
            print('\n')


























