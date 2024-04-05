import logging


class Logger:
    # * This is a class that will create a logger object to be used in your script 
    def __init__(self, name=__name__, level=int(1), file_path=None):
        self.logger = logging.getLogger(name)
        # # Default log level is set to INFO
        if level > 4:
            # # If verbose is more than 4
            self.logger.setLevel('DEBUG')
        else:
            self.logger.setLevel('INFO')


        formatter = logging.Formatter('%(asctime)s - [%(levelname)s] %(name)s ''%(funcName)s | %(message)s')

        if file_path:
            file_handler = logging.FileHandler(file_path)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

    def get_logger(self):
        return self.logger
