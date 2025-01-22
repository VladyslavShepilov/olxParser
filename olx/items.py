import locale
import re
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field, field_validator


class ItemValidator(BaseModel):
    olx_id: int = Field(..., description="Unique identifier for the OLX item")
    views: Optional[int] = Field(
        default=0, description="Number of views for the OLX item"
    )
    title: str = Field(..., description="Title of the OLX item")
    price: str = Field(..., description="Price of the OLX item")
    published_at: datetime = Field(..., description="Publication date in Ukrainian")
    description: Optional[str] = Field(
        default=None, description="Description of the OLX item"
    )
    images: Optional[List[str]] = Field(
        default=None, description="List of image URLs for the OLX item"
    )
    tags: Optional[List[str]] = Field(
        default=None, description="List of tags for the OLX item"
    )

    @field_validator("olx_id", "views", mode="before")
    def validate_integer_fields(cls, value, info):
        """Extract the last numeric part of a string input."""
        if value is None:
            return 0
        if isinstance(value, str):
            try:
                # Split the string by spaces and take the last part
                last_part = value.split()[-1]
                return int(last_part)
            except (ValueError, IndexError):
                raise ValueError(
                    f"Invalid integer value for {info.field_name}: {value}"
                )
        return value

    @field_validator("published_at", mode="before")
    def validate_published_at(cls, value):
        """Parse and validate the date string with manual month mapping."""
        try:
            if "Сьогодні" in value or "Сегодня" in value:
                time_str = value.split("в")[-1].strip()
                today = datetime.now()
                hour, minute = map(int, time_str.split(":"))
                return today.replace(hour=hour, minute=minute, second=0, microsecond=0)

            month_mapping = {
                # Ukr
                "Січень": 1, "Лютий": 2, "Березень": 3, "Квітень": 4,
                "Травень": 5, "Червень": 6, "Липень": 7, "Серпень": 8,
                "Вересень": 9, "Жовтень": 10, "Листопад": 11, "Грудень": 12,
                # Rus
                "Январь": 1, "Февраль": 2, "Март": 3, "Апрель": 4,
                "Май": 5, "Июнь": 6, "Июль": 7, "Август": 8,
                "Сентябрь": 9, "Октябрь": 10, "Ноябрь": 11, "Декабрь": 12,
            }

            parts = value.split()
            day = int(parts[0])
            month_name = parts[1]
            year = int(parts[2]) if len(parts) > 2 else datetime.now().year

            # Get the month number from the mapping
            month = month_mapping.get(month_name)
            if not month:
                raise ValueError(f"Unknown month name: {month_name}")

            return datetime(year, month, day)
        except (ValueError, IndexError) as e:
            raise ValueError(f"Invalid date format: {e}") from e