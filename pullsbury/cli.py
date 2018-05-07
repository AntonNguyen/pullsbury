import argparse
import sys

from flask import url_for
from pullsbury.config import load_config
from pullsbury.database import db
from pullsbury.handlers.github_handler import GithubHandler
from pullsbury.models.user import User
from pullsbury.models.team import Team
from pullsbury.models.team_member import TeamMember
from pullsbury.models.emoji import Emoji
from pullsbury.models.pull_request import PullRequest
from pullsbury.models.comment import Comment
from pullsbury.web import app


def main():
    parser = create_parser()
    args = parser.parse_args()
    if 'func' not in args:
        sys.stderr.write('Incorrect command\n')
        sys.exit(2)
    args.func(args)


def register_hook(args):
    try:
        github = GithubHandler(load_config())
        github.register(args.org, args.url)
        sys.stdout.write('Hook registered successfully\n')
    except Exception as error:
        sys.stderr.write('Hook registration failed\n')
        sys.stderr.write(error + '\n')
        sys.exit(2)


def unregister_hook(args):
    try:
        github = GithubHandler(load_config())
        github.unregister(args.org, args.url)
        sys.stdout.write('Hook removed successfully\n')
    except Exception as error:
        sys.stderr.write('Hook removal failed\n')
        sys.stderr.write(error + '\n')
        sys.exit(2)


def create_tables(args):
    with app.app_context():
        db.init_app(app)
        sys.stdout.write('Creating tables\n')
        db.create_all()
        db.session.commit()


def drop_tables(args):
    with app.app_context():
        db.init_app(app)
        sys.stdout.write('Dropping tables\n')
        db.drop_all()
        db.session.commit()


def populate_tables(args):
    happy_emojis = [
        "exclamation",
        "heart",
        "icecream",
        "joy_cat",
        "octocat",
        "rainbow",
        "smile",
        "snowflake",
        "snowman",
        "sparkles",
        "squirrel",
        "tada"
    ]
    with app.app_context():
        db.init_app(app)
        sys.stdout.write('Populating tables\n')
        for name in happy_emojis:
            Emoji(name=name, sentiment="happy").save()
        db.session.commit()


def create_user(args):
    with app.app_context():
        db.init_app(app)
        sys.stdout.write('Creating user\n')
        User(github_username=args.github, slack_username=args.slack).save()
        db.session.commit()


def create_team(args):
    with app.app_context():
        db.init_app(app)
        sys.stdout.write('Creating team\n')
        Team(name=args.name, slack_channel=args.slack_channel).save()
        db.session.commit()


def add_team_member(args):
    with app.app_context():
        db.init_app(app)
        sys.stdout.write('Adding team member\n')
        user = db.session.query(User).filter_by(github_username=args.github).first()
        team = db.session.query(Team).filter_by(name=args.team).first()
        TeamMember(user_id=user.id, team_id=team.id, ).save()
        db.session.commit()


def add_emoji(args):
    with app.app_context():
        db.init_app(app)
        sys.stdout.write('Adding emoji\n')
        Emoji(name=args.name, sentiment=args.sentiment).save()
        db.session.commit()


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
    Creates the database tables
    """
    create = commands.add_parser('create_tables', help=desc)
    create.set_defaults(func=create_tables)

    desc = """
    Drops the database tables
    """
    drop = commands.add_parser('drop_tables', help=desc)
    drop.set_defaults(func=drop_tables)

    desc = """
    Populates the database tables
    """
    populate = commands.add_parser('populate_tables', help=desc)
    populate.set_defaults(func=populate_tables)

    desc = """
    Creates a user
    """
    user = commands.add_parser('create_user', help=desc)
    user.add_argument('github',
                      help="The user's github username.")
    user.add_argument('slack',
                      help="The user's slack username.")
    user.set_defaults(func=create_user)

    desc = """
    Creates a team
    """
    team = commands.add_parser('create_team', help=desc)
    team.add_argument('name',
                      help="The team's name.")
    team.add_argument('slack_channel',
                      help="The team's slack channel.")
    team.set_defaults(func=create_team)


    desc = """
    Adds a user to a team
    """
    team = commands.add_parser('add_team_member', help=desc)
    team.add_argument('github',
                      help="The user's github username.")
    team.add_argument('team',
                      help="The team's name.")
    team.set_defaults(func=add_team_member)

    desc = """
    Adds an emoji
    """
    emoji = commands.add_parser('add_emoji', help=desc)
    emoji.add_argument('name',
                      help="The name of the emoji")
    emoji.add_argument('sentiment',
                      help="The sentiment: happy/sad")
    emoji.set_defaults(func=add_emoji)

    return parser

if __name__ == '__main__':
    main()