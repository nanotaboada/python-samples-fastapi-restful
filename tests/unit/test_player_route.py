"""
Unit tests for the Player API routes.
"""

from unittest.mock import AsyncMock, patch
from uuid import UUID

import pytest
from fastapi import HTTPException, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from models.player_model import PlayerRequestModel
from routes.player_route import (
    CACHE_KEY,
    CACHE_TTL,
    delete_async,
    get_all_async,
    get_by_id_async,
    get_by_squad_number_async,
    post_async,
    put_async,
    simple_memory_cache,
)
from schemas.player_schema import Player


@pytest.fixture
def existing_player_schema():
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


@pytest.fixture
def player_request_model():
    return PlayerRequestModel(
        first_name="Giovani",
        last_name="Lo Celso",
        date_of_birth="1996-07-09T00:00:00.000Z",
        squad_number=27,
        position="Central Midfield",
        abbr_position="CM",
        team="Real Betis Balompié",
        league="La Liga",
        starting11=False,
    )


@pytest.fixture
def player_schema():
    return Player(
        first_name="Giovani",
        last_name="Lo Celso",
        date_of_birth="1996-07-09T00:00:00.000Z",
        squad_number=27,
        position="Central Midfield",
        abbr_position="CM",
        team="Real Betis Balompié",
        league="La Liga",
        starting11=False,
    )


@pytest.mark.anyio
async def test_request_post_player_body_nonexistent_response_created(
    player_request_model, player_schema
):
    """Create a player when the squad number does not already exist."""
    mock_async_session = AsyncMock(spec=AsyncSession)
    response = Response()

    with (
        patch(
            "routes.player_route.player_service.retrieve_by_squad_number_async",
            new_callable=AsyncMock,
        ) as mock_retrieve,
        patch(
            "routes.player_route.player_service.create_async",
            new_callable=AsyncMock,
        ) as mock_create,
        patch.object(
            simple_memory_cache, "clear", new_callable=AsyncMock
        ) as mock_clear_cache,
    ):
        mock_retrieve.return_value = None
        mock_create.return_value = player_schema

        result = await post_async(
            player_model=player_request_model,
            async_session=mock_async_session,
            response=response,
        )

    assert result == player_schema
    mock_retrieve.assert_awaited_once_with(
        mock_async_session, player_request_model.squad_number
    )
    mock_create.assert_awaited_once_with(mock_async_session, player_request_model)
    assert (
        response.headers["Location"]
        == f"/players/squadnumber/{player_request_model.squad_number}"
    )
    mock_clear_cache.assert_awaited_once_with(CACHE_KEY)


@pytest.mark.anyio
async def test_request_post_player_body_existing_response_conflict(
    player_request_model, player_schema
):
    """Reject player creation when the squad number already exists."""
    mock_async_session = AsyncMock(spec=AsyncSession)
    response = Response()

    with (
        patch(
            "routes.player_route.player_service.retrieve_by_squad_number_async",
            new_callable=AsyncMock,
        ) as mock_retrieve,
        patch(
            "routes.player_route.player_service.create_async",
            new_callable=AsyncMock,
        ) as mock_create,
        patch.object(
            simple_memory_cache, "clear", new_callable=AsyncMock
        ) as mock_clear_cache,
    ):
        mock_retrieve.return_value = player_schema

        with pytest.raises(HTTPException) as exc_info:
            await post_async(
                player_model=player_request_model,
                async_session=mock_async_session,
                response=response,
            )

    assert exc_info.value.status_code == status.HTTP_409_CONFLICT
    assert exc_info.value.detail == "A Player with this squad number already exists."
    mock_retrieve.assert_awaited_once_with(
        mock_async_session, player_request_model.squad_number
    )
    mock_create.assert_not_awaited()
    mock_clear_cache.assert_not_awaited()


@pytest.mark.anyio
async def test_request_post_player_body_service_failure_response_server_error(
    player_request_model,
):
    """Raise a server error when player creation fails."""
    mock_async_session = AsyncMock(spec=AsyncSession)
    response = Response()

    with (
        patch(
            "routes.player_route.player_service.retrieve_by_squad_number_async",
            new_callable=AsyncMock,
        ) as mock_retrieve,
        patch(
            "routes.player_route.player_service.create_async",
            new_callable=AsyncMock,
        ) as mock_create,
        patch.object(
            simple_memory_cache, "clear", new_callable=AsyncMock
        ) as mock_clear_cache,
    ):
        mock_retrieve.return_value = None
        mock_create.return_value = None

        with pytest.raises(HTTPException) as exc_info:
            await post_async(
                player_model=player_request_model,
                async_session=mock_async_session,
                response=response,
            )

    assert exc_info.value.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert (
        exc_info.value.detail == "Failed to create the Player due to a database error."
    )
    mock_retrieve.assert_awaited_once_with(
        mock_async_session, player_request_model.squad_number
    )
    mock_create.assert_awaited_once_with(mock_async_session, player_request_model)
    mock_clear_cache.assert_not_awaited()


@pytest.mark.anyio
async def test_request_get_players_cache_hit_response_success(player_schema):
    """Return cached players without querying the service."""
    mock_async_session = AsyncMock(spec=AsyncSession)
    response = Response()

    with (
        patch.object(
            simple_memory_cache, "get", new_callable=AsyncMock
        ) as mock_get_cache,
        patch(
            "routes.player_route.player_service.retrieve_all_async",
            new_callable=AsyncMock,
        ) as mock_retrieve_all,
    ):
        mock_get_cache.return_value = [player_schema]

        result = await get_all_async(
            response=response, async_session=mock_async_session
        )

    assert result == [player_schema]
    assert response.headers["X-Cache"] == "HIT"
    mock_get_cache.assert_awaited_once_with(CACHE_KEY)
    mock_retrieve_all.assert_not_awaited()


@pytest.mark.anyio
async def test_request_get_players_cache_miss_response_success(player_schema):
    """Retrieve and cache players when the cache misses."""
    mock_async_session = AsyncMock(spec=AsyncSession)
    response = Response()

    with (
        patch.object(
            simple_memory_cache, "get", new_callable=AsyncMock
        ) as mock_get_cache,
        patch(
            "routes.player_route.player_service.retrieve_all_async",
            new_callable=AsyncMock,
        ) as mock_retrieve_all,
        patch.object(
            simple_memory_cache, "set", new_callable=AsyncMock
        ) as mock_set_cache,
    ):
        mock_get_cache.return_value = None
        mock_retrieve_all.return_value = [player_schema]

        result = await get_all_async(
            response=response, async_session=mock_async_session
        )

    assert result == [player_schema]
    assert response.headers["X-Cache"] == "MISS"
    mock_get_cache.assert_awaited_once_with(CACHE_KEY)
    mock_retrieve_all.assert_awaited_once_with(mock_async_session)
    mock_set_cache.assert_awaited_once_with(CACHE_KEY, [player_schema], ttl=CACHE_TTL)


@pytest.mark.anyio
async def test_request_get_player_id_existing_response_success(existing_player_schema):
    """Return a player when the requested ID exists."""
    mock_async_session = AsyncMock(spec=AsyncSession)

    with patch(
        "routes.player_route.player_service.retrieve_by_id_async",
        new_callable=AsyncMock,
    ) as mock_retrieve_by_id:
        mock_retrieve_by_id.return_value = existing_player_schema

        result = await get_by_id_async(
            player_id=existing_player_schema.id,
            async_session=mock_async_session,
        )

    assert result == existing_player_schema
    mock_retrieve_by_id.assert_awaited_once_with(
        mock_async_session, existing_player_schema.id
    )


@pytest.mark.anyio
async def test_request_get_player_id_unknown_response_not_found():
    """Raise not found when the requested ID does not exist."""
    mock_async_session = AsyncMock(spec=AsyncSession)
    unknown_player_id = UUID("00000000-0000-0000-0000-000000000000")

    with patch(
        "routes.player_route.player_service.retrieve_by_id_async",
        new_callable=AsyncMock,
    ) as mock_retrieve_by_id:
        mock_retrieve_by_id.return_value = None

        with pytest.raises(HTTPException) as exc_info:
            await get_by_id_async(
                player_id=unknown_player_id,
                async_session=mock_async_session,
            )

    assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
    mock_retrieve_by_id.assert_awaited_once_with(mock_async_session, unknown_player_id)


@pytest.mark.anyio
async def test_request_get_player_squadnumber_existing_response_success(
    existing_player_schema,
):
    """Return a player when the squad number exists."""
    mock_async_session = AsyncMock(spec=AsyncSession)

    with patch(
        "routes.player_route.player_service.retrieve_by_squad_number_async",
        new_callable=AsyncMock,
    ) as mock_retrieve_by_squad_number:
        mock_retrieve_by_squad_number.return_value = existing_player_schema

        result = await get_by_squad_number_async(
            squad_number=existing_player_schema.squad_number,
            async_session=mock_async_session,
        )

    assert result == existing_player_schema
    mock_retrieve_by_squad_number.assert_awaited_once_with(
        mock_async_session, existing_player_schema.squad_number
    )


@pytest.mark.anyio
async def test_request_get_player_squadnumber_unknown_response_not_found():
    """Raise not found when the squad number does not exist."""
    mock_async_session = AsyncMock(spec=AsyncSession)
    unknown_squad_number = 99

    with patch(
        "routes.player_route.player_service.retrieve_by_squad_number_async",
        new_callable=AsyncMock,
    ) as mock_retrieve_by_squad_number:
        mock_retrieve_by_squad_number.return_value = None

        with pytest.raises(HTTPException) as exc_info:
            await get_by_squad_number_async(
                squad_number=unknown_squad_number,
                async_session=mock_async_session,
            )

    assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
    mock_retrieve_by_squad_number.assert_awaited_once_with(
        mock_async_session, unknown_squad_number
    )


@pytest.mark.anyio
async def test_request_put_player_squadnumber_existing_response_no_content(
    existing_player_schema, player_request_model
):
    """Update a player when the squad number matches."""
    player_request_model.squad_number = existing_player_schema.squad_number
    mock_async_session = AsyncMock(spec=AsyncSession)

    with (
        patch(
            "routes.player_route.player_service.retrieve_by_squad_number_async",
            new_callable=AsyncMock,
        ) as mock_retrieve_by_squad_number,
        patch(
            "routes.player_route.player_service.update_by_squad_number_async",
            new_callable=AsyncMock,
        ) as mock_update,
        patch.object(
            simple_memory_cache, "clear", new_callable=AsyncMock
        ) as mock_clear_cache,
    ):
        mock_retrieve_by_squad_number.return_value = existing_player_schema
        mock_update.return_value = True

        result = await put_async(
            squad_number=existing_player_schema.squad_number,
            player_model=player_request_model,
            async_session=mock_async_session,
        )

    assert result is None
    mock_retrieve_by_squad_number.assert_awaited_once_with(
        mock_async_session, existing_player_schema.squad_number
    )
    mock_update.assert_awaited_once_with(
        mock_async_session, existing_player_schema.squad_number, player_request_model
    )
    mock_clear_cache.assert_awaited_once_with(CACHE_KEY)


@pytest.mark.anyio
async def test_request_put_player_squadnumber_mismatch_response_bad_request(
    existing_player_schema, player_request_model
):
    """Reject an update when the URL and body squad numbers differ."""
    player_request_model.squad_number = existing_player_schema.squad_number + 1
    mock_async_session = AsyncMock(spec=AsyncSession)

    with (
        patch(
            "routes.player_route.player_service.retrieve_by_squad_number_async",
            new_callable=AsyncMock,
        ) as mock_retrieve_by_squad_number,
        patch(
            "routes.player_route.player_service.update_by_squad_number_async",
            new_callable=AsyncMock,
        ) as mock_update,
        patch.object(
            simple_memory_cache, "clear", new_callable=AsyncMock
        ) as mock_clear_cache,
    ):
        mock_retrieve_by_squad_number.return_value = existing_player_schema

        with pytest.raises(HTTPException) as exc_info:
            await put_async(
                squad_number=existing_player_schema.squad_number,
                player_model=player_request_model,
                async_session=mock_async_session,
            )

    assert exc_info.value.status_code == status.HTTP_400_BAD_REQUEST
    mock_retrieve_by_squad_number.assert_not_awaited()
    mock_update.assert_not_awaited()
    mock_clear_cache.assert_not_awaited()


@pytest.mark.anyio
async def test_request_put_player_squadnumber_unknown_response_not_found(
    player_request_model,
):
    """Raise not found when the player does not exist."""
    mock_async_session = AsyncMock(spec=AsyncSession)

    with (
        patch(
            "routes.player_route.player_service.retrieve_by_squad_number_async",
            new_callable=AsyncMock,
        ) as mock_retrieve_by_squad_number,
        patch(
            "routes.player_route.player_service.update_by_squad_number_async",
            new_callable=AsyncMock,
        ) as mock_update,
        patch.object(
            simple_memory_cache, "clear", new_callable=AsyncMock
        ) as mock_clear_cache,
    ):
        mock_retrieve_by_squad_number.return_value = None

        with pytest.raises(HTTPException) as exc_info:
            await put_async(
                squad_number=player_request_model.squad_number,
                player_model=player_request_model,
                async_session=mock_async_session,
            )

    assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
    mock_retrieve_by_squad_number.assert_awaited_once_with(
        mock_async_session, player_request_model.squad_number
    )
    mock_update.assert_not_awaited()
    mock_clear_cache.assert_not_awaited()


@pytest.mark.anyio
async def test_request_put_player_squadnumber_service_failure_response_server_error(
    existing_player_schema, player_request_model
):
    """Raise a server error when player update fails."""
    player_request_model.squad_number = existing_player_schema.squad_number
    mock_async_session = AsyncMock(spec=AsyncSession)

    with (
        patch(
            "routes.player_route.player_service.retrieve_by_squad_number_async",
            new_callable=AsyncMock,
        ) as mock_retrieve_by_squad_number,
        patch(
            "routes.player_route.player_service.update_by_squad_number_async",
            new_callable=AsyncMock,
        ) as mock_update,
        patch.object(
            simple_memory_cache, "clear", new_callable=AsyncMock
        ) as mock_clear_cache,
    ):
        mock_retrieve_by_squad_number.return_value = existing_player_schema
        mock_update.return_value = False

        with pytest.raises(HTTPException) as exc_info:
            await put_async(
                squad_number=existing_player_schema.squad_number,
                player_model=player_request_model,
                async_session=mock_async_session,
            )

    assert exc_info.value.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert (
        exc_info.value.detail == "Failed to update the Player due to a database error."
    )
    mock_retrieve_by_squad_number.assert_awaited_once_with(
        mock_async_session, existing_player_schema.squad_number
    )
    mock_update.assert_awaited_once_with(
        mock_async_session, existing_player_schema.squad_number, player_request_model
    )
    mock_clear_cache.assert_not_awaited()


@pytest.mark.anyio
async def test_request_delete_player_squadnumber_existing_response_no_content(
    existing_player_schema,
):
    """Delete a player when the squad number exists."""
    mock_async_session = AsyncMock(spec=AsyncSession)

    with (
        patch(
            "routes.player_route.player_service.retrieve_by_squad_number_async",
            new_callable=AsyncMock,
        ) as mock_retrieve_by_squad_number,
        patch(
            "routes.player_route.player_service.delete_by_squad_number_async",
            new_callable=AsyncMock,
        ) as mock_delete,
        patch.object(
            simple_memory_cache, "clear", new_callable=AsyncMock
        ) as mock_clear_cache,
    ):
        mock_retrieve_by_squad_number.return_value = existing_player_schema
        mock_delete.return_value = True

        result = await delete_async(
            squad_number=existing_player_schema.squad_number,
            async_session=mock_async_session,
        )

    assert result is None
    mock_retrieve_by_squad_number.assert_awaited_once_with(
        mock_async_session, existing_player_schema.squad_number
    )
    mock_delete.assert_awaited_once_with(
        mock_async_session, existing_player_schema.squad_number
    )
    mock_clear_cache.assert_awaited_once_with(CACHE_KEY)


@pytest.mark.anyio
async def test_request_delete_player_squadnumber_unknown_response_not_found():
    """Raise not found when the player does not exist."""
    mock_async_session = AsyncMock(spec=AsyncSession)
    unknown_squad_number = 99

    with (
        patch(
            "routes.player_route.player_service.retrieve_by_squad_number_async",
            new_callable=AsyncMock,
        ) as mock_retrieve_by_squad_number,
        patch(
            "routes.player_route.player_service.delete_by_squad_number_async",
            new_callable=AsyncMock,
        ) as mock_delete,
        patch.object(
            simple_memory_cache, "clear", new_callable=AsyncMock
        ) as mock_clear_cache,
    ):
        mock_retrieve_by_squad_number.return_value = None

        with pytest.raises(HTTPException) as exc_info:
            await delete_async(
                squad_number=unknown_squad_number,
                async_session=mock_async_session,
            )

    assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
    mock_retrieve_by_squad_number.assert_awaited_once_with(
        mock_async_session, unknown_squad_number
    )
    mock_delete.assert_not_awaited()
    mock_clear_cache.assert_not_awaited()


@pytest.mark.anyio
async def test_request_delete_player_squadnumber_service_failure_response_server_error(
    existing_player_schema,
):
    """Raise a server error when player deletion fails."""
    mock_async_session = AsyncMock(spec=AsyncSession)

    with (
        patch(
            "routes.player_route.player_service.retrieve_by_squad_number_async",
            new_callable=AsyncMock,
        ) as mock_retrieve_by_squad_number,
        patch(
            "routes.player_route.player_service.delete_by_squad_number_async",
            new_callable=AsyncMock,
        ) as mock_delete,
        patch.object(
            simple_memory_cache, "clear", new_callable=AsyncMock
        ) as mock_clear_cache,
    ):
        mock_retrieve_by_squad_number.return_value = existing_player_schema
        mock_delete.return_value = False

        with pytest.raises(HTTPException) as exc_info:
            await delete_async(
                squad_number=existing_player_schema.squad_number,
                async_session=mock_async_session,
            )

    assert exc_info.value.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert (
        exc_info.value.detail == "Failed to delete the Player due to a database error."
    )
    mock_retrieve_by_squad_number.assert_awaited_once_with(
        mock_async_session, existing_player_schema.squad_number
    )
    mock_delete.assert_awaited_once_with(
        mock_async_session, existing_player_schema.squad_number
    )
    mock_clear_cache.assert_not_awaited()
