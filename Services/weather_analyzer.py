
from collections import defaultdict
from collections.abc import Iterable

from Model.weather_data import WeatherData
from Model.weather_statistic import CountryWeatherSummary


def analyze_weather(
    weather_data: Iterable[WeatherData],
) -> list[CountryWeatherSummary]:
    """Group weather data by country and calculate statistics."""
    grouped: dict[str, list[WeatherData]] = defaultdict(list)
    country_names: dict[str, str] = {}

    for weather in weather_data:
        country = weather.country.strip()

        if not country:
            raise ValueError("Country name cannot be empty")

        country_key = country.casefold()
        country_names.setdefault(country_key, country)
        grouped[country_key].append(weather)

    summaries: list[CountryWeatherSummary] = []

    for country_key, cities in grouped.items():
        temperatures = [city.temperature_c for city in cities]

        summaries.append(
            CountryWeatherSummary(
                country=country_names[country_key],
                city_count=len(cities),
                average_temperature_c=(
                    sum(temperatures) / len(temperatures)
                ),
                min_temperature_c=min(temperatures),
                max_temperature_c=max(temperatures),
            )
        )

    return sorted(summaries, key=lambda summary: summary.country.casefold())