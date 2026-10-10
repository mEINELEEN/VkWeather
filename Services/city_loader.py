
from pathlib import Path


def load_cities(file_path: str | Path) -> list[str]:
    """Load unique city names from a text file."""
    path = Path(file_path)

    cities: list[str] = []
    seen: set[str] = set()

    with path.open("r", encoding="utf-8-sig") as file:
        for line in file:
            city = line.strip()

            if not city:
                continue

            normalized_city = city.casefold()

            if normalized_city in seen:
                continue

            seen.add(normalized_city)
            cities.append(city)

    return cities