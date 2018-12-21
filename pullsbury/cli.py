import argparse
import sys

from pullsbury.config import load_config
from pullsbury.handlers.github_handler import GithubHandler
from pullsbury.handlers.slack_handler import SlackHandler


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


def send_reminders(args):
    try:
        github = GithubHandler(load_config())
        slack = SlackHandler(load_config())

        ignored_prs = github.get_uncommented_prs()
        slack.send_reminders(ignored_prs)

        sys.stdout.write('Slack reminders sent\n')
    except Exception as e:
        sys.stderr.write('Slack reminders failed to send\n')
        sys.stderr.write(e.message + '\n')
        sys.exit(2)


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

    desc = """
    Send team reminders for unreviewed PRs
    """
    remove = commands.add_parser('send_reminders', help=desc)
    remove.set_defaults(func=send_reminders)

    return parser


if __name__ == '__main__':
    main()
