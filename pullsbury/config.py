import os
import json
import logging.config

from flask.config import Config
from ConfigParser import ConfigParser
from StringIO import StringIO


def load_config():
    """
    Loads the config files merging the defaults
    with the file defined in environ.PULLSBURY_SETTINGS if it exists.
    """
    config = Config(os.getcwd())

    if 'PULLSBURY_SETTINGS' in os.environ:
        config.from_envvar('PULLSBURY_SETTINGS')
    elif os.path.exists(os.path.join(os.getcwd(), 'settings.py')):
        config.from_pyfile('settings.py')
    else:
        msg = ("Unable to load configuration file. Please "
               "either create ./settings.py or set PULLSBURY_SETTINGS "
               "in your environment before running.")
        raise ImportError(msg)
    if config.get('LOGGING_CONFIG'):
        logging.config.fileConfig(
            config.get('LOGGING_CONFIG'),
            disable_existing_loggers=False)

    if config.get('SSL_CA_BUNDLE'):
        os.environ['REQUESTS_CA_BUNDLE'] = config.get('SSL_CA_BUNDLE')

    json_values = [
        'TEAMS', 'HAPPY_SLACK_EMOJIS', 'REPO_BLACKLIST', 'SLACK_CUSTOM_EMOJI_MAPPING'
    ]

    for value in json_values:
        if value in config:
            config.update({
                value: json.loads(config.get(value, ''))
            })

    return config

