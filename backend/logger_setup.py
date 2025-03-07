import logging

def logger_setup(name, log_file = 'server.log', log_level = logging.DEBUG):
    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    file_handler = logging.FileHandler(log_file)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger