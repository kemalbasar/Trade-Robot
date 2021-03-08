#importing package
#importing ftx and ccxt , these are packages for connecting and manupulating exchange account.
#ccxt can be used with most of the exchanges , ftx is for only ftx exchange.
#we will use both

import time
from indicators import CheckSignal
import trade

uniform_resources='https://ftx.com/api/'
execute = CheckSignal()
execute.create_market_cop()
execute.create_trade_agent()
execute.trade_agent.create_agent()
execute.trade_agent.get_balance()
execute.trade_agent.check_positions()
fills = execute.marketcop.instance1.get_fills()


for i in range(99999):
 trade_starting_time = int(time.time())

 execute.trade_agent.check_fills()

 print('available pairs')
 print(trade.available_pairs)
 print('\n')
 print('long positions')
 print(trade.traded_pairs_long)
 print('\n')
 print('short positions')
 print(trade.traded_pairs_short)



 execute.ema_setter()
 execute.rsi()

 for symbol in trade.available_pairs: execute.trend(symbol)

 for symbol in trade.traded_pairs_long:
        if  execute.D[symbol]['rsi'][-1] > 70:
            execute.trade_agent.close_position(symbol,'sell')

 for symbol in trade.traded_pairs_short:

        if execute.D[symbol]['rsi'][-1] < 30:

         execute.trade_agent.close_position(symbol,'buy')

 print('sleeping')
 print('\n')

 p = execute.marketcop.a + 300 + 300*i +1  - time.time()
 time.sleep(p)
 print('slept %f'%p)

 execute.marketcop.addcandle(i,5)

 print('\n')





