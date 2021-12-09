
class MemoryCandidateDataRepository:

    def __init__(self, single_mode=False, param_count=1):
        self.data_store = []
        self.meta_store = []
        self.single_mode = single_mode
        self.param_count = param_count

    def __add_single_data(self, meta, data):
        self.meta_store.append(meta)
        self.data_store.append(data)

    def __add_multi_data(self, index, meta, data):
        is_stored = False
        for i, _data in enumerate(self.data_store):
            if _data[index] == None:
                _data[index] = data
                self.meta_store[i][index] = meta
                is_stored = True
                break
        
        if not is_stored:
            _meta, _data = self.__create_data()
            _meta[index] = meta
            _data[index] = data
            self.meta_store.append(_meta)
            self.data_store.append(_data)

    def __create_data(self):
        _meta = [None] * self.param_count
        _data = [None] * self.param_count
        return _meta, _data

    def add_data(self, meta, data, index=0):
        if self.single_mode:
            self.__add_single_data(meta, data)
        else:
            self.__add_multi_data(index, meta, data)

    def is_candidate_complete(self):
        if self.single_mode:
            return len(self.data_store) > 0
        else:
            return len(self.data_store) > 0 and not None in self.data_store[0]

    
    def pick_first_data(self):
        meta_result = self.meta_store[0]
        data_result = self.data_store[0]
        self.meta_store = self.meta_store[1:]
        self.data_store = self.data_store[1:]
        return meta_result, data_result
