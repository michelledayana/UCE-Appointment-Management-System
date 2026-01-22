import pytest
from unittest.mock import patch

from app.services.validation_service import validate_availability


def test_validate_availability_success():
    """
    When Redis returns True, availability should be valid
    """
    with patch("app.services.validation_service.get_availability") as mock_get:
        mock_get.return_value = True

        result = validate_availability("dentistry")

        assert result is True
        mock_get.assert_called_once_with("dentistry")


def test_validate_availability_not_available():
    """
    When Redis returns False, availability should be invalid
    """
    with patch("app.services.validation_service.get_availability") as mock_get:
        mock_get.return_value = False

        result = validate_availability("dentistry")

        assert result is False
        mock_get.assert_called_once_with("dentistry")


def test_validate_availability_no_data():
    """
    When Redis has no key, availability is invalid
    """
    with patch("app.services.validation_service.get_availability") as mock_get:
        mock_get.return_value = None

        result = validate_availability("dentistry")

        assert result is False
        mock_get.assert_called_once_with("dentistry")
