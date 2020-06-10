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

        self.send_on_req("Hello Server")

        print("Client init successfully")


    """
    SEND AND RECEIVE FUNCTIONS
    """

    # On envoie une requete et on attend un ACK
    def send_on_req(self, data):
        try: 
            self.reqSocket.send_string(data)
            message = self.reqSocket.recv_string()
            return message
        except: 
            print("Waiting from MT4...")


    # On receptionne un message sur la pullSocket
    def receive_on_pull(self):
        try:
            message = self.pullSocket.recv(flags = zmq.NOBLOCK)
            return message
        except:
            print("Waiting from MT4...")


    """
    ORDER FUNCTIONS
    """

    def buy_order(self, symbol, stop_loss, take_profit):
        self.send_on_req(
            "TRADE|OPEN|0|" +
            str(symbol) + "|" +
            str(stop_loss) + "|" +
            str(take_profit)
        )

    def sell_order(self, symbol, stop_loss, take_profit):
        self.send_on_req(
            "TRADE|OPEN|1|" +
            str(symbol) + "|" +
            str(stop_loss) + "|" + 
            str(take_profit)
        )
        
    def close_buy_order(self):
        self.send_on_req(
            "TRADE|CLOSE|0"
        )
    
    def close_sell_order(self):
        self.send_on_req(
            "TRADE|CLOSE|1"
        )
        