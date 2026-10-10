
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class WeatherData:
    city: str
    temperature_c: float
    country: str