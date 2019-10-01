import github
import logging

log = logging.getLogger(__name__)
github_logger = logging.getLogger("github")
github_logger.setLevel(logging.INFO)


class GithubHandler(object):
    def __init__(self, config):
        if 'GITHUB_OAUTH_TOKEN' in config and config.get('GITHUB_OAUTH_TOKEN'):
            self.client = github.Github(
                base_url=config.get('GITHUB_URL'),
                login_or_token=config.get('GITHUB_OAUTH_TOKEN'))
        else:
            self.client = github.Github(
                base_url=config.get('GITHUB_URL'),
                login_or_token=config.get('GITHUB_USER'),
                password=config.get('GITHUB_PASSWORD'))

    def register(self, org_name, url):
        org = self.client.get_organization(org_name)
        try:
            org.create_hook("web", {"url": url}, events=["pull_request"], active=True)
        except github.GithubException as error:
            response = error.data
            message = "{}: {}".format(response['message'], response['errors'][0]['message'])
            raise Exception(message)

    def unregister(self, org_name, url):
        org = self.client.get_organization(org_name)
        hooks = org.get_hooks()

        hook_id = None
        for hook in hooks:
            if hook.config['url'] == url:
                hook_id = hook.id
                break

        if not hook_id:
            msg = ("Could not find hook for '%s' "
                   "No hooks removed.") % (url)
            raise Exception(msg)

        try:
            org.delete_hook(hook_id)
        except github.UnknownObjectException as error:
            raise Exception(error.data['message'])
