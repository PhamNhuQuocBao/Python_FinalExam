from abc import ABC, abstractmethod
from typing import Optional, Dict, Any


class Person(ABC):
    """Base abstract class for all people in the system"""
    
    def __init__(self, name: str, age: int, phone: str = "", cccd: str = "", 
                 address: str = "", _id: Optional[str] = None):
        self._validate_basic_info(name, age)
        self._id = _id
        self._name = name
        self._age = age
        self._phone = phone
        self._cccd = cccd
        self._address = address

    def _validate_basic_info(self, name: str, age: int) -> None:
        """Validate basic person information"""
        if not name or not name.strip():
            raise ValueError("Name cannot be empty")
        if not isinstance(age, int) or age < 0 or age > 150:
            raise ValueError("Age must be a valid integer between 0 and 150")

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
    def age(self) -> int:
        return self._age

    @age.setter
    def age(self, value: int) -> None:
        if not isinstance(value, int) or value < 0 or value > 99:
            raise ValueError("Age must be a valid integer between 0 and 150")
        self._age = value

    @property
    def phone(self) -> str:
        return self._phone

    @phone.setter
    def phone(self, value: str) -> None:
        self._phone = value.strip()

    @property
    def cccd(self) -> str:
        return self._cccd

    @cccd.setter
    def cccd(self, value: str) -> None:
        self._cccd = value.strip()

    @property
    def address(self) -> str:
        return self._address

    @address.setter
    def address(self, value: str) -> None:
        self._address = value.strip()

    def get_basic_info(self) -> Dict[str, Any]:
        """Get basic person information"""
        return {
            "name": self._name,
            "age": self._age,
            "phone": self._phone,
            "cccd": self._cccd,
            "address": self._address
        }

    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """Convert object to dictionary - must be implemented by subclasses"""
        pass

    @abstractmethod
    def get_role(self) -> str:
        """Get the role/type of this person - must be implemented by subclasses"""
        pass

    def __str__(self) -> str:
        return f"{self.get_role()}: {self._name} (Age: {self._age})"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name='{self._name}', age={self._age})"



