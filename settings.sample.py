from kombu import Exchange, Queue
import os


def env(key, default, cast=str):
    return cast(os.environ.get(key, default))


# Webserver configuration #
###########################

# gunicorn config
bind = env('PULLSBURY_GUNICORN_BIND', '127.0.0.1:5000')
errorlog = env('PULLSBURY_GUNICORN_LOG_ERROR',
               'pullsbury.error.log')
accesslog = env('PULLSBURY_GUNICORN_LOG_ACCESS',
                'pullsbury.access.log')
debug = env('PULLSBURY_GUNICORN_DEBUG', True, bool)
loglevel = env('PULLSBURY_GUNICORN_LOGLEVEL', 'debug')

# Basic flask config
DEBUG = env('PULLSBURY_FLASK_DEBUG', True, bool)
TESTING = env('PULLSBURY_TESTING', True, bool)
SERVER_NAME = env('PULLSBURY_SERVER_NAME', '127.0.0.1:5000')

# Config file for logging
LOGGING_CONFIG = './logging.ini'


# Celery worker configuration #
###############################


# AMQP or other celery broker URL.
# amqp paths should be in the form of user:pass@host:port//virtualhost
BROKER_URL = 'amqp://'+''.join([
    env('PULLSBURY_MQ_USER', 'guest'), ':',
    env('PULLSBURY_MQ_PASS', 'guest'), '@',
    env('PULLSBURY_MQ_HOST',
        env('BROKER_PORT_5672_TCP_ADDR', '127.0.0.1')), ':',
    env('PULLSBURY_MQ_PORT',
        env('BROKER_PORT_5672_TCP_PORT', '5672')), '/',
    env('PULLSBURY_MQ_VIRTUAL_HOST', '/')
])

# Use json for serializing messages.
CELERY_TASK_SERIALIZER = 'json'

# Show dates and times in UTC
CELERY_ENABLE_UTC = True


# General project configuration #
#################################

# Path where project code should be
# checked out when reviews are done
# Repos will be checked out into $WORKSPACE/$user/$repo/$number
# directories to prevent collisions.
WORKSPACE = env('PULLSBURY_WORKSPACE', '/tmp/workspace')

# Use GITHUB_URL when working with github:e
# When working with github:e don't forget to add the /api/v3/ path
GITHUB_URL = env('GITHUB_URL', 'https://api.github.com/')

# Github username + password
# This is the user that pullsbury will use
# to fetch repositories and leave review comments.
# Set the GITHUB_PASSWORD environment variable first.
# example: $ export GITHUB_PASSWORD=mygithubpassword
GITHUB_USER = env('GITHUB_USERNAME', 'octocat')
GITHUB_PASSWORD = env('GITHUB_PASSWORD', '')

# You can also use an Oauth token for github, if you do
# uncomment this line. Using a token will take precedence
# over a username and password.
GITHUB_OAUTH_TOKEN = env('GITHUB_OAUTH_TOKEN', None)

# Set to a path containing a custom CA bundle.
# This is useful when you have github:enterprise on an internal
# network with self-signed certificates.
SSL_CA_BUNDLE = None
