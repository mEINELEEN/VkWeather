
import json
import unittest
from io import BytesIO
from unittest.mock import patch
from urllib.error import HTTPError

from Model.weather_data import WeatherData
from Services.weather_api import WeatherApiError, get_weather


def make_api_response(
    temperature: str = "18",
    country: str = "Japan",
) -> bytes:
    """Build a minimal valid wttr.in JSON response."""
    payload = {
        "current_condition": [
            {"temp_C": temperature}
        ],
        "nearest_area": [
            {
                "country": [
                    {"value": country}
                ]
            }
        ],
    }
    return json.dumps(payload).encode("utf-8")


class TestWeatherApi(unittest.TestCase):
    @patch("Services.weather_api.urlopen")
    def test_get_weather_returns_weather_data(self, mock_urlopen):
        mock_urlopen.return_value = BytesIO(make_api_response())

        result = get_weather("Tokyo")

        self.assertEqual(
            result,
            WeatherData(
                city="Tokyo",
                temperature_c=18.0,
                country="Japan",
            ),
        )

        mock_urlopen.assert_called_once()

    @patch("Services.weather_api.urlopen")
    def test_http_error_is_converted(self, mock_urlopen):
        mock_urlopen.side_effect = HTTPError(
            url="https://wttr.in/Tokyo?format=j1",
            code=503,
            msg="Service Unavailable",
            hdrs=None,
            fp=None,
        )

        with self.assertRaises(WeatherApiError):
            get_weather("Tokyo")

    @patch("Services.weather_api.urlopen")
    def test_invalid_json_is_converted(self, mock_urlopen):
        mock_urlopen.return_value = BytesIO(b"{invalid json")

        with self.assertRaises(WeatherApiError):
            get_weather("Tokyo")

    @patch("Services.weather_api.urlopen")
    def test_unexpected_response_is_converted(self, mock_urlopen):
        mock_urlopen.return_value = BytesIO(
            json.dumps({"unexpected": []}).encode("utf-8")
        )

        with self.assertRaises(WeatherApiError):
            get_weather("Tokyo")


if __name__ == "__main__":
    unittest.main()
