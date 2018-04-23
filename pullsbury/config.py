import os
import json
import logging.config
from flask.config import Config


def load_config(settings_file='./test_settings.py'):
    """
    Loads the config files merging the defaults
    with the file defined in environ.PULLSBURY_SETTINGS if it exists.
    """
    config = Config(os.getcwd())

    if 'PULLSBURY_SETTINGS' in os.environ:
        config.from_envvar('PULLSBURY_SETTINGS')
    else:
        config.from_pyfile(settings_file)

    if config.get('LOGGING_CONFIG'):
        logging.config.fileConfig(
            config.get('LOGGING_CONFIG'),
            disable_existing_loggers=False)

    json_values = [
        'TEAMS',
        'HAPPY_SLACK_EMOJIS',
        'REPO_BLACKLIST',
        'SLACK_CUSTOM_EMOJI_MAPPING'
    ]

    for value in json_values:
        if value in config:
            config.update({
                value: json.loads(config.get(value, ''))
            })

    return config
