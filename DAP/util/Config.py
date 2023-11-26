import yaml
from pathlib import Path

class Config:

    def load_config(self):
        script_dir = Path(__file__).absolute().parent
        BASE_DIR = script_dir.parent.absolute()
        configPath = BASE_DIR / "config" / "config.yml"

        with open(configPath) as yml_file:
            config_file = yaml.load(yml_file, Loader=yaml.FullLoader)
            config_file['base_dir'] = str(BASE_DIR)

        return config_file