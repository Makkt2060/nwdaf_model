from util import Config as cfg 
from util import Log as log
import logging
import json
from functions import MTLF as mtlf
from functions import ANLF as anlf
from flask import Flask, request

app = Flask(__name__)

class Main:

    @app.route('/', methods=['GET', 'POST'])
    def parser():
        config_file = cfg.Config().load_config()
        data = {}

        # payload = {
        #     'cell_id': 2,
        #     'cat_id': 2,
        #     'pe_id': 4,
        #     'load': 5.976979,
        #     'last2_mean': 5.981692,
        #     'per_change_last2': 0.402706,
        #     'per_change_last3': -1.985990,
        #     'per_change_last4': -3.211737
        # }

        # logging.info('Requesting inference service from ANLF')
        # inference_result = anlf.ANLF(config_file).inference(payload)
        # data['data'] = str(inference_result)
        # print(f'The inference result is {inference_result}')

        # logging.info('Requesting training service from MTLF')
        # mtlf.MTLF(config_file).training()
        # data['data'] = 'training finish'

        if request.method == 'POST':
            data = request.json
            logging.info(f'The received request data was {data}')

            if str(data['nfService']) == 'training':
                logging.info('Requesting training service from MTLF')
                mtlf.MTLF(config_file).training()
                data['data'] = 'training finish'
                
            elif str(data['nfService']) == 'inference':
                logging.info('Requesting inference service from ANLF')
                inference_result = anlf.ANLF(config_file).inference(data['data'])
                data['data'] = str(inference_result)
                
            else:
                data['data'] = 'None (Wrong)'

            data['reqNFInstanceID'] = data['reqNFInstanceID'] + ' (reply)'
            data['nfService'] = data['nfService'] + ' (reply)'
            # data['reqTime'] = data['reqTime']

        return json.dumps(data)

    if __name__ == "__main__":
        config_file = cfg.Config().load_config()
        log.Log().set_logging(config_file['application']['debug'])
        app.run(debug=config_file['application']['debug'])