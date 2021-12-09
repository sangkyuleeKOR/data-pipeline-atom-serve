
class MemoryDataRepository:

    def __init__(self):
        self.data_store = []
        self.meta_store = []

    def count_all(self):
        return len(self.data_store)

    def add_data(self, meta, data):
        self.meta_store.append(meta)
        self.data_store.append(data)

    def pick_data_by_count(self, count):
        if count > len(self.data_store):
            raise Exception("Can't pick more than current data size")
        meta_result = self.meta_store[:count]
        self.meta_store = self.meta_store[count:]
        data_result = self.data_store[:count]
        self.data_store = self.data_store[count:]
        return meta_result, data_result

