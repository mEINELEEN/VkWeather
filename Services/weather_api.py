import json
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

from Model.weather_data import WeatherData


class WeatherApiError(Exception):
    """Raised when weather data cannot be retrieved or parsed."""


def get_weather(city: str) -> WeatherData:
    """Fetch current weather for a city from wttr.in."""
    encoded_city = quote(city, safe="")
    url = f"https://wttr.in/{encoded_city}?format=j1"

    request = Request(
        url,
        headers={"User-Agent": "VkWeather/1.0"},
    )

    try:
        with urlopen(request, timeout=15) as response:
            payload = json.loads(response.read().decode("utf-8"))

    except HTTPError as error:
        raise WeatherApiError(
            f"HTTP error for {city}: {error.code}"
        ) from error
    except URLError as error:
        raise WeatherApiError(
            f"Network error for {city}: {error.reason}"
        ) from error
    except (TimeoutError, OSError) as error:
        raise WeatherApiError(
            f"Connection failed for {city}: {error}"
        ) from error
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise WeatherApiError(
            f"Invalid JSON response for {city}"
        ) from error

    try:
        current = payload["current_condition"][0]
        area = payload["nearest_area"][0]

        temperature = float(current["temp_C"])
        country = area["country"][0]["value"]

        if not country:
            raise ValueError("Country is empty")

    except (KeyError, IndexError, TypeError, ValueError) as error:
        raise WeatherApiError(
            f"Unexpected API response for {city}"
        ) from error

    return WeatherData(
        city=city,
        temperature_c=temperature,
        country=country,
    )