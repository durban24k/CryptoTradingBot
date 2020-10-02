import websocket, numpy,json,pprint


SOCKET="wss://stream.binance.com:9443/ws/ethusdt@kline_1m"
SYMBOL="ETHUSDT"

def on_open(ws):
     print('Connection Open')

def on_close(ws):
     print("Connection Closed")

def on_message(ws,message):
     print("Message Received")
     json_message=json.loads(message)
     pprint.pprint(json_message)

     candle=json_message['k']
     is_candle_closed=candle['x']
     close=candle['c']

     if is_candle_closed:
          print(f"Candle closed at {close}".format())

ws=websocket.WebSocketApp(SOCKET,on_open=on_open,on_close=on_close,on_message=on_message)
ws.run_forever()