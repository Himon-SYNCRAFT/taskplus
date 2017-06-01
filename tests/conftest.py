import pytest

from taskplus.apps.rest.app import create_app
from taskplus.apps.rest.settings import TestConfig


@pytest.fixture(scope='function')
def app():
    return create_app(TestConfig)
