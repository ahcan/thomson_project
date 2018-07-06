from os import path, remove
import logging
import logging.config
import logging.handlers
import json
# from config.config import LOGGING as logging_config_dict


def getLogger(loggerName):
    with open("setting/logger/logging_configuration.json", 'r') as configuration_file:
        config_dict = json.load(configuration_file)
    logging.config.dictConfig(config_dict)
# Create the Logger
    return logging.getLogger(loggerName)
# logger.setLevel(logging.WARNING)