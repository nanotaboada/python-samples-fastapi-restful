# -------------------------------------------------------------------------------------------------
# Model
# -------------------------------------------------------------------------------------------------

from typing import Optional
from pydantic import BaseModel, Field


class PlayerModel(BaseModel):
    id: int
    first_name: str = Field(..., serialization_alias='firstName')
    middle_name: Optional[str] = Field(None, serialization_alias='middleName')
    last_name: str = Field(..., serialization_alias='lastName')
    date_of_birth: Optional[str] = Field(..., serialization_alias='dateOfBirth')
    squad_number: int = Field(..., serialization_alias='squadNumber')
    position: str = Field(..., serialization_alias='position')
    abbr_position: Optional[str] = Field(..., serialization_alias='abbrPosition')
    team: Optional[str] = Field(..., serialization_alias='team')
    league: Optional[str] = Field(..., serialization_alias='league')
    starting11: Optional[bool] = Field(..., serialization_alias='starting11')


class Config:
    orm_mode = True
