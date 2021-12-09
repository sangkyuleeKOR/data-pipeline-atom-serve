from .plc import PLCConnector
from threading import Lock
from datetime import datetime
import time

class PlcApi:

    def __init__(self, connector):
        self.connector = connector
        self.requests = {}
        self.lock = Lock()
    
    def __del__(self):
        PLCConnector.close(self.connector)

    def get_value(self, read_size=1, headdevice='D701'):
        return PLCConnector.get_value(self.connector, read_size, headdevice)

    def send_message(self, value, key):
        PLCConnector.send_message(self.connector, value, key)

    def send_result(self, request_id, value, sender_type):
        if request_id in self.requests:
            with self.lock:
                print('Delete plc request', request_id, 'sender_type : ', sender_type, '\n')
                del self.requests[request_id]
        else:
            with self.lock:
                self.requests[request_id] = True
            print('Send plc request', request_id, '/ value:', value,'/ current time:', datetime.now(), '/ sender_type', sender_type)
            PLCConnector.send_message(self.connector, value, "M751M752")
            time.sleep(0.1)
            PLCConnector.send_message(self.connector, 0, "M754")
