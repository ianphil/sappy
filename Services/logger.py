import logging

class Logger:
    def __init__(self, log_filename, log_level):
        self.log_level = log_level
        logging.basicConfig(filename=log_filename, level=logging.DEBUG)
    
    def log_error(self, msg):
        self.log_msg = 'ERROR -- '
        if self.log_level == 'DEBUG':
            print (self.log_msg + msg)
        logging.error(self.log_msg + msg)

    def log_info(self, msg):
        self.log_msg = 'INFO -- '
        if self.log_level == 'DEBUG':
            print (self.log_msg + msg)
        logging.info(self.log_msg + msg)
