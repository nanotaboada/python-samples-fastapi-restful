"""
Pydantic models defining the data schema for football players.

- `MainModel`: Base model with common config for camelCase aliasing.
- `PlayerRequestModel`: Represents player data for Create and Update operations.
- `PlayerResponseModel`: Represents player data including UUID for Retrieve operations.

These models are used for data validation and serialization in the API.
"""

from typing import Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class MainModel(BaseModel):
    """
    Base model configuration for all Pydantic models in the application.

    This class sets a common configuration for alias generation and name population
    for any model that inherits from it. It uses camelCase for JSON field names.

    Attributes:
        model_config (ConfigDict): Configuration for Pydantic models, including:
            alias_generator (function): A function to generate field aliases.
                Here, it uses `to_camel` to convert field names to camelCase.
            populate_by_name (bool): Allows population of fields by name when using
            Pydantic models.
    """

    model_config = ConfigDict(
        alias_generator=to_camel, populate_by_name=True, from_attributes=True
    )


class PlayerRequestModel(MainModel):
    """
    Pydantic model representing the data required for Create and Update operations
    on a football Player.

    Attributes:
        first_name (str): The first name of the Player.
        middle_name (Optional[str]): The middle name of the Player, if any.
        last_name (str): The last name of the Player.
        date_of_birth (Optional[str]): The date of birth of the Player, if provided.
        squad_number (int): The unique squad number assigned to the Player.
        position (str): The playing position of the Player.
        abbr_position (Optional[str]): The abbreviated form of the Player's position,
        if any.
        team (Optional[str]): The team to which the Player belongs, if any.
        league (Optional[str]): The league where the team plays, if any.
        starting11 (Optional[bool]): Indicates if the Player is in the starting 11,
        if provided.
    """

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


class PlayerResponseModel(PlayerRequestModel):
    """
    Pydantic model representing a football Player with a UUID for Retrieve operations.

    Attributes:
        id (UUID): The unique identifier for the Player (UUID v4).
    """

    id: UUID
