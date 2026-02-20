import pytest
import json
import urllib.request
import urllib.parse
from unittest.mock import patch
from weather_service import weather_service  # Assuming the file is named weather_service.py


def test_weather_service_success():
    """Tests a standard success case with a valid city name."""
    with patch("urllib.request.urlopen") as mock_urlopen:
        mock_response = mock_urlopen.return_value
        mock_response.read.return_value = json.dumps({
            "cod": 200,
            "weather": [{"description": "clear sky"}],
            "main": {"temp": 25, "humidity": 60},
            "wind": {"speed": 5}
        }).encode()
        result = weather_service("London")
        assert "Weather in London" in result
        assert "Description: clear sky" in result
        assert "Temperature: 25°C" in result
        assert "Humidity: 60%" in result
        assert "Wind Speed: 5 m/s" in result


def test_weather_service_empty_city():
    """Tests the edge case of an empty city name."""
    result = weather_service("")
    assert result == "Error: City name cannot be empty."


def test_weather_service_large_city_name():
    """Tests the edge case of a very long city name."""
    city_name = "ThisIsAVeryLongCityNameThatShouldStillBeHandled"
    with patch("urllib.request.urlopen") as mock_urlopen:
        mock_response = mock_urlopen.return_value
        mock_response.read.return_value = json.dumps({
            "cod": 200,
            "weather": [{"description": "cloudy"}],
            "main": {"temp": 15, "humidity": 80},
            "wind": {"speed": 2}
        }).encode()
        result = weather_service(city_name)
        assert f"Weather in {city_name}" in result
        assert "Description: cloudy" in result
        assert "Temperature: 15°C" in result
        assert "Humidity: 80%" in result
        assert "Wind Speed: 2 m/s" in result


def test_weather_service_api_error():
    """Tests the failure mode of an API returning an error code."""
    with patch("urllib.request.urlopen") as mock_urlopen:
        mock_response = mock_urlopen.return_value
        mock_response.read.return_value = json.dumps({
            "cod": 404,
            "message": "city not found"
        }).encode()
        result = weather_service("InvalidCity")
        assert result == "Error: city not found"


def test_weather_service_network_error():
    """Tests the failure mode of a network error."""
    with patch("urllib.request.urlopen") as mock_urlopen:
        mock_urlopen.side_effect = urllib.error.URLError("Network is unreachable")
        result = weather_service("SomeCity")
        assert "Error: Network issue" in result
        assert "Network is unreachable" in result


def test_weather_service_unexpected_error():
    """Tests the failure mode of an unexpected exception."""
    with patch("urllib.request.urlopen") as mock_urlopen:
        mock_urlopen.side_effect = Exception("Some unexpected error")
        result = weather_service("AnotherCity")
        assert "Error: An unexpected error occurred" in result
        assert "Some unexpected error" in result