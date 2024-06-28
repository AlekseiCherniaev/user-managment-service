import logging
import logging.config


def setup_logger(logger_name=''):
    logging.config.fileConfig('logging.conf', disable_existing_loggers=False)

    return logging.getLogger(logger_name)
