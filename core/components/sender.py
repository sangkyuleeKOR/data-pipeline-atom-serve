from queue import Queue
import custom.custom_sender as custom

class Sender:

    def __init__(self, config, push):
        self.config = config
        self.send_type = config['sendType']
        self.send_url = config['sendUrl']
        self.count = 0
        self.file_name = ''
        self.file_list = Queue()
        self.push=push

    def add_data(self, meta, data):
        self.select(data, meta)
       
    def select(self, data, meta):
        if self.send_type == 'mqtt':
            self.mqtt(data, meta)
        else:
            custom.run(meta, data, push=self.push)

    def mqtt(self, data, meta):
        print(meta, data)
             	
