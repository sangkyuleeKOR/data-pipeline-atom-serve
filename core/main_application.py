from .components import DataParser, PreProcessor, InferenceRunner, PostProcessor, DataTransmitter, Sender
import json
from multiprocessing import Process, Queue

class MainApplication:

    def test_tempo(self):
        queue = Queue()
        config = self.configuration()
        transmitter = DataTransmitter()

        collector = DataParser(config, lambda meta, data: transmitter.push({'type': 'parse', 'meta': meta, 'data': data}), queue)
        pre_processor = PreProcessor(config, lambda meta, data: transmitter.push({'type': 'preprocess', 'meta': meta, 'data': data}))
        inference_runner = InferenceRunner(config, lambda meta, data: transmitter.push({'type': 'inference', 'meta': meta, 'data': data}))
        post_processor = PostProcessor(config, lambda meta, data: transmitter.push({'type': 'postprocess', 'meta': meta, 'data': data}))
        sender = Sender(config, lambda meta, data: print(meta, data))
        
        transmitter.observe('collect', pre_processor)
        transmitter.observe('preprocess', inference_runner)
        transmitter.observe('inference', post_processor)
        transmitter.observe('postprocess', sender)
        
        p = Process(target=collector.start, args=())
        p.start()
        pre_processor.start(queue)


        # from datetime import datetime
        # import time
        #queue.put(({'type': 5, 'time': datetime.now()}, data))
        #transmitter.push({'type': 'collect', 'meta': {'type': 5, 'time': datetime.now()}, 'data': data})
        #time.sleep(0.4)
        
        #transmitter.push({'type': 'collect', 'meta': {'type': 5, 'time': datetime.now()}, 'data': data})
        #time.sleep(0.4)
        #transmitter.push({'type': 'collect', 'meta': {'type': 5, 'time': datetime.now()}, 'data': data})
        #time.sleep(0.4)
        #transmitter.push({'type': 'collect', 'meta': {'type': 5, 'time': datetime.now()}, 'data': data})
        #time.sleep(0.4)
        #transmitter.push({'type': 'collect', 'meta': {'type': 5, 'time': datetime.now()}, 'data': data})
        #time.sleep(0.4)
        #transmitter.push({'type': 'collect', 'meta': {'type': 5, 'time': datetime.now()}, 'data': data})
        #time.sleep(0.4)
        #transmitter.push({'type': 'collect', 'meta': {'type': 5, 'time': datetime.now()}, 'data': data})
        
        #time.sleep(20)

    def start(self):
        config = self.configuration()

        transmitter = DataTransmitter()
        parser = DataParser(config, lambda meta, data: transmitter.push({'type': 'parse', 'meta': meta, 'data': data}))
        pre_processor = PreProcessor(config, lambda meta, data: transmitter.push({'type': 'preprocess', 'meta': meta, 'data': data}))
        inference_runner = InferenceRunner(config, lambda meta, data: transmitter.push({'type': 'inference', 'meta': meta, 'data': data}))
        post_processor = PostProcessor(config, lambda meta, data: transmitter.push({'type': 'postprocess', 'meta':meta, 'data': data}))
        sender = Sender(config, lambda meta, data: print(meta, data))
        
        transmitter.observe('collect', parser)
        transmitter.observe('parse', pre_processor)
        transmitter.observe('preprocess', inference_runner)
        transmitter.observe('inference', post_processor)
        transmitter.observe('postprocess', sender)

        parser.start()


    def configuration(self):
        with open('core/config.json', 'r') as fd:
            config = json.loads(fd.read())
        return config
