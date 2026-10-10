
import tempfile
import unittest
from pathlib import Path

from Services.city_loader import load_cities


class TestCityLoader(unittest.TestCase):
    def test_load_unique_cities(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "cities.txt"
            file_path.write_text(
                "Moscow\nVienna\nMoscow\n\nPerm\n",
                encoding="utf-8",
            )

            result = load_cities(file_path)

        self.assertEqual(result, ["Moscow", "Vienna", "Perm"])

    def test_duplicate_detection_is_case_insensitive(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "cities.txt"
            file_path.write_text(
                "Moscow\nMOSCOW\nmoscow\n",
                encoding="utf-8",
            )

            result = load_cities(file_path)

        self.assertEqual(result, ["Moscow"])

    def test_empty_file(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "cities.txt"
            file_path.write_text("", encoding="utf-8")

            result = load_cities(file_path)

        self.assertEqual(result, [])


if __name__ == "__main__":
    unittest.main()