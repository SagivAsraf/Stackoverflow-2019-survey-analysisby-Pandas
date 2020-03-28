import logging
from Utils.DateUtils import DateUtils

class PandasLogger:

    def __init__(self):
        pass

    def create_pandas_logger(self,logger,log_file_name):

        log_file_name_with_time_stamp = str(DateUtils.get_time()) + "_" + log_file_name

        logger = logging.getLogger(log_file_name)
        logger.setLevel(logging.INFO)
        fh = logging.FileHandler(log_file_name_with_time_stamp, 'w+')
        fh.setLevel(logging.INFO)

        # create formatter and add it to the handlers
        formatter = logging.Formatter('%(asctime)s - %(message)s')
        fh.setFormatter(formatter)
        # add the handlers to the logger
        logger.addHandler(fh)

        print("log file will save in: " + logger.handlers[0].baseFilename)

        logger.info("Pandas_Seminary_Project")

        return logger