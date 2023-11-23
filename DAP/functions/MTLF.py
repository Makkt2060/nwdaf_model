from model import Model as m


class MTLF:

    def __init__(self, config_file):
        self._config_file = config_file

    def training(self):
        model = m.Model(self._config_file)
        model.training()