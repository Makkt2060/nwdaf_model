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
            data['reqTime'] = data['reqTime']

        return json.dumps(data)

    if __name__ == "__main__":
        config_file = cfg.Config().load_config()
        log.Log().set_logging(config_file['application']['debug'])
        app.run(debug=config_file['application']['debug'], port=config_file['application']['port'])