import custom.custom_collector as custom

class DataParser:

    def __init__(self, config, push, queue=None): 
        self.is_run = True
        self.collector_type = config['collectorType']
        self.config = config
        self.push = push
        self.queue = queue
    
    def __del__(self):
       print('DataParser destroy')
       
    def start(self):
        print('start core collector')
        if self.collector_type == 'mqtt':
            self.mqtt()
        else:
           custom.test_run(push=self.push, queue=self.queue)
            # custom.run(push=self.push, queue=self.queue)

    def mqtt(self):
        pass
