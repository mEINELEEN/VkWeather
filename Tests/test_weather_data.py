
import unittest
from dataclasses import FrozenInstanceError

from Model.weather_data import WeatherData


class TestWeatherData(unittest.TestCase):
    def test_create_weather_data(self):
        weather = WeatherData(
            city="Moscow",
            temperature_c=12.0,
            country="Russia",
        )

        self.assertEqual(weather.city, "Moscow")
        self.assertEqual(weather.temperature_c, 12.0)
        self.assertEqual(weather.country, "Russia")

    def test_weather_data_is_immutable(self):
        weather = WeatherData(
            city="Moscow",
            temperature_c=12.0,
            country="Russia",
        )

        with self.assertRaises(FrozenInstanceError):
            weather.city = "Vienna"


if __name__ == "__main__":
    unittest.main()