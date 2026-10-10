
import sys
from pathlib import Path

from Services.city_loader import load_cities
from Services.weather_analyzer import analyze_weather
from Services.weather_api import WeatherApiError, get_weather
from Services.weather_formatter import (
    format_city_weather,
    format_country_summary,
)


def main() -> int:
    """Run the VkWeather command-line application."""
    project_dir = Path(__file__).resolve().parent
    cities_file = project_dir / "Data" / "cities.txt"

    try:
        cities = load_cities(cities_file)
    except OSError as error:
        print(
            f"Error reading cities file: {error}",
            file=sys.stderr,
        )
        return 1

    if not cities:
        print("No cities found in the input file.")
        return 0

    weather_data = []

    print("VkWeather")
    print("=" * 40)
    print("Current weather")
    print("-" * 40)

    for city in cities:
        try:
            weather = get_weather(city)
        except WeatherApiError as error:
            print(f"Failed to get weather for {city}: {error}",
                  file=sys.stderr)
            continue

        weather_data.append(weather)
        print(format_city_weather(weather))

    if not weather_data:
        print("Weather data could not be retrieved for any city.")
        return 1

    summaries = analyze_weather(weather_data)

    print()
    print("Weather statistics by country")
    print("-" * 40)

    for summary in summaries:
        print(format_country_summary(summary))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())