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
    description: str = field(default=None)
    images: Optional[str] = field(default=None)
    tags: Optional[str] = field(default=None)

    def __post_init__(self):
        try:
            self.published_at = parse_ukrainian_date(self.published_at)
        except ValueError:
            raise ValueError(f"Invalid publication date format: {self.published_at}")
        

def parse_ukrainian_date(date_str):
    try:
        locale.setlocale(locale.LC_TIME, "uk_UA.UTF-8")
        
        if "Сьогодні" in date_str:
            return datetime.now()
        
        cleaned_date = date_str.replace(" р.", "").strip()
        date_obj = datetime.strptime(cleaned_date, "%d %B %Y")
        return date_obj
    
    except (ValueError, locale.Error):
        raise ValueError(f"Invalid date string: {date_str}")