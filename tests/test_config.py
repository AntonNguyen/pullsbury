from unittest import TestCase
from pullsbury.config import load_config


def test_load_config():
    res = load_config()
    assert res['GITHUB_USER'].endswith, 'Exists and is stringy'
