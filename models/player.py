from datetime import date, datetime
from typing import Any, Dict, Optional
from models.person import Person


class Player(Person):
    """Football Player class inheriting from Person"""
    
    # Valid football positions
    VALID_POSITIONS = {
        "Goalkeeper": ["GK"],
        "Defender": ["CB", "LB", "RB", "LWB", "RWB", "SW"],
        "Midfielder": ["CDM", "CM", "CAM", "LM", "RM", "LW", "RW"],
        "Forward": ["CF", "ST", "LF", "RF"]
    }
    
    # Valid contract status
    CONTRACT_STATUS = ["Active", "Expired", "Loan", "Transfer Listed", "Injured Reserve"]
    
    def __init__(self, name: str, age: int, position: str, jersey_number: int,
                 height: float = 0.0, weight: float = 0.0, nationality: str = "",
                 contract_start: Optional[date] = None, contract_end: Optional[date] = None,
                 salary: float = 0.0, market_value: float = 0.0, 
                 previous_clubs: str = "", goals: int = 0, assists: int = 0,
                 yellow_cards: int = 0, red_cards: int = 0, matches_played: int = 0,
                 phone: str = "", cccd: str = "", address: str = "", 
                 _id: Optional[str] = None):
        super().__init__(name, age, phone, cccd, address, _id)
        self._validate_player_info(position, jersey_number, height, weight)
        
        # Basic player info
        self._position = position
        self._jersey_number = jersey_number
        self._height = height  # in cm
        self._weight = weight  # in kg
        self._nationality = nationality
        
        # Contract info
        self._contract_start = contract_start
        self._contract_end = contract_end
        self._salary = salary
        self._market_value = market_value
        self._previous_clubs = previous_clubs
        
        # Performance stats
        self._goals = goals
        self._assists = assists
        self._yellow_cards = yellow_cards
        self._red_cards = red_cards
        self._matches_played = matches_played

    def _validate_player_info(self, position: str, jersey_number: int, 
                            height: float, weight: float) -> None:
        """Validate player-specific information"""
        if not position or not position.strip():
            raise ValueError("Position cannot be empty")
        
        if not isinstance(jersey_number, int) or jersey_number < 1 or jersey_number > 99:
            raise ValueError("Jersey number must be between 1 and 99")
            
        if height < 0 or height > 250:
            raise ValueError("Height must be between 0 and 250 cm")
            
        if weight < 0 or weight > 200:
            raise ValueError("Weight must be between 0 and 200 kg")

    # Position properties
    @property
    def position(self) -> str:
        return self._position

    @position.setter
    def position(self, value: str) -> None:
        if not value or not value.strip():
            raise ValueError("Position cannot be empty")
        self._position = value.strip()

    @property
    def jersey_number(self) -> int:
        return self._jersey_number

    @jersey_number.setter
    def jersey_number(self, value: int) -> None:
        if not isinstance(value, int) or value < 1 or value > 99:
            raise ValueError("Jersey number must be between 1 and 99")
        self._jersey_number = value

    # Physical properties
    @property
    def height(self) -> float:
        return self._height

    @height.setter
    def height(self, value: float) -> None:
        if value < 0 or value > 250:
            raise ValueError("Height must be between 0 and 250 cm")
        self._height = float(value)

    @property
    def weight(self) -> float:
        return self._weight

    @weight.setter
    def weight(self, value: float) -> None:
        if value < 0 or value > 200:
            raise ValueError("Weight must be between 0 and 200 kg")
        self._weight = float(value)

    @property
    def nationality(self) -> str:
        return self._nationality

    @nationality.setter
    def nationality(self, value: str) -> None:
        self._nationality = value.strip()

    # Contract properties
    @property
    def contract_start(self) -> Optional[date]:
        return self._contract_start

    @contract_start.setter
    def contract_start(self, value: Optional[date]) -> None:
        self._contract_start = value

    @property
    def contract_end(self) -> Optional[date]:
        return self._contract_end

    @contract_end.setter
    def contract_end(self, value: Optional[date]) -> None:
        self._contract_end = value

    @property
    def salary(self) -> float:
        return self._salary

    @salary.setter
    def salary(self, value: float) -> None:
        if value < 0:
            raise ValueError("Salary must be positive")
        self._salary = float(value)

    @property
    def market_value(self) -> float:
        return self._market_value

    @market_value.setter
    def market_value(self, value: float) -> None:
        if value < 0:
            raise ValueError("Market value must be positive")
        self._market_value = float(value)

    @property
    def previous_clubs(self) -> str:
        return self._previous_clubs

    @previous_clubs.setter
    def previous_clubs(self, value: str) -> None:
        self._previous_clubs = value.strip()

    # Performance properties
    @property
    def goals(self) -> int:
        return self._goals

    @goals.setter
    def goals(self, value: int) -> None:
        if value < 0:
            raise ValueError("Goals must be non-negative")
        self._goals = value

    @property
    def assists(self) -> int:
        return self._assists

    @assists.setter
    def assists(self, value: int) -> None:
        if value < 0:
            raise ValueError("Assists must be non-negative")
        self._assists = value

    @property
    def yellow_cards(self) -> int:
        return self._yellow_cards

    @yellow_cards.setter
    def yellow_cards(self, value: int) -> None:
        if value < 0:
            raise ValueError("Yellow cards must be non-negative")
        self._yellow_cards = value

    @property
    def red_cards(self) -> int:
        return self._red_cards

    @red_cards.setter
    def red_cards(self, value: int) -> None:
        if value < 0:
            raise ValueError("Red cards must be non-negative")
        self._red_cards = value

    @property
    def matches_played(self) -> int:
        return self._matches_played

    @matches_played.setter
    def matches_played(self, value: int) -> None:
        if value < 0:
            raise ValueError("Matches played must be non-negative")
        self._matches_played = value

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Player':
        """Create Player instance from dictionary"""
        # Handle date conversion
        contract_start = None
        contract_end = None
        
        if data.get("contract_start"):
            if isinstance(data["contract_start"], str):
                contract_start = datetime.strptime(data["contract_start"], "%Y-%m-%d").date()
            else:
                contract_start = data["contract_start"]
                
        if data.get("contract_end"):
            if isinstance(data["contract_end"], str):
                contract_end = datetime.strptime(data["contract_end"], "%Y-%m-%d").date()
            else:
                contract_end = data["contract_end"]
        
        return cls(
            name=data.get("name", ""),
            age=data.get("age", 18),
            position=data.get("position", ""),
            jersey_number=data.get("jersey_number", 1),
            height=data.get("height", 0.0),
            weight=data.get("weight", 0.0),
            nationality=data.get("nationality", ""),
            contract_start=contract_start,
            contract_end=contract_end,
            salary=data.get("salary", 0.0),
            market_value=data.get("market_value", 0.0),
            previous_clubs=data.get("previous_clubs", ""),
            goals=data.get("goals", 0),
            assists=data.get("assists", 0),
            yellow_cards=data.get("yellow_cards", 0),
            red_cards=data.get("red_cards", 0),
            matches_played=data.get("matches_played", 0),
            phone=data.get("phone", ""),
            cccd=data.get("cccd", ""),
            address=data.get("address", ""),
            _id=str(data.get("_id")) if data.get("_id") else None
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert Player to dictionary"""
        base_dict = self.get_basic_info()
        base_dict.update({
            "position": self._position,
            "jersey_number": self._jersey_number,
            "height": self._height,
            "weight": self._weight,
            "nationality": self._nationality,
            "contract_start": self._contract_start.isoformat() if self._contract_start else None,
            "contract_end": self._contract_end.isoformat() if self._contract_end else None,
            "salary": self._salary,
            "market_value": self._market_value,
            "previous_clubs": self._previous_clubs,
            "goals": self._goals,
            "assists": self._assists,
            "yellow_cards": self._yellow_cards,
            "red_cards": self._red_cards,
            "matches_played": self._matches_played,
            "role": self.get_role()
        })
        return base_dict

    def get_role(self) -> str:
        """Get player role"""
        return "Football Player"

    def get_player_info(self) -> str:
        """Get formatted player information"""
        return f"#{self._jersey_number} - {self._name} ({self._position})"

    def get_physical_info(self) -> str:
        """Get physical information"""
        if self._height > 0 and self._weight > 0:
            return f"Height: {self._height}cm, Weight: {self._weight}kg"
        return "Physical info not available"

    def get_performance_summary(self) -> str:
        """Get performance summary"""
        return (f"Matches: {self._matches_played}, Goals: {self._goals}, "
                f"Assists: {self._assists}, Yellow: {self._yellow_cards}, Red: {self._red_cards}")

    def get_contract_info(self) -> str:
        """Get contract information"""
        if self._contract_start and self._contract_end:
            return f"Contract: {self._contract_start} to {self._contract_end}"
        return "Contract info not available"

    def is_contract_active(self) -> bool:
        """Check if contract is currently active"""
        if not self._contract_end:
            return False
        return date.today() <= self._contract_end

    def get_goals_per_match(self) -> float:
        """Calculate goals per match ratio"""
        if self._matches_played == 0:
            return 0.0
        return round(self._goals / self._matches_played, 2)

    def get_assists_per_match(self) -> float:
        """Calculate assists per match ratio"""
        if self._matches_played == 0:
            return 0.0
        return round(self._assists / self._matches_played, 2)

    def add_goal(self, count: int = 1) -> None:
        """Add goals to player's record"""
        if count > 0:
            self._goals += count

    def add_assist(self, count: int = 1) -> None:
        """Add assists to player's record"""
        if count > 0:
            self._assists += count

    def add_yellow_card(self) -> None:
        """Add yellow card to player's record"""
        self._yellow_cards += 1

    def add_red_card(self) -> None:
        """Add red card to player's record"""
        self._red_cards += 1

    def add_match_played(self) -> None:
        """Increment matches played"""
        self._matches_played += 1

    def get_position_type(self) -> str:
        """Get general position type (Goalkeeper, Defender, Midfielder, Forward)"""
        for pos_type, positions in self.VALID_POSITIONS.items():
            if self._position in positions:
                return pos_type
        return "Unknown"

    def get_market_value_formatted(self) -> str:
        """Get formatted market value"""
        if self._market_value >= 1000000:
            return f"€{self._market_value / 1000000:.1f}M"
        elif self._market_value >= 1000:
            return f"€{self._market_value / 1000:.0f}K"
        else:
            return f"€{self._market_value:.0f}"

    def __str__(self) -> str:
        return f"Player #{self._jersey_number}: {self._name} - {self._position} (Age: {self._age})"

