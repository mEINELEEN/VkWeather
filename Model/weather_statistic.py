
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CountryWeatherSummary:
    country: str
    city_count: int
    average_temperature_c: float
    min_temperature_c: float
    max_temperature_c: float