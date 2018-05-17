from os import path, remove
import logging
import logging.config
import logging.handlers
import json
# from config.config import LOGGING as logging_config_dict


with open("setting/logger/logging_configuration.json", 'r') as configuration_file:
    config_dict = json.load(configuration_file)
logging.config.dictConfig(config_dict)
# Create the Logger
logger = logging.getLogger(__name__)
# logger.setLevel(logging.WARNING)