
import tkinter as tk
from pathlib import Path
from tkinter import messagebox, ttk

from Model.weather_data import WeatherData
from Model.weather_statistic import CountryWeatherSummary
from Services.weather_formatter import (
    format_city_weather,
    format_country_summary,
)
from ViewModel.weather_viewmodel import WeatherViewModel


class WeatherView:
    """Tkinter view for the VkWeather application."""

    def __init__(
        self,
        root: tk.Tk,
        view_model: WeatherViewModel,
    ) -> None:
        self.root = root
        self.view_model = view_model

        self.root.title("VkWeather — Weather Dashboard")
        self.root.geometry("900x650")
        self.root.minsize(700, 500)

        self._build_ui()
        self.root.after(100, self._process_events)

    def _build_ui(self) -> None:
        container = ttk.Frame(self.root, padding=16)
        container.pack(fill=tk.BOTH, expand=True)

        header = ttk.Frame(container)
        header.pack(fill=tk.X, pady=(0, 12))

        ttk.Label(
            header,
            text="VkWeather",
            font=("Segoe UI", 20, "bold"),
        ).pack(side=tk.LEFT)

        self.refresh_button = ttk.Button(
            header,
            text="Обновить погоду",
            command=self._refresh,
        )
        self.refresh_button.pack(side=tk.RIGHT)

        self.status_var = tk.StringVar(value="Готово к загрузке")
        ttk.Label(
            container,
            textvariable=self.status_var,
        ).pack(anchor=tk.W, pady=(0, 8))

        self.progress = ttk.Progressbar(
            container,
            mode="determinate",
            maximum=100,
        )
        self.progress.pack(fill=tk.X, pady=(0, 16))

        ttk.Label(
            container,
            text="Погода по городам",
            font=("Segoe UI", 12, "bold"),
        ).pack(anchor=tk.W, pady=(0, 6))

        self.weather_table = ttk.Treeview(
            container,
            columns=("city", "country", "temperature"),
            show="headings",
            height=10,
        )
        self.weather_table.heading("city", text="Город")
        self.weather_table.heading("country", text="Страна")
        self.weather_table.heading("temperature", text="Температура")

        self.weather_table.column("city", width=240)
        self.weather_table.column("country", width=240)
        self.weather_table.column("temperature", width=150, anchor=tk.CENTER)

        self.weather_table.pack(fill=tk.BOTH, expand=True)

        ttk.Label(
            container,
            text="Статистика по странам",
            font=("Segoe UI", 12, "bold"),
        ).pack(anchor=tk.W, pady=(16, 6))

        self.statistics_table = ttk.Treeview(
            container,
            columns=("country", "count", "average", "minimum", "maximum"),
            show="headings",
            height=7,
        )

        headings = {
            "country": "Страна",
            "count": "Городов",
            "average": "Средняя, °C",
            "minimum": "Минимум, °C",
            "maximum": "Максимум, °C",
        }

        for column, heading in headings.items():
            self.statistics_table.heading(column, text=heading)

        self.statistics_table.column("country", width=180)
        self.statistics_table.column("count", width=90, anchor=tk.CENTER)

        for column in ("average", "minimum", "maximum"):
            self.statistics_table.column(
                column,
                width=120,
                anchor=tk.CENTER,
            )

        self.statistics_table.pack(fill=tk.X)

    def _refresh(self) -> None:
        if not self.view_model.start_loading():
            return

        self.refresh_button.configure(state=tk.DISABLED)
        self.progress.configure(value=0)
        self.status_var.set("Подготовка загрузки…")

        self._clear_table(self.weather_table)
        self._clear_table(self.statistics_table)

    def _process_events(self) -> None:
        for event, payload in self.view_model.get_events():
            if event == "loading":
                self.status_var.set("Загрузка погоды…")

            elif event == "progress":
                current, total, city = payload
                self.status_var.set(
                    f"Загрузка {current}/{total}: {city}"
                )
                self.progress.configure(
                    value=(current / total * 100) if total else 0
                )

            elif event == "result":
                weather_data, summaries, errors = payload
                self._show_weather(weather_data)
                self._show_statistics(summaries)

                if errors:
                    self.status_var.set(
                        f"Загрузка завершена с ошибками: "
                        f"{len(errors)} из них"
                    )
                    messagebox.showwarning(
                        "Некоторые города не загружены",
                        "\n".join(errors),
                        parent=self.root,
                    )
                else:
                    self.status_var.set(
                        f"Загрузка завершена. "
                        f"Городов обработано: {len(weather_data)}"
                    )

            elif event == "error":
                self.status_var.set("Ошибка загрузки")
                messagebox.showerror(
                    "Ошибка VkWeather",
                    str(payload),
                    parent=self.root,
                )

            elif event == "finished":
                self.refresh_button.configure(state=tk.NORMAL)

        self.root.after(100, self._process_events)

    def _show_weather(self, weather_data: list[WeatherData]) -> None:
        for weather in weather_data:
            self.weather_table.insert(
                "",
                tk.END,
                values=(
                    weather.city,
                    weather.country,
                    f"{weather.temperature_c:+.0f} °C",
                ),
            )

    def _show_statistics(
        self,
        summaries: list[CountryWeatherSummary],
    ) -> None:
        for summary in summaries:
            self.statistics_table.insert(
                "",
                tk.END,
                values=(
                    summary.country,
                    summary.city_count,
                    f"{summary.average_temperature_c:+.1f}",
                    f"{summary.min_temperature_c:+.0f}",
                    f"{summary.max_temperature_c:+.0f}",
                ),
            )

    @staticmethod
    def _clear_table(table: ttk.Treeview) -> None:
        for item in table.get_children():
            table.delete(item)