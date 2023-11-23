from model import XGBoost_Model as xgb
from model import Feature_Engineering as fe

class Model:

    def __init__(self, config_file):
        self._config_file = config_file
        self._model = None
    
    def _load_model(self):
        if(self._config_file['model']['model_algorithm'] == 'xgboost'):
            self._model = xgb.XGBoost_Model(self._config_file)
            self._model.load_model()
    
    def training(self):
        df = fe.Feature_Engineering(self._config_file).generate_features()
        self._model = xgb.XGBoost_Model(self._config_file)
        self._model.training(df)
    
    def inference(self, payload):
        self._load_model()
        return self._model.inference(payload)