
from Model.weather_data import WeatherData
from Model.weather_statistic import CountryWeatherSummary


def format_temperature(temperature_c: float) -> str:
    """Format temperature with an explicit sign and whole degrees."""
    return f"{temperature_c:+.0f} C"


def format_city_weather(weather: WeatherData) -> str:
    """Format weather information for one city."""
    return (
        f"{weather.city}, {weather.country} "
        f"{format_temperature(weather.temperature_c)}"
    )


def format_country_summary(summary: CountryWeatherSummary) -> str:
    """Format aggregated weather statistics for one country."""
    return (
        f"{summary.country} - {summary.city_count} cities, "
        f"avg: {format_temperature(summary.average_temperature_c)}, "
        f"min: {format_temperature(summary.min_temperature_c)}, "
        f"max: {format_temperature(summary.max_temperature_c)}"
    )