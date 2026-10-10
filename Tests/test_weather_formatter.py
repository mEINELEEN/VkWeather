
import unittest

from Model.weather_data import WeatherData
from Model.weather_statistic import CountryWeatherSummary
from Services.weather_formatter import (
    format_city_weather,
    format_country_summary,
    format_temperature,
)


class TestWeatherFormatter(unittest.TestCase):
    def test_positive_temperature(self):
        self.assertEqual(format_temperature(18.0), "+18 C")

    def test_negative_temperature(self):
        self.assertEqual(format_temperature(-4.0), "-4 C")

    def test_city_weather(self):
        weather = WeatherData("Tokyo", 18.0, "Japan")

        self.assertEqual(
            format_city_weather(weather),
            "Tokyo, Japan +18 C",
        )

    def test_country_summary(self):
        summary = CountryWeatherSummary(
            country="Japan",
            city_count=2,
            average_temperature_c=20.0,
            min_temperature_c=18.0,
            max_temperature_c=22.0,
        )

        self.assertEqual(
            format_country_summary(summary),
            "Japan - 2 cities, avg: +20 C, min: +18 C, max: +22 C",
        )


if __name__ == "__main__":
    unittest.main()