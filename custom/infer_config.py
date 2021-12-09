class Config(object):
    def __init__(self, config_dict):
        for key, val in config_dict.items():
            self.__setattr__(key, val)

    def copy(self, new_config_dict={}):
        ret = Config(vars(self))
        for key, val in new_config_dict.items():
            ret.__setattr__(key, val)

        return ret

    def replace(self, new_config_dict):
        if isinstance(new_config_dict, Config):
            new_config_dict = vars(new_config_dict)

        for key, val in new_config_dict.items():
            self.__setattr__(key, val)
    
    def print(self):
        for k, v in vars(self).items():
            print(k,'=',v)

infer_config = Config(
    {
        'cut_model_path': 'custom/cut_model.ckpt',
        'dot_model_path': 'custom/dot_model.ckpt',
        'dot_result_path': '/app/inference_result/',
        'dot_save_path': '/app/dot_result/',
        'cut_save_path':'/app/shortcut_result/',
        ### mode:0 cut/dot both
        ### mode:1 dot
        ### mode:2 cut
        'mode': 1,
        'save_img': True,
        'save_json': True,
        'dot_score': 0.9,
        'dot_pixels': 5
    }
)

