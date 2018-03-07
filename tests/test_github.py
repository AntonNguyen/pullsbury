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
    gh = github.get_client(config, 'anton')
    assert isinstance(gh, Github)


@patch('pygithub3.core.client.Client.get')
def test_register_hook(http):
    response = Response()
    response._content = '[]'
    http.return_value = response

    gh = Github()
    gh.repos.hooks.create = Mock()
    url = 'http://example.com/review/start'

    github.register_hook(gh, url, 'antonnguyen', 'test')

    assert gh.repos.hooks.create.called, 'Create not called'
    calls = gh.repos.hooks.create.call_args_list
    expected = call({
        'name': 'web',
        'active': True,
        'config': {
            'content_type': 'json',
            'url': url,
        },
        'events': ['pull_request']
    }, user='anton', repo='test')
    eq_(calls[0], expected)


@patch('pygithub3.core.client.Client.get')
def test_register_hook__already_exists(http):
    response = Response()
    response._content = load_fixture('webhook_list.json')
    http.return_value = response

    gh = Github()
    gh.repos.hooks.create = Mock()
    url = 'http://example.com/review/start'

    github.register_hook(gh, url, 'anton', 'test')

    assert gh.repos.hooks.create.called is False, 'Create called'


@patch('pygithub3.core.client.Client.get')
def test_unregister_hook__success(http):
    response = Response()
    response._content = load_fixture('webhook_list.json')
    http.return_value = response

    gh = Github()
    gh.repos.hooks.delete = Mock()
    url = 'http://example.com/review/start'

    github.unregister_hook(gh, url, 'anton', 'test')

    assert gh.repos.hooks.delete.called, 'Delete not called'


@patch('pygithub3.core.client.Client.get')
def test_unregister_hook__not_there(http):
    response = Response()
    response._content = "[]"
    http.return_value = response

    gh = Github()
    gh.repos.hooks.delete = Mock()
    url = 'http://example.com/review/start'

    try:
        github.unregister_hook(gh, url, 'anton', 'test')
        assert False, 'No exception'
    except:
        assert True, 'Exception raised'
    assert gh.repos.hooks.delete.called is False, 'Delete called'
