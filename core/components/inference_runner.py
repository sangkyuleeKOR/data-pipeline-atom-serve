from threading import Thread
import custom.custom_inference_runner as custom

class InferenceRunner:

    def __init__(self, config, push):
        self.config = config
        self.batch_size = config['batchSize']
        self.wait_time = config['waitTime']
        self.inference_url = config['inferenceUrl']
        self.inference_type = config['inferenceType']
        self.infer_temp_data = config['inferTempData']
        self.data_store = []
        self.push = push
        self.meta_store = []
       
    def add_data(self, meta, data):
        self.data_store.append(data)
        self.meta_store.append(meta)
        if self.is_ready_for_inference():
            custom.run(self.meta_store, self.data_store, self.push)
            #p = Thread(target = custom.run, \
            #            args=(self.meta_store, self.data_store, self.push))
            #p.start()
            self.data_store = []
            self.meta_store = []

    def is_ready_for_inference(self):
        return len(self.data_store) == self.batch_size
