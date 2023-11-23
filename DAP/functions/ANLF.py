from model import Model as m

class ANLF:

    def __init__(self, config_file):
        self._config_file = config_file

    def inference(self, payload):
        model = m.Model(self._config_file)
        
        return model.inference(payload)