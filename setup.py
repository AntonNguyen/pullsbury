from setuptools import setup

PACKAGE_NAME = "pullsbury"
VERSION = "0.1.0"

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    description="""
    Pullsbury Gitboy, a collaborative code review tool that alerts team members
    Whenever a pull request has been put up by a team member
    """,
    author="Anton",
    author_email="afnguyen85@gmail.com",
    entry_points={
        'console_scripts': [
            'pullsbury = pullsbury.cli:main',
        ],
    },
)
