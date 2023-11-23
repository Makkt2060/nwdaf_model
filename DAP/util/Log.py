import logging

class Log:    
    
    def set_logging(self, debug):
        if debug:
            logging.basicConfig(level = logging.DEBUG, format = '%(message)s')
        else:
            logging.basicConfig(level = logging.ERROR, format = '%(message)s')