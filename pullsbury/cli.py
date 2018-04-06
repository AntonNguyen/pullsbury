import argparse
import sys

from flask import url_for
from pullsbury.config import load_config
from pullsbury.handlers.github_handler import GithubHandler
from pullsbury.web import app


def main():
    parser = create_parser()
    args = parser.parse_args()
    args.func(args)


def register_hook(args):
    try:
        github = GithubHandler(load_config())
        github.register(args.org, args.url)
        sys.stdout.write('Hook registered successfully\n')
    except Exception as e:
        sys.stderr.write('Hook registration failed\n')
        sys.stderr.write(e.message + '\n')
        sys.exit(2)


def unregister_hook(args):
    try:
        github = GithubHandler(load_config())
        github.unregister(args.org, args.url)
        sys.stdout.write('Hook removed successfully\n')
    except Exception as e:
        sys.stderr.write('Hook removal failed\n')
        sys.stderr.write(e.message + '\n')
        sys.exit(2)


def process_hook(func, args):
    """
    Generic helper for processing hook commands.
    """
    credentials = None
    if args.login_user and args.login_pass:
        credentials = {
            'GITHUB_USER': args.login_user,
            'GITHUB_PASSWORD': args.login_pass
        }

    with app.app_context():
        if credentials:
            credentials['GITHUB_URL'] = app.config['GITHUB_URL']
            gh = github.get_client(
                credentials,
                args.user,
                args.repo)
        else:
            gh = github.get_client(
                app.config,
                args.user,
                args.repo)
        endpoint = url_for('start_review', _external=True)
    func(gh, endpoint, args.user, args.repo)


def create_parser():
    desc = """
    Command line utilities for pullsbury.
    """
    parser = argparse.ArgumentParser(description=desc)

    commands = parser.add_subparsers(
        title="Subcommands",
        description="Valid subcommands")

    desc = """
    Register webhooks for a given org
    """
    register = commands.add_parser('register', help=desc)
    register.add_argument('org',
                          help="The organization the hook will be added to.")
    register.add_argument('url',
                          help="The url that pullsbury will be listening on.")
    register.set_defaults(func=register_hook)

    desc = """
    Unregister webhooks for the given org
    """
    remove = commands.add_parser('unregister', help=desc)
    remove.add_argument('org',
                          help="The organization the hook will be added to.")
    remove.add_argument('url',
                          help="The url that pullsbury will be listening on.")
    remove.set_defaults(func=unregister_hook)

    return parser

if __name__ == '__main__':
    main()