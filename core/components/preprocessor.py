import custom.custom_preprocessor as custom
from core.repository import MemoryDataRepository
from core.repository import MemoryCandidateDataRepository
import time

class PreProcessor:
    
    def __init__(self, config, push):
        self.config = config
        self.pre_size = config['preSize']
        self.parameter_list = config['parameterList']
        self.pre_temp_data = config['preTempData']
        self.push = push
        self.parameter_map = {key:i for i, key in enumerate(self.parameter_list)}
        self.data_repository = MemoryDataRepository()
        self.candidate_data_repository = MemoryCandidateDataRepository(self.__is_single_parameter(), len(self.parameter_list))

    def start(self, queue):
        while True:
            if not queue.empty():
                (meta, data) = queue.get()
                self.add_data(meta, data)
            else:
                time.sleep(0.01)

    def add_data(self, meta, data):
        if self.__is_single_parameter():
            self.candidate_data_repository.add_data(meta, data)
        else:
            data = data if isinstance(data, list) else [data]
            for param_name, _data in data:
                param_index = self.parameter_map[param_name]
                self.candidate_data_repository.add_data(meta, _data, param_index)

        if self.candidate_data_repository.is_candidate_complete():
            candidate_meta, candidate_data = self.candidate_data_repository.pick_first_data()
            self.data_repository.add_data(candidate_meta, candidate_data)
        
        if self.__is_ready_for_run():
            meta_parameters, data_parameters = self.data_repository.pick_data_by_count(self.pre_size)
            meta_parameters = meta_parameters[0] if self.pre_size == 1 else meta_parameters
            data_parameters = data_parameters[0] if self.pre_size == 1 else data_parameters
            custom.run(meta_parameters, data_parameters, push=self.push, debug=True)
            # custom.run(meta_parameters, data_parameters, push=self.push)

    def __is_single_parameter(self):
        return len(self.parameter_list) == 0

    def __is_ready_for_run(self):
        return self.data_repository.count_all() >= self.pre_size
         
