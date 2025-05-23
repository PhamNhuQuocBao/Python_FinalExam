from abc import ABC, abstractmethod
from typing import Optional, Dict, Any


class Club():
    """Base abstract class for all people in the system"""
    
    def __init__(self, name: str, city: str, country: str, _id: Optional[str] = None):
        self._validate_basic_info(name, city, country)
        self._id = _id
        self._name = name
        self._city = city
        self._country = country

    def _validate_basic_info(self, name: str, city: str, country: str) -> None:
        """Validate basic person information"""
        if not name or not name.strip():
            raise ValueError("Name cannot be empty")
        if not city or not city.strip():
            raise ValueError("City cannot be empty")
        if not country or not country.strip():
            raise ValueError("Country cannot be empty")

    # Properties with getters and setters
    @property
    def id(self) -> Optional[str]:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        if not value or not value.strip():
            raise ValueError("Name cannot be empty")
        self._name = value.strip()

    @property
    def city(self) -> int:
        return self._city

    @city.setter
    def city(self, value: int) -> None:
        if not value or not value.strip():
            raise ValueError("City cannot be empty")
        self._city = value

    @property
    def country(self) -> int:
        return self._country

    @country.setter
    def country(self, value: int) -> None:
        if not value or not value.strip():
            raise ValueError("Country cannot be empty")
        self._country = value

    def get_basic_info(self) -> Dict[str, Any]:
        """Get basic person information"""
        return {
            "name": self._name,
            "city": self._city,
            "country": self._country
        }

    def to_dict(self) -> Dict[str, Any]:
        """Convert object to dictionary"""
        return {**self.get_basic_info()}

   



