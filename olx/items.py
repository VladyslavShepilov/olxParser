from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime
import locale

@dataclass
class OlxItem:
    id: int
    views: int
    title: str
    price: str
    published_at: str
    description: Optional[str] = field(default=None)
    images: Optional[str] = field(default=None)
    tags: Optional[str] = field(default=None)

    def __post_init__(self):
        if isinstance(self.id, str):
            self.id = self._extract_integer(self.id, "id")
        
        if isinstance(self.views, str):
            self.views = self._extract_integer(self.views, "views")
        
        try:
            parsed_date = self.parse_ukrainian_date(self.published_at)
            self.published_at = parsed_date.strftime("%Y-%m-%d %H:%M:%S")
        except ValueError as e:
            raise ValueError(f"Invalid publication date format: {self.published_at}") from e

    @staticmethod
    def _extract_integer(value: str, field_name: str) -> int:
        try:
            return int("".join(filter(str.isdigit, value)))
        except ValueError:
            raise ValueError(f"Invalid integer value for {field_name}: {value}")

    @staticmethod
    def parse_ukrainian_date(date_str: str) -> datetime:
        try:
            locale_code = "uk_UA.UTF-8"
            locale.setlocale(locale.LC_TIME, locale_code)
            
            if "Сьогодні" in date_str:
                time_str = date_str.split("в")[-1].strip()
                today = datetime.now()
                hour, minute = map(int, time_str.split(":"))
                return today.replace(hour=hour, minute=minute, second=0, microsecond=0)
            
            cleaned_date = date_str.replace(" г.", "").strip()
            return datetime.strptime(cleaned_date, "%d %B %Y")
        
        except (ValueError, locale.Error):
            raise ValueError(f"Invalid date string: {date_str}")
