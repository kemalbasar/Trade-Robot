import ftx
import time

defult_pairs = ['XLM-PERP', 'XRP-PERP', 'DOGE-PERP']
available_pairs = ['XLM-PERP', 'XRP-PERP', 'DOGE-PERP']
traded_pairs_long = []
traded_pairs_short = []



class Trade():

    def __init__(self):
        self.api_key = 'QMP9IOD3oZ_nscanB1C9p7Shcj4hGdGHT44DfN-2'
        self.secret_key = '-gGJhztTh9NedfuY8noTeYXnjEnMBo1HxICR4Ixk'
        self.agent = None
        self.balance = None
        self.F = dict.fromkeys(defult_pairs)
        for symbol in defult_pairs:
            self.F[symbol] = {'size': 0, 'id': 0}

    def create_agent(self):

        self.agent = ftx.FtxClient(api_key=self.api_key, api_secret=self.secret_key)

    def get_balance(self):

        a=self.agent.get_balances()
        for i in range(4):
         if a[i]['total'] > 10 :
             self.balance = a[i]['total']
             break

    def execution(self,instrument: str, side: str):

        if side == 'buy' : a = 'bids'
        elif side == 'sell' : a = 'asks'
        else : a = None
        price = self.agent.get_orderbook(instrument, 1)
        price = price[a][0][0]

        quantity = self.balance/(3*price)
        quantity = format(quantity, '.5f')
        self.F[instrument]['size'] = quantity


        id = self.agent.place_order(instrument, side, price, quantity)['id']
        time.sleep(15)

        while int(self.agent.get_position(instrument)['openSize']) == 0:
         time.sleep(15)
         price = self.agent.get_orderbook(instrument, 1)
         price = price[a][0][0]
         id = self.agent.modify_order(existing_order_id = id , price = price )['id']


        if side=='buy':

         b='bought'
         self.F[instrument]['id'] = self.agent.place_conditional_order(instrument , side = 'sell' , size = quantity , limit_price = price - price*0.95/100 ,trigger_price = price - price * 0.95 / 100, type = 'stop' , reduce_only = True )

        elif side == 'sell':

         b='sold'
         self.F[instrument]['id'] = self.agent.place_conditional_order(instrument, side='buy', size = quantity, trigger_price = price + price * 0.95 / 100, limit_price = price + price * 0.95 / 100, type='stop' , reduce_only = True)


        else: b = None

        print('%s %s has just %s at %.2f'%(quantity,instrument,b,price))

        if side == 'buy' :
            traded_pairs_long.append(instrument)
            available_pairs.remove(instrument)
        elif side == 'sell' :
            traded_pairs_short.append(instrument)
            available_pairs.remove(instrument)
        print(traded_pairs_long,traded_pairs_short,available_pairs)

    def close_position(self,symbolclose: str,sideclose: str):

        price = self.agent.get_orderbook(symbolclose, 1)
        if sideclose == 'buy' :
            a = 'asks'
        elif sideclose == 'sell' :
            a = 'bids'
        else:
            a = None
        price=price[a][0][0]

        id = self.agent.place_order(symbolclose, sideclose, price, self.F[symbolclose]['size'],reduce_only=True)['id']

        while (self.agent.get_position(symbolclose)['openSize'] != 0):
         time.sleep(30)
         price = self.agent.get_orderbook(symbolclose, 1)
         price = price[a][0][0]
         id = self.agent.modify_order(id = id , price = price )['id']

        if sideclose=='buy': a='short'
        elif sideclose=='sell': a='long'
        else: a = None
        print('%s position of %s has just closed at %.2f'%(a,symbolclose,price))


        if sideclose == 'buy':
            traded_pairs_short.remove(symbolclose)
            available_pairs.append(symbolclose)

        elif sideclose == 'sell':
            traded_pairs_long.remove(symbolclose)
            available_pairs.append(symbolclose)

    def check_fills(self):

     for symbol in traded_pairs_short:
      for k in range(3):
        if self.F[symbol]['id'] == self.agent.get_fills()[k]['orderId']:
            traded_pairs_short.remove(symbol)
            available_pairs.append(symbol)
            print('short position of %s has just closed at %.2f' % (symbol,self.agent.get_fills[k]['price']))

     for symbol in traded_pairs_long:
      for k in range(3):
        if self.F[symbol]['id'] == self.agent.get_fills()[k]['orderId']:
            traded_pairs_long.remove(symbol)
            available_pairs.append(symbol)
            print('long position of %s has just closed at %.2f' % (symbol, self.agent.get_fills[k]['price']))

    def check_positions(self):
        a = self.agent.get_positions()
        for i in range(len(a)):
            if a[i]['openSize'] != 0:
                if a[i]['side'] == 'sell':
                 traded_pairs_short.append(a[i]['future'])
                 available_pairs.remove(a[i]['future'])
                 self.F[a[i]['future']]['size'] = a[i]['openSize']
                 self.close_position(a[i]['future'],'buy')

                elif a[i]['side'] == 'buy' :
                 traded_pairs_long.append(a[i]['future'])
                 available_pairs.remove(a[i]['future'])
                 self.F[a[i]['future']]['size'] = a[i]['openSize']
                 self.close_position(a[i]['future'],'sell')

    def cancel_order(self,id):

        self.agent.cancel_order(id)
        print('order canceled')

