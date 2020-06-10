import zmq
import time
import numpy as np

class Client(): 

    """
    Setup -> MT4 Connector
    """
    def __init__(
        self,
        _ClientID = 'PYTHON_CLIENT',
        _host = '192.168.1.22', 
        _protocol = 'tcp',
        _REQ_PORT = 5555,
        _PULL_PORT = 5556
    ):

        print("Client init...")

        # Create ZMQ Context
        self.context = zmq.Context()

        # Create REQ Socket
        self.reqSocket = self.context.socket(zmq.REQ)
        self.reqSocket.connect(
            _protocol + "://" + _host + ":" + str(_REQ_PORT)
        )

        # Create PULL Socket
        self.pullSocket = self.context.socket(zmq.PULL)
        self.pullSocket.connect(
            _protocol + "://" + _host + ":" + str(_PULL_PORT)
        )

        self.remote_send(self.reqSocket, "Hello World !")

        print("Client init successfully")


    def remote_send(self, socket, data):
        try: 
            socket.send_string(data)
            msg_send = socket.recv_string()
            print(msg_send)
        except: 
            print("Waiting for PUSH from MT4...")


    def remote_pull(self, socket):
        try:
            msg_pull = socket.recv(flags = zmq.NOBLOCK)
            return msg_pull
        except:
            print("Waiting for PUSH from MT4...")


    def get_data(self, symbol, timeframe, start_bar, end_bar):
        
        # On compose notre message (data) et on l'envoie
        self.data = "DATA|" + symbol + "|" + "PERIOD_" + timeframe + "|" + str(start_bar) + "|" + str(end_bar + 1)
        self.remote_send(self.reqSocket, self.data)

        # On recupere la réponse
        prices = self.remote_pull(self.pullSocket)
        prices_str = str(prices)
        
        price_lst = prices_str.split(sep='|')[1:-1]
        price_lst = [float(i) for i in price_lst]
        price_lst = price_lst[::1]
        
        price_arr = np.array(price_lst)
        return price_arr

    
    def buy_order(self, symbol, stop_loss, take_profit):
        self.buy = "TRADE|OPEN|0|" + str(symbol) + "|" + str(stop_loss) + "|" + str(take_profit)
        self.remote_send(self.reqSocket, self.buy)
        reply = self.remote_pull(self.pullSocket)
        return reply

    def sell_order(self, symbol, stop_loss, take_profit):
        self.buy = "TRADE|OPEN|1|" + str(symbol) + "|" + str(stop_loss) + "|" + str(take_profit)
        self.remote_send(self.reqSocket, self.buy)
        reply = self.remote_pull(self.pullSocket)
        return reply

    def close_buy_order(self):
        self.close_buy = "TRADE|CLOSE|0"
        self.remote_send(self.reqSocket, self.close_buy)
        reply = self.remote_pull(self.pullSocket)
        return reply
    
    def close_sell_order(self):
        self.close_sell = "TRADE|CLOSE|1"
        self.remote_send(self.reqSocket, self.close_sell)
        reply = self.remote_pull(self.pullSocket)
        return reply
