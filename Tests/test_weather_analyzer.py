
import unittest

from Model.weather_data import WeatherData
from Model.weather_statistic import CountryWeatherSummary
from Services.weather_analyzer import analyze_weather


class TestWeatherAnalyzer(unittest.TestCase):
    def test_group_cities_and_calculate_statistics(self):
        weather_data = [
            WeatherData("Tokyo", 18.0, "Japan"),
            WeatherData("Osaka", 22.0, "Japan"),
            WeatherData("Moscow", -4.0, "Russia"),
        ]

        result = analyze_weather(weather_data)

        self.assertEqual(
            result,
            [
                CountryWeatherSummary(
                    country="Japan",
                    city_count=2,
                    average_temperature_c=20.0,
                    min_temperature_c=18.0,
                    max_temperature_c=22.0,
                ),
                CountryWeatherSummary(
                    country="Russia",
                    city_count=1,
                    average_temperature_c=-4.0,
                    min_temperature_c=-4.0,
                    max_temperature_c=-4.0,
                ),
            ],
        )

    def test_country_grouping_is_case_insensitive(self):
        weather_data = [
            WeatherData("Tokyo", 18.0, "Japan"),
            WeatherData("Osaka", 22.0, "JAPAN"),
        ]

        result = analyze_weather(weather_data)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].country, "Japan")
        self.assertEqual(result[0].city_count, 2)
        self.assertEqual(result[0].average_temperature_c, 20.0)

    def test_empty_input(self):
        self.assertEqual(analyze_weather([]), [])

    def test_empty_country_is_rejected(self):
        weather_data = [
            WeatherData("Tokyo", 18.0, "   "),
        ]

        with self.assertRaises(ValueError):
            analyze_weather(weather_data)


if __name__ == "__main__":
    unittest.main()