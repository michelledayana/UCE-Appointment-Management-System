import pytest
from unittest.mock import MagicMock
from app.main import app
from app.db.database import get_db


@pytest.fixture
def mock_db():
    db = MagicMock()
    yield db


@pytest.fixture(autouse=True)
def override_get_db(mock_db):
    def _get_db_override():
        yield mock_db

    app.dependency_overrides[get_db] = _get_db_override
    yield
    app.dependency_overrides.clear()
