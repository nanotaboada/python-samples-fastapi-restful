# -------------------------------------------------------------------------------------------------
# Schema
# -------------------------------------------------------------------------------------------------

from pydantic import BaseModel
from typing import Optional


class PlayerModel(BaseModel):
    id: int
    firstName: str
    middleName: Optional[str] = None
    lastName: str
    dateOfBirth: str
    squadNumber: int
    position: str
    abbrPosition: str
    team: str
    league: str
    starting11: bool

    class ConfigDict:
        from_attributes = True
