from typing import Optional, List
from pydantic import BaseModel, Field, field_validator
from datetime import datetime
import re
import locale


class OlxItem(BaseModel):
    olx_id: int = Field(..., description="Unique identifier for the OLX item")
    views: Optional[int] = Field(default=0, description="Number of views for the OLX item")
    title: str = Field(..., description="Title of the OLX item")
    price: str = Field(..., description="Price of the OLX item")
    published_at: str = Field(..., description="Publication date in Ukrainian")
    description: Optional[str] = Field(default=None, description="Description of the OLX item")
    images: Optional[List[str]] = Field(default=None, description="List of image URLs for the OLX item")
    tags: Optional[List[str]] = Field(default=None, description="List of tags for the OLX item")

    @field_validator("olx_id", "views", mode="before")
    def validate_integer_fields(cls, value, info):
        """Validate and extract integers from string input."""
        if value is None:
            return 0  # Default for None
        if isinstance(value, str):
            try:
                return int("".join(filter(str.isdigit, value)))
            except ValueError:
                raise ValueError(f"Invalid integer value for {info.field_name}: {value}")
        return value

    @field_validator("published_at", mode="before")
    def validate_and_parse_date(cls, value):
        """Parse Ukrainian publication date strings into a standardized format."""
        try:
            parsed_date = cls.parse_ukrainian_date(value)
            return parsed_date.strftime("%Y-%m-%d %H:%M:%S")
        except ValueError as e:
            raise ValueError(f"Invalid publication date format: {value}") from e

    @staticmethod
    def parse_ukrainian_date(date_str: str) -> datetime:
        """Parse a Ukrainian date string into a datetime object."""
        try:
            # Set the locale to Ukrainian to handle Ukrainian month names
            locale_code = "uk_UA.UTF-8"
            locale.setlocale(locale.LC_TIME, locale_code)

            # Handle special case for "Сьогодні"
            if "Сьогодні" in date_str:
                time_str = date_str.split("в")[-1].strip()
                today = datetime.now()
                hour, minute = map(int, time_str.split(":"))
                return today.replace(hour=hour, minute=minute, second=0, microsecond=0)

            # Remove trailing "г." or "р." if present
            cleaned_date = re.sub(r'\s*(г\.|р\.)\s*$', '', date_str).strip()

            # Try to parse the cleaned date string
            return datetime.strptime(cleaned_date, "%d %B %Y")
        except (ValueError, locale.Error) as e:
            raise ValueError(f"Invalid date string: {date_str}") from e
