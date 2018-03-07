import pullsbury.github as github

from . import load_fixture
from mock import call
from mock import patch
from mock import Mock
from nose.tools import eq_
from pygithub3 import Github
from requests.models import Response


config = {
    'GITHUB_URL': 'https://api.github.com/',
    'GITHUB_USER': 'octocat',
    'GITHUB_PASSWORD': ''
}


def test_get_client():
    gh = github.get_client(config, 'anton', 'myrepository')
    assert isinstance(gh, Github)
