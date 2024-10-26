from datetime import datetime

from pydantic import BaseModel


class GameData(BaseModel):
    idx: int
    icon: str
    honor: str
    level: int
    name: str
    rating: float
    max_rating: float
    over_power: float
    over_power_percentage: float
    lastplaydate: datetime
