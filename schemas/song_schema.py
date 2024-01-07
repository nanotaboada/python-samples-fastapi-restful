# -------------------------------------------------------------------------------------------------
# Schemas
# -------------------------------------------------------------------------------------------------

from pydantic import BaseModel
from typing import Optional


class SongModel(BaseModel):
    rank: int
    title: str
    artist: str
    album: Optional[str] = None
    year: int

    class ConfigDict:
        from_attributes = True
