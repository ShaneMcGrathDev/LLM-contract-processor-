import os
from importlib import reload

import pytest


@pytest.fixture(autouse=True)
def clear_env(monkeypatch):
    monkeypatch.delenv('DATABASE_URL', raising=False)
    monkeypatch.delenv('SECRET_KEY', raising=False)
    monkeypatch.delenv('FLASK_ENV', raising=False)


def test_config_defaults_to_sqlite_when_database_url_missing(monkeypatch):
    import config

    reload(config)

    assert config.Config.SQLALCHEMY_DATABASE_URI == 'sqlite:///app.db'
    assert config.Config.SQLALCHEMY_TRACK_MODIFICATIONS is False
    assert config.Config.SECRET_KEY == 'dev-secret-key'
