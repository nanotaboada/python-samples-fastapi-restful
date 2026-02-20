"""
SQLAlchemy ORM model for the Player database table.

Defines the schema and columns corresponding to football player attributes.

Used for async database CRUD operations in the application.
"""

from uuid import UUID, uuid4
from sqlalchemy import Column, String, Integer, Boolean, TypeDecorator
from databases.player_database import Base


class HyphenatedUUID(TypeDecorator):
    """
    Custom SQLAlchemy type that stores UUIDs as hyphenated strings in SQLite
    (e.g. '550e8400-e29b-41d4-a716-446655440000') and returns Python UUID objects.
    """

    impl = String(36)
    cache_ok = True

    def process_bind_param(self, value, dialect):
        if value is None:
            return None
        if isinstance(value, UUID):
            return str(value)
        return str(UUID(str(value)))

    def process_result_value(self, value, dialect):
        if value is None:
            return None
        return UUID(value)


class Player(Base):
    """
    SQLAlchemy schema describing a database table of football players.

    Attributes:
        id (UUID): Surrogate key — the internal technical primary key. Opaque to
            end users; used for all CRUD operations and service-to-service calls.
            Records created through the API receive a randomly generated UUID v4.
            Records seeded by migration scripts use deterministic UUID v5 values so
            that IDs are stable across environments and can be safely referenced in
            tests.
        first_name (String): The first name of the player (not nullable).
        middle_name (String): The middle name of the player.
        last_name (String): The last name of the player (not nullable).
        date_of_birth (String): The date of birth of the player.
        squad_number (Integer): Natural key — the domain identifier meaningful to
            API consumers (e.g. squad number 10 = Messi). Unlike the surrogate UUID,
            this value is human-readable and stable within a squad roster. It is the
            preferred lookup key for external clients. Not nullable, unique.
        position (String): The playing position of the player (not nullable).
        abbr_position (String): The abbreviated form of the player's position.
        team (String): The team to which the player belongs.
        league (String): The league where the team plays.
        starting11 (Boolean): Indicates if the player is in the starting 11.
    """

    __tablename__ = "players"

    # Surrogate key: opaque UUID, internal to the system. UUID v4 for API-created
    # records (randomly generated); UUID v5 for migration-seeded records
    # (deterministic, stable across environments).
    id = Column(
        HyphenatedUUID(),
        primary_key=True,
        default=uuid4,
        nullable=False,
    )
    first_name = Column(String, name="firstName", nullable=False)
    middle_name = Column(String, name="middleName")
    last_name = Column(String, name="lastName", nullable=False)
    date_of_birth = Column(String, name="dateOfBirth")
    # Natural key: human-readable domain identifier, unique within a squad roster.
    # Preferred lookup key for external API consumers over the surrogate UUID.
    squad_number = Column(Integer, name="squadNumber", unique=True, nullable=False)
    position = Column(String, nullable=False)
    abbr_position = Column(String, name="abbrPosition")
    team = Column(String)
    league = Column(String)
    starting11 = Column(Boolean)
