"""
Test cases for the PlayerService.
"""

from unittest.mock import AsyncMock, Mock, patch
from uuid import UUID

import pytest
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from models.player_model import PlayerRequestModel
from schemas.player_schema import Player
from services.player_service import (
    create_async,
    delete_by_squad_number_async,
    retrieve_all_async,
    retrieve_by_id_async,
    retrieve_by_squad_number_async,
    update_by_squad_number_async,
)
from tests.player_fake import existing_player, nonexistent_player, unknown_player


@pytest.fixture
def existing_player_request_model():
    """Fixture for an existing PlayerRequestModel."""
    return PlayerRequestModel(
        first_name="Damián",
        middle_name="Emiliano",
        last_name="Martínez",
        date_of_birth="1992-09-02T00:00:00.000Z",
        squad_number=23,
        position="Goalkeeper",
        abbr_position="GK",
        team="Aston Villa FC",
        league="Premier League",
        starting11=True,
    )


@pytest.fixture
def existing_player_schema():
    """Fixture for an existing Player schema."""
    return Player(
        id=UUID("01772c59-43f0-5d85-b913-c78e4e281452"),
        first_name="Damián",
        middle_name="Emiliano",
        last_name="Martínez",
        date_of_birth="1992-09-02T00:00:00.000Z",
        squad_number=23,
        position="Goalkeeper",
        abbr_position="GK",
        team="Aston Villa FC",
        league="Premier League",
        starting11=True,
    )


@pytest.mark.anyio
async def test_create_async_success(existing_player_request_model):
    """Test the successful creation of a Player."""
    mock_session = AsyncMock(spec=AsyncSession)

    result = await create_async(mock_session, existing_player_request_model)

    assert result is not None
    mock_session.add.assert_called_once_with(result)
    mock_session.commit.assert_awaited_once()
    mock_session.refresh.assert_awaited_once_with(result)


@pytest.mark.anyio
async def test_create_async_database_error(existing_player_request_model):
    """Return None and roll back when player creation raises a database error."""
    mock_session = AsyncMock(spec=AsyncSession)
    mock_session.commit.side_effect = SQLAlchemyError("Connection timeout")

    result = await create_async(mock_session, existing_player_request_model)

    assert result is None
    mock_session.commit.assert_awaited_once()
    mock_session.rollback.assert_awaited_once()
    mock_session.refresh.assert_not_awaited()


@pytest.mark.anyio
async def test_retrieve_all_async():
    """Test the retrieval of all players."""
    mock_session = AsyncMock(spec=AsyncSession)
    mock_result = Mock()
    mock_players = [existing_player(), nonexistent_player(), unknown_player()]
    mock_result.scalars.return_value.all.return_value = mock_players

    mock_session.execute.return_value = mock_result

    result = await retrieve_all_async(mock_session)

    assert result == mock_players
    mock_session.execute.assert_awaited_once()


@pytest.mark.anyio
async def test_retrieve_all_async_empty():
    """Test the retrieval of all players when no players exist."""
    mock_session = AsyncMock(spec=AsyncSession)
    mock_result = Mock()
    mock_result.scalars.return_value.all.return_value = []

    mock_session.execute.return_value = mock_result

    result = await retrieve_all_async(mock_session)

    assert result == []
    mock_session.execute.assert_awaited_once()


@pytest.mark.anyio
async def test_retrieve_by_id_async(existing_player_schema):
    """Test the retrieval of a player by ID."""
    mock_session = AsyncMock(spec=AsyncSession)

    mock_session.get.return_value = existing_player_schema

    result = await retrieve_by_id_async(mock_session, existing_player_schema.id)

    assert result == existing_player_schema
    mock_session.get.assert_awaited_once_with(Player, existing_player_schema.id)


@pytest.mark.anyio
async def test_retrieve_by_id_async_not_found():
    """Test the retrieval of a player by ID when the player does not exist."""
    mock_session = AsyncMock(spec=AsyncSession)
    non_existent_id = UUID("00000000-0000-0000-0000-000000000000")

    mock_session.get.return_value = None

    result = await retrieve_by_id_async(mock_session, non_existent_id)

    assert result is None
    mock_session.get.assert_awaited_once_with(Player, non_existent_id)


@pytest.mark.anyio
async def test_retrieve_by_squad_number_async(existing_player_schema):
    """Test the retrieval of a player by Squad Number."""
    mock_session = AsyncMock(spec=AsyncSession)
    mock_result = Mock()
    mock_result.scalars.return_value.first.return_value = existing_player_schema

    mock_session.execute.return_value = mock_result

    result = await retrieve_by_squad_number_async(
        mock_session,
        existing_player_schema.squad_number,
    )

    assert result == existing_player_schema
    mock_session.execute.assert_awaited_once()
    statement = mock_session.execute.await_args.args[0]
    expected = Player.squad_number == existing_player_schema.squad_number
    assert statement.whereclause.compare(expected)


@pytest.mark.anyio
async def test_retrieve_by_squad_number_async_not_found():
    """Test the retrieval of a player by Squad Number when the player does not exist."""
    mock_session = AsyncMock(spec=AsyncSession)
    non_existent_squad_number = 99

    mock_result = Mock()
    mock_result.scalars.return_value.first.return_value = None
    mock_session.execute.return_value = mock_result

    result = await retrieve_by_squad_number_async(
        mock_session, non_existent_squad_number
    )

    assert result is None

    mock_session.execute.assert_awaited_once()
    statement = mock_session.execute.await_args.args[0]
    expected = Player.squad_number == non_existent_squad_number
    assert statement.whereclause.compare(expected)


@pytest.mark.anyio
async def test_update_by_squad_number_async_success(
    existing_player_request_model, existing_player_schema
):
    """Test the successful update of a player by Squad Number."""
    mock_session = AsyncMock(spec=AsyncSession)

    existing_player_request_model.first_name = "UpdatedFirstName"
    existing_player_request_model.middle_name = "UpdatedMiddleName"
    existing_player_request_model.last_name = "UpdatedLastName"
    existing_player_request_model.position = "UpdatedPosition"
    existing_player_request_model.abbr_position = "UPD"
    existing_player_request_model.team = "UpdatedTeam"
    existing_player_request_model.league = "UpdatedLeague"
    existing_player_request_model.starting11 = not existing_player_schema.starting11

    with patch(
        "services.player_service.retrieve_by_squad_number_async",
        new_callable=AsyncMock,
    ) as mock_retrieve:
        mock_retrieve.return_value = existing_player_schema

        result = await update_by_squad_number_async(
            mock_session,
            existing_player_schema.squad_number,
            existing_player_request_model,
        )

    assert result is True
    mock_retrieve.assert_awaited_once_with(
        mock_session, existing_player_schema.squad_number
    )
    mock_session.commit.assert_awaited_once()
    mock_session.rollback.assert_not_awaited()

    assert existing_player_schema.first_name == existing_player_request_model.first_name
    assert (
        existing_player_schema.middle_name == existing_player_request_model.middle_name
    )
    assert existing_player_schema.last_name == existing_player_request_model.last_name
    assert (
        existing_player_schema.date_of_birth
        == existing_player_request_model.date_of_birth
    )
    assert (
        existing_player_schema.squad_number
        == existing_player_request_model.squad_number
    )
    assert existing_player_schema.position == existing_player_request_model.position
    assert (
        existing_player_schema.abbr_position
        == existing_player_request_model.abbr_position
    )
    assert existing_player_schema.team == existing_player_request_model.team
    assert existing_player_schema.league == existing_player_request_model.league
    assert existing_player_schema.starting11 == existing_player_request_model.starting11


@pytest.mark.anyio
async def test_update_by_squad_number_async_not_found(
    existing_player_request_model,
):
    """Test the update of a player by Squad Number when the player does not exist."""
    mock_session = AsyncMock(spec=AsyncSession)
    non_existent_squad_number = 99

    with patch(
        "services.player_service.retrieve_by_squad_number_async",
        new_callable=AsyncMock,
    ) as mock_retrieve:
        mock_retrieve.return_value = None

        result = await update_by_squad_number_async(
            mock_session,
            non_existent_squad_number,
            existing_player_request_model,
        )

    assert result is False
    mock_retrieve.assert_awaited_once_with(mock_session, non_existent_squad_number)
    mock_session.commit.assert_not_awaited()
    mock_session.rollback.assert_not_awaited()


@pytest.mark.anyio
async def test_update_by_squad_number_async_database_error(
    existing_player_request_model, existing_player_schema
):
    """Test the update of a player by Squad Number when a database error occurs."""
    mock_session = AsyncMock(spec=AsyncSession)

    with patch(
        "services.player_service.retrieve_by_squad_number_async",
        new_callable=AsyncMock,
    ) as mock_retrieve:
        mock_retrieve.return_value = existing_player_schema
        mock_session.commit.side_effect = SQLAlchemyError("Connection timeout")

        result = await update_by_squad_number_async(
            mock_session,
            existing_player_schema.squad_number,
            existing_player_request_model,
        )

    assert result is False
    mock_retrieve.assert_awaited_once_with(
        mock_session, existing_player_schema.squad_number
    )
    mock_session.commit.assert_awaited_once()
    mock_session.rollback.assert_awaited_once()


@pytest.mark.anyio
async def test_delete_by_squad_number_async_success(existing_player_schema):
    """Test the successful deletion of a player by Squad Number."""
    mock_session = AsyncMock(spec=AsyncSession)

    with patch(
        "services.player_service.retrieve_by_squad_number_async",
        new_callable=AsyncMock,
    ) as mock_retrieve:
        mock_retrieve.return_value = existing_player_schema

        result = await delete_by_squad_number_async(
            mock_session,
            existing_player_schema.squad_number,
        )

    assert result is True
    mock_retrieve.assert_awaited_once_with(
        mock_session, existing_player_schema.squad_number
    )
    mock_session.delete.assert_awaited_once_with(existing_player_schema)
    mock_session.commit.assert_awaited_once()
    mock_session.rollback.assert_not_awaited()


@pytest.mark.anyio
async def test_delete_by_squad_number_async_not_found():
    """Test the deletion of a player by Squad Number when the player does not exist."""
    mock_session = AsyncMock(spec=AsyncSession)
    non_existent_squad_number = 99

    with patch(
        "services.player_service.retrieve_by_squad_number_async",
        new_callable=AsyncMock,
    ) as mock_retrieve:
        mock_retrieve.return_value = None

        result = await delete_by_squad_number_async(
            mock_session, non_existent_squad_number
        )

    assert result is False
    mock_retrieve.assert_awaited_once_with(mock_session, non_existent_squad_number)
    mock_session.delete.assert_not_awaited()
    mock_session.commit.assert_not_awaited()
    mock_session.rollback.assert_not_awaited()


@pytest.mark.anyio
async def test_delete_by_squad_number_async_database_error(existing_player_schema):
    """Test the deletion of a player by Squad Number when a database error occurs."""
    mock_session = AsyncMock(spec=AsyncSession)

    with patch(
        "services.player_service.retrieve_by_squad_number_async",
        new_callable=AsyncMock,
    ) as mock_retrieve:
        mock_retrieve.return_value = existing_player_schema
        mock_session.commit.side_effect = SQLAlchemyError("Connection timeout")

        result = await delete_by_squad_number_async(
            mock_session,
            existing_player_schema.squad_number,
        )

    assert result is False
    mock_retrieve.assert_awaited_once_with(
        mock_session, existing_player_schema.squad_number
    )
    mock_session.delete.assert_awaited_once_with(existing_player_schema)
    mock_session.commit.assert_awaited_once()
    mock_session.rollback.assert_awaited_once()
