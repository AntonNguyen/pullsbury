from nose.tools import eq_, ok_, raises
from pullsbury.handlers.github_handler import GithubHandler
from pullsbury.config import load_config
from tests import load_fixture
from unittest import TestCase
import httpretty
import github as pygithub

class TestGithubHandler(TestCase):
    def test_get_oauth_client(self):
        github = self.get_github_handler({
            'GITHUB_OAUTH_TOKEN': 'oauth-token'
        })
        ok_(isinstance(github.client, pygithub.Github))

    def test_get_username_password_client(self):
        github = self.get_github_handler()
        ok_(isinstance(github.client, pygithub.Github))

    @httpretty.activate
    def test_create_hook_succeeds(self):
        self.mock_github_auth()
        self.mock_github_create_hook()
        github = self.get_github_handler()
        github.register('org_name', 'www.example.com')
        eq_(httpretty.last_request().path, '/orgs/org_name/hooks')

    @httpretty.activate
    @raises(Exception)
    def test_create_hook_fails(self):
        self.mock_github_auth()
        self.mock_github_create_hook(
            status=422,
            fixture='github_create_hook_validation_failed.json')
        github = self.get_github_handler()
        github.register('org_name', 'www.example.com')

    @httpretty.activate
    def test_delete_hook_succeeds(self):
        self.mock_github_auth()
        self.mock_github_get_hooks()
        self.mock_github_delete_hook()
        github = self.get_github_handler()
        github.unregister('org_name', 'http://mysite.example.com')
        eq_(httpretty.last_request().path, '/orgs/org_name/hooks/910')

    @httpretty.activate
    @raises(Exception)
    def test_delete_hook_cannot_find_hook(self):
        self.mock_github_auth()
        self.mock_github_get_hooks()
        github = self.get_github_handler()
        github.unregister('org_name', 'www.unknown.com')

    @httpretty.activate
    @raises(Exception)
    def test_delete_hook_already_deleted(self):
        self.mock_github_auth()
        self.mock_github_get_hooks()
        self.mock_github_delete_hook(status=404, fixture='github_delete_hook_not_found.json')
        github = self.get_github_handler()
        github.unregister('org_name', 'http://mysite.example.com')

    def mock_github_auth(self, status=200, fixture='github_auth.json'):
        httpretty.register_uri(
            httpretty.GET,
            'http://api.github.com/orgs/org_name',
            status=status,
            body=load_fixture(fixture)
        )

    def mock_github_create_hook(self, status=200, fixture='github_create_hook_success.json'):
        httpretty.register_uri(
            httpretty.POST,
            'http://api.github.com/orgs/org_name/hooks',
            status=status,
            body=load_fixture(fixture)
        )

    def mock_github_get_hooks(self):
        httpretty.register_uri(
            httpretty.GET,
            'http://api.github.com/orgs/org_name/hooks',
            status=200,
            body=load_fixture('github_get_hooks_success.json')
        )

    def mock_github_delete_hook(self, status=200, fixture=None):
        body = ''
        if fixture:
            body = load_fixture(fixture)
        httpretty.register_uri(
            httpretty.DELETE,
            'http://api.github.com/orgs/org_name/hooks/910',
            status=status,
            body=body
        )

    def get_github_handler(self, custom_config=None):
        config = load_config()
        if custom_config:
            config.update({
                'GITHUB_OAUTH_TOKEN': 'oauth-token'
            })
        return GithubHandler(config)