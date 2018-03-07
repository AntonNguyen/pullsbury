from setuptools import setup, find_packages

PACKAGE_NAME = "pullsbury"
VERSION = "0.3.0"

requirements = open('./requirements.txt', 'r')

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    description="""
    Pullsbury Gitboy, a collaborative code review tool that alerts team members
    Whenever a pull request has been put up by a team member
    """,
    author="Anton",
    author_email="afnguyen85@gmail.com",
    packages=find_packages(),
    install_requires=requirements.readlines(),
)
