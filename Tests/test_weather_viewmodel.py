
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from Model.weather_data import WeatherData
from Model.weather_statistic import CountryWeatherSummary
from ViewModel.weather_viewmodel import WeatherViewModel


class TestWeatherViewModel(unittest.TestCase):
    def test_loading_weather_produces_results(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            cities_file = Path(temp_dir) / "cities.txt"
            cities_file.write_text(
                "Tokyo\nOsaka\n",
                encoding="utf-8",
            )

            view_model = WeatherViewModel(cities_file)

            with (
                patch(
                    "ViewModel.weather_viewmodel.get_weather",
                    side_effect=[
                        WeatherData("Tokyo", 18.0, "Japan"),
                        WeatherData("Osaka", 22.0, "Japan"),
                    ],
                ),
                patch(
                    "ViewModel.weather_viewmodel.analyze_weather",
                    return_value=[
                        CountryWeatherSummary(
                            country="Japan",
                            city_count=2,
                            average_temperature_c=20.0,
                            min_temperature_c=18.0,
                            max_temperature_c=22.0,
                        )
                    ],
                ),
            ):
                self.assertTrue(view_model.start_loading())
                view_model._worker.join(timeout=5)

            events = view_model.get_events()
            result_events = [
                payload
                for event, payload in events
                if event == "result"
            ]

            self.assertEqual(len(result_events), 1)

            weather, summaries, errors = result_events[0]

            self.assertEqual(len(weather), 2)
            self.assertEqual(len(summaries), 1)
            self.assertEqual(errors, [])

    def test_missing_file_produces_error_event(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            missing_file = Path(temp_dir) / "missing.txt"
            view_model = WeatherViewModel(missing_file)

            view_model._load_weather()
            events = view_model.get_events()

        self.assertTrue(
            any(event == "error" for event, _ in events)
        )


if __name__ == "__main__":
    unittest.main()