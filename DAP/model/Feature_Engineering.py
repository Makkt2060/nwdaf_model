import pandas as pd
import logging

class Feature_Engineering:

    def __init__(self, config_file):
        self._config_file = config_file

    def _load_data(self):
        return pd.read_csv(self._config_file['model']['data_dir'])
    
    def _compute_mean(self, df_raw, cell_id, cat_id, pe_id, num_dt):
        df_temp = df_raw[(df_raw['cell_id'] == cell_id) & (df_raw['cat_id'] == cat_id) & (df_raw['pe_id'] == pe_id)].copy()

        column_name = f'last{num_dt}_mean'
        df_temp[column_name] = df_temp['load'].rolling(window=num_dt, closed='left').mean()

        return df_temp
    
    def _compute_single_per_change(self, t, dt, ndt):
        d1 = t - dt
        d2 = t - ndt
        
        return (d1 / d2) - 1
    
    def _compute_per_change(self, df_raw, cell_id, cat_id, pe_id, num_dt):
        df_temp = df_raw[(df_raw['cell_id'] == cell_id) & (df_raw['cat_id'] == cat_id) & (df_raw['pe_id'] == pe_id)].copy()
        
        column_name = f'per_change_last{num_dt}'
        df_temp[column_name] = df_temp['load'].rolling(window=num_dt+1).apply(lambda x: self._compute_single_per_change(x.iloc[num_dt], x.iloc[num_dt-1], x.iloc[0]))

        return df_temp

    def generate_features(self):
        try:
            logging.info('Performing the feature engineering process')
            df = self._load_data()

            cell_id_list = df['cell_id'].unique()
            cat_id_list = df['cat_id'].unique()
            pe_id_list = df['pe_id'].unique()
            df_fe_list = []

            # generate the features
            for cell_id in cell_id_list:
                for cat_id in cat_id_list:
                    for pe_id in pe_id_list:
                        # lastn_mean 
                        df_fe = self._compute_mean(df_raw=df, cell_id=cell_id, cat_id=cat_id, pe_id=pe_id, num_dt=2)

                        # per_change_lastn
                        for n in [2,3,4]:
                            df_per_change = self._compute_per_change(df_raw=df, cell_id=cell_id, cat_id=cat_id, pe_id=pe_id, num_dt=n)
                            df_fe = df_fe.merge(df_per_change, how='inner', on=['t', 'cell_id', 'cat_id', 'pe_id', 'load', 'has_anomaly'])

                        # append to the list
                        df_fe_list.append(df_fe)

            # concat all the dfs
            df_ml = pd.concat(df_fe_list)

            # assert the number of lines
            len_df_raw = len(df)
            len_df_ml = len(df_ml)

            assert len_df_raw == len_df_ml

            df_ml = df_ml.dropna()

            return df_ml
        
        except AssertionError as ae:
            logging.exception(f'The feature engineering step generated a processed dataframe with fewer rows than the original one')

        except Exception as e:
            logging.exception(f'An exception occurred during the feature engineering process, exception was {e}')

        return None