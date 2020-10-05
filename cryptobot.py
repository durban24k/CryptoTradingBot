import websocket, numpy as np,json,pprint,talib


SOCKET="wss://stream.binance.com:9443/ws/ethusdt@kline_1m"

RSI_PERIOD=29
RSI_OVERBOUGHT=70
RSI_OVERSOLD=30
TRADE_SYMBOL='ETHUSD'
TRADE_QUANT=0.05

closes=[]
in_position=False

def on_open(ws):
     print('Connection Open')

def on_close(ws):
     print("Connection Closed")

def on_message(ws,message):
     global closes
     print("Message Received")
     json_message=json.loads(message)

     candle=json_message['k']
     is_candle_closed=candle['x']
     close=candle['c']
     pprint.pprint(close)

     if is_candle_closed:
          print(f"Candle closed at {close}".format())
          closes.append(float(close))
          print("Closes::")
          print(closes)

          if len(closes)>RSI_PERIOD:
               np_closes=np.array(closes)
               rsi=talib.RSI(np_closes,RSI_PERIOD)
               print("All RSIs calculated so far")
               print(rsi)
               last_rsi=rsi[-1]
               print(f'The current RSI is {last_rsi}'.format())

               if last_rsi>RSI_OVERBOUGHT:
                    if in_position:
                         print("SELL! SELL! SELL!")
                         # put binance sell logic here
                    else:
                         print("It is overbought:We don't own any position. Nothing to Sell")
               
               if last_rsi<RSI_OVERSOLD:
                    if in_position:
                         print("It is OVERSOLD, but you already own it. Nothing to Do!!")
                    else:
                         print("BUY! BUY! BUY!")
                         # put binance logic here

ws=websocket.WebSocketApp(SOCKET,on_open=on_open,on_close=on_close,on_message=on_message)
ws.run_forever()