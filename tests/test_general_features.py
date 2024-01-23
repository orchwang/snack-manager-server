import pytest

from snack.celery import app as celery_app


class TestMisc:
    def test_dummy_case_success(self):
        assert 1 == 1


@pytest.fixture(scope='session')
def celery_session_worker():
    return celery_app
