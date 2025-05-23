

from typing import Any, Dict, Optional
from models.person import Person


class Trainer(Person):
    """Football Trainer class inheriting from Person"""
    
    # Valid coaching positions in football
    VALID_POSITIONS = [
        "Head Coach", "Assistant Coach", "Goalkeeping Coach", 
        "Fitness Coach", "Technical Coach", "Youth Coach",
        "Tactical Analyst", "Set Piece Coach"
    ]
    
    # Valid coaching licenses
    VALID_LICENSES = [
        "UEFA Pro License", "UEFA A License", "UEFA B License", 
        "AFC Pro License", "AFC A License", "AFC B License",
        "FIFA Coaching License", "National C License", "Grassroots License"
    ]
    
    def __init__(self, name: str, age: int, coaching_position: str, 
                 coaching_license: str = "", experience_years: int = 0, 
                 previous_clubs: str = "", salary: float = 0.0,
                 phone: str = "", cccd: str = "", address: str = "", 
                 _id: Optional[str] = None):
        super().__init__(name, age, phone, cccd, address, _id)
        self._validate_trainer_info(coaching_position, experience_years, salary)
        self._coaching_position = coaching_position
        self._coaching_license = coaching_license
        self._experience_years = experience_years
        self._previous_clubs = previous_clubs
        self._salary = salary

    def _validate_trainer_info(self, coaching_position: str, experience_years: int, salary: float) -> None:
        """Validate trainer-specific information"""
        if not coaching_position or not coaching_position.strip():
            raise ValueError("Coaching position cannot be empty")
        if not isinstance(experience_years, int) or experience_years < 0:
            raise ValueError("Experience years must be a positive integer")
        if not isinstance(salary, (int, float)) or salary < 0:
            raise ValueError("Salary must be a positive number")

    @property
    def coaching_position(self) -> str:
        return self._coaching_position

    @coaching_position.setter
    def coaching_position(self, value: str) -> None:
        if not value or not value.strip():
            raise ValueError("Coaching position cannot be empty")
        self._coaching_position = value.strip()

    @property
    def coaching_license(self) -> str:
        return self._coaching_license

    @coaching_license.setter
    def coaching_license(self, value: str) -> None:
        self._coaching_license = value.strip()

    @property
    def experience_years(self) -> int:
        return self._experience_years

    @experience_years.setter
    def experience_years(self, value: int) -> None:
        if not isinstance(value, int) or value < 0:
            raise ValueError("Experience years must be a positive integer")
        self._experience_years = value

    @property
    def previous_clubs(self) -> str:
        return self._previous_clubs

    @previous_clubs.setter
    def previous_clubs(self, value: str) -> None:
        self._previous_clubs = value.strip()

    @property
    def salary(self) -> float:
        return self._salary

    @salary.setter
    def salary(self, value: float) -> None:
        if not isinstance(value, (int, float)) or value < 0:
            raise ValueError("Salary must be a positive number")
        self._salary = float(value)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Trainer':
        """Create Trainer instance from dictionary"""
        return cls(
            name=data.get("name", ""),
            age=data.get("age", 30),
            coaching_position=data.get("coaching_position", ""),
            coaching_license=data.get("coaching_license", ""),
            experience_years=data.get("experience_years", 0),
            previous_clubs=data.get("previous_clubs", ""),
            salary=data.get("salary", 0.0),
            phone=data.get("phone", ""),
            cccd=data.get("cccd", ""),
            address=data.get("address", ""),
            _id=str(data.get("_id")) if data.get("_id") else None
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert Trainer to dictionary"""
        base_dict = self.get_basic_info()
        base_dict.update({
            "coaching_position": self._coaching_position,
            "coaching_license": self._coaching_license,
            "experience_years": self._experience_years,
            "previous_clubs": self._previous_clubs,
            "salary": self._salary,
            "role": self.get_role()
        })
        return base_dict

    def get_role(self) -> str:
        """Get trainer role"""
        return "Football Trainer"

    def get_trainer_info(self) -> str:
        """Get formatted trainer information"""
        license_info = f" ({self._coaching_license})" if self._coaching_license else ""
        return f"{self._name} - {self._coaching_position}{license_info} ({self._experience_years} years experience)"

    def is_qualified_for_position(self, required_license: str) -> bool:
        """Check if trainer has required license for a position"""
        return self._coaching_license == required_license

    def get_salary_info(self) -> str:
        """Get formatted salary information"""
        if self._salary > 0:
            return f"${self._salary:,.2f}"
        return "Salary not disclosed"

    def add_previous_club(self, club_name: str) -> None:
        """Add a previous club to trainer's history"""
        if club_name and club_name.strip():
            if self._previous_clubs:
                self._previous_clubs += f", {club_name.strip()}"
            else:
                self._previous_clubs = club_name.strip()

    def __str__(self) -> str:
        return f"Football Trainer: {self._name} - {self._coaching_position} ({self._experience_years} years experience)"

