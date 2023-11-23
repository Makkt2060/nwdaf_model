import pandas as pd
import logging
from xgboost import XGBClassifier
from sklearn.metrics import classification_report
from sklearn.model_selection import GridSearchCV

class XGBoost_Model:

    def __init__(self, config_file):
        self._config_file = config_file
        self._xgb_model = None

    def load_model(self):
        try:
            model_dir = self._config_file['model']['model_dir']
            logging.info(f'Loading xgboost model from {model_dir}')

            self._xgb_model = XGBClassifier(objective='binary:logistic', 
                                            enable_categorical=True, 
                                            random_state=self._config_file['model']['seed'])
            self._xgb_model.load_model(model_dir)
        
        except Exception as e:
            logging.exception(f'Failed to load the xgboost model, exception was {e}')
    
    def _train_test_split(self, df_ml):
        test_start_t = self._config_file['model']['test_start_t']
        df_ml_train = df_ml[df_ml['t'] < test_start_t].copy()
        df_ml_test = df_ml[df_ml['t'] >= test_start_t].copy()

        return df_ml_train, df_ml_test
    
    def _set_column_types(self, df_ml_train, df_ml_test):
        ml_columns = ['cell_id', 
              'cat_id', 
              'pe_id',
              'load',
              'last2_mean', 
              'per_change_last2', 
              'per_change_last3', 
              'per_change_last4', 
              'has_anomaly']

        df_ml_train = df_ml_train[ml_columns].copy()
        df_ml_test = df_ml_test[ml_columns].copy()

        categorical_features = ['cell_id', 'cat_id', 'pe_id']

        for categorical_feature in categorical_features:
            df_ml_train.loc[:, categorical_feature] = df_ml_train[categorical_feature].astype('category')
            df_ml_test.loc[:, categorical_feature] = df_ml_test[categorical_feature].astype('category')

        return df_ml_train, df_ml_test
    
    def _generate_X_y_data(self, df_ml_train, df_ml_test):
        target_feature = 'has_anomaly'
        features = list(df_ml_train.columns)
        features.remove(target_feature)

        X_train = df_ml_train[features]
        y_train = df_ml_train[target_feature]
        X_test = df_ml_test[features]
        y_test = df_ml_test[target_feature]

        return X_train, y_train, X_test, y_test
    
    def _fit_model(self, X_train, y_train):
        if self._config_file['model']['hyperparameter_optimization']['active']:
            # perform HPO
            logging.info('Performing hyperparameter optimization and cross validation for the xgboost model')
            xgb_model_cv = XGBClassifier(objective='binary:logistic', 
                                         enable_categorical=True, 
                                         random_state=self._config_file['model']['seed'])

            grid_search = GridSearchCV(
                estimator = xgb_model_cv,
                param_grid = self._config_file['model']['hyperparameter_optimization']['hyperparameter_optimization_parameters'],
                scoring = self._config_file['model']['hyperparameter_optimization']['scoring_metric'],
                n_jobs = self._config_file['model']['hyperparameter_optimization']['jobs'],
                cv = self._config_file['model']['hyperparameter_optimization']['cv'],
                verbose = True
            )

            grid_search.fit(X_train, y_train)
            xgb_model = grid_search.best_estimator_

        else:
            # fit single model
            logging.info('Training a single xgboost model')
            xgb_model = XGBClassifier(objective='binary:logistic', 
                                      enable_categorical=True, 
                                      random_state=self._config_file['model']['seed'],
                                      **self._config_file['model']['model_parameters'])
            
            xgb_model.fit(X_train, y_train)

        return xgb_model
    
    def _generate_model_metrics(self, xgb_model, X_test, y_test):
        logging.info('Generating metrics for the xgboost model')
        y_pred = xgb_model.predict(X_test)
        report = classification_report(y_test, y_pred)

        with open(self._config_file['model']['metrics_dir'], 'w') as f:
            f.write(report)

    def _save_model(self, xgb_model):
        logging.info('Saving the xgboost model')
        xgb_model.save_model(self._config_file['model']['model_dir'])

    def training(self, df_ml):
        try:
            logging.info('Starting training step for the xgboost model')

            df_ml_train, df_ml_test = self._train_test_split(df_ml)
            df_ml_train, df_ml_test = self._set_column_types(df_ml_train, df_ml_test)
            X_train, y_train, X_test, y_test = self._generate_X_y_data(df_ml_train, df_ml_test)
            self._xgb_model = self._fit_model(X_train, y_train)
            self._generate_model_metrics(self._xgb_model, X_test, y_test)
            self._save_model(self._xgb_model)
        
        except Exception as e:
            logging.exception(f'The training step for the xgboost model failed, exception was {e}')
    
    def inference(self, payload):
        try:
            logging.info(f'Trying to perform inference with payload {payload}')

            X_inference = pd.DataFrame({
                'cell_id': [int(payload['cell_id'])],
                'cat_id': [int(payload['cat_id'])],
                'pe_id': [int(payload['pe_id'])],
                'load': [float(payload['load'])],
                'last2_mean': [float(payload['last2_mean'])],
                'per_change_last2': [float(payload['per_change_last2'])],
                'per_change_last3': [float(payload['per_change_last3'])],
                'per_change_last4': [float(payload['per_change_last4'])]
            })

            y_pred = self._xgb_model.predict(X_inference)

            return y_pred[0]
        
        except Exception as e:
            logging.exception(f'Failed to perform inference, exception was {e}')
            
            return None