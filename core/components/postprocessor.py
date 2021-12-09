import custom.custom_postprocessor as custom

class PostProcessor:

    def __init__(self, config, push):
        self.push = push
        self.post_size = config['postSize']
        self.post_temp_data = config['postTempData']
        self.data_store = []
        self.meta_store = []

    def add_data(self, meta, data):
        self.data_store.append(data)
        self.meta_store.append(meta)
        if len(self.meta_store) == self.post_size: 
            custom.run(self.meta_store, self.data_store, push=self.push) 
            self.data_store = []
            self.meta_store = []
