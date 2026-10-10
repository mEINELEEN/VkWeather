from pathlib import Path
from queue import Empty, Queue
from threading import Thread

from Model.weather_data import WeatherData
from Model.weather_statistic import CountryWeatherSummary
from Services.city_loader import load_cities
from Services.weather_analyzer import analyze_weather
from Services.weather_api import WeatherApiError, get_weather


class WeatherViewModel:
    """Coordinates weather loading and exposes events to the view."""

    def __init__(self, cities_file: str | Path) -> None:
        self._cities_file = Path(cities_file)
        self._events: Queue[tuple[str, object]] = Queue()
        self._worker: Thread | None = None

    @property
    def is_loading(self) -> bool:
        return self._worker is not None and self._worker.is_alive()

    def start_loading(self) -> bool:
        """Start loading in a background thread."""
        if self.is_loading:
            return False

        self._worker = Thread(
            target=self._load_weather,
            daemon=True,
        )
        self._events.put(("loading", None))
        self._worker = Thread(
            target=self._load_weather,
            daemon=True,
        )
        self._worker.start()
        return True

    def get_events(self) -> list[tuple[str, object]]:
        events: list[tuple[str, object]] = []

        while True:
            try:
                events.append(self._events.get_nowait())
            except Empty:
                break

        return events

    def _load_weather(self) -> None:
        try:
            cities = load_cities(self._cities_file)
        except OSError as error:
            self._events.put(("error", f"Cannot read cities file: {error}"))
            self._events.put(("finished", None))
            return

        weather_data: list[WeatherData] = []
        errors: list[str] = []

        for index, city in enumerate(cities, start=1):
            self._events.put(("progress", (index, len(cities), city)))

            try:
                weather_data.append(get_weather(city))
            except WeatherApiError as error:
                errors.append(f"{city}: {error}")

        summaries: list[CountryWeatherSummary] = []

        if weather_data:
            summaries = analyze_weather(weather_data)

        self._events.put(
            ("result", (weather_data, summaries, errors))
        )
        self._events.put(("finished", None))