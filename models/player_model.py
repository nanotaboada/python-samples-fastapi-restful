# -------------------------------------------------------------------------------------------------
# Model
# -------------------------------------------------------------------------------------------------

from typing import Optional
from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class MainModel(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)


class PlayerModel(MainModel):
    id: int
    first_name: str
    middle_name: Optional[str]
    last_name: str
    date_of_birth: Optional[str]
    squad_number: int
    position: str
    abbr_position: Optional[str]
    team: Optional[str]
    league: Optional[str]
    starting11: Optional[bool]
