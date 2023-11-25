import yaml

class Config:

    def load_config(self):
        with open('./DAP/config/config.yml') as yml_file:
            config_file = yaml.load(yml_file, Loader=yaml.FullLoader)

        return config_file