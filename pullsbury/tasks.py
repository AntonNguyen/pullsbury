import pullsbury.github as github
import logging

from celery import Celery
from pullsbury.config import load_config

config = load_config()
celery = Celery('pullsbury.tasks')
celery.config_from_object(config)

log = logging.getLogger(__name__)


@celery.task(ignore_result=True)
def notify_pull_request(user, repo, number, target_branch):
    pass
