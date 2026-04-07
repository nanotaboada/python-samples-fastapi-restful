"""
Test suite for the /players/ API endpoints.

Covers:
- GET    /health/
- GET    /players/
- GET    /players/{player_id}
- GET    /players/squadnumber/{squad_number}
- POST   /players/
- PUT    /players/squadnumber/{squad_number}
- DELETE /players/squadnumber/{squad_number}

Validates:
- Status codes, response bodies, headers (e.g., X-Cache)
- Handling of existing, nonexistent, and malformed requests
- Conflict and edge case behaviors
"""

from uuid import UUID

from tests.player_fake import (
    existing_player,
    nonexistent_player,
    unknown_player,
)

PATH = "/players/"


def _is_valid_uuid(value: str) -> bool:
    """Return True if value is a well-formed UUID string, False otherwise."""
    try:
        UUID(value)
        return True
    except ValueError:
        return False


# GET /health/ -----------------------------------------------------------------


def test_request_get_health_response_status_ok(client):
    """GET /health/ returns 200 OK"""
    # Act
    response = client.get("/health/")
    # Assert
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


# GET /players/ ----------------------------------------------------------------


def test_request_get_players_response_header_cache_miss(client):
    """GET /players/ initial request returns X-Cache: MISS"""
    # Act
    response = client.get(PATH)
    # Assert
    assert "X-Cache" in response.headers
    assert response.headers.get("X-Cache") == "MISS"


def test_request_get_players_response_header_cache_hit(client):
    """GET /players/ subsequent request returns X-Cache: HIT"""
    # Act
    client.get(PATH)  # initial
    response = client.get(PATH)  # subsequent (cached)
    # Assert
    assert "X-Cache" in response.headers
    assert response.headers.get("X-Cache") == "HIT"


def test_request_get_players_response_status_ok(client):
    """GET /players/ returns 200 OK"""
    # Act
    response = client.get(PATH)
    # Assert
    assert response.status_code == 200


def test_request_get_players_response_body_each_player_has_uuid(client):
    """GET /players/ returns players each containing a UUID id field"""
    # Act
    response = client.get(PATH)
    # Assert
    players = response.json()
    assert all(
        _is_valid_uuid(player["id"]) for player in players
    )  # UUID v5 (migration-seeded)


# GET /players/{player_id} -----------------------------------------------------


def test_request_get_player_id_unknown_response_status_not_found(client):
    """GET /players/{player_id} with unknown UUID returns 404 Not Found"""
    # Arrange
    player_id = unknown_player().id
    # Act
    response = client.get(PATH + str(player_id))
    # Assert
    assert response.status_code == 404


def test_request_get_player_id_existing_response_status_ok(client):
    """GET /players/{player_id} with existing ID returns 200 OK"""
    # Arrange
    player_id = existing_player().id
    # Act
    response = client.get(PATH + str(player_id))
    # Assert
    assert response.status_code == 200


def test_request_get_player_id_existing_response_body_player_match(client):
    """GET /players/{player_id} with existing ID returns matching player"""
    # Arrange
    player_id = existing_player().id
    # Act
    response = client.get(PATH + str(player_id))
    # Assert
    player = response.json()
    assert player["id"] == str(player_id)


# GET /players/squadnumber/{squad_number} --------------------------------------


def test_request_get_player_squadnumber_nonexistent_response_status_not_found(client):
    """GET /players/squadnumber/{squad_number} with nonexistent number returns 404 Not Found"""
    # Arrange
    squad_number = nonexistent_player().squad_number
    # Act
    response = client.get(PATH + "squadnumber" + "/" + str(squad_number))
    # Assert
    assert response.status_code == 404


def test_request_get_player_squadnumber_existing_response_status_ok(client):
    """GET /players/squadnumber/{squad_number} with existing number returns 200 OK"""
    # Arrange
    squad_number = existing_player().squad_number
    # Act
    response = client.get(PATH + "squadnumber" + "/" + str(squad_number))
    # Assert
    assert response.status_code == 200


def test_request_get_player_squadnumber_existing_response_body_player_match(client):
    """GET /players/squadnumber/{squad_number} with existing number returns matching player"""
    # Arrange
    squad_number = existing_player().squad_number
    # Act
    response = client.get(PATH + "squadnumber" + "/" + str(squad_number))
    # Assert
    player = response.json()
    assert player["squadNumber"] == squad_number


# POST /players/ ---------------------------------------------------------------


def test_request_post_player_body_empty_response_status_unprocessable(client):
    """POST /players/ with empty body returns 422 Unprocessable Entity"""
    # Act
    response = client.post(PATH, json={})
    # Assert
    assert response.status_code == 422


def test_request_post_player_body_existing_response_status_conflict(client):
    """POST /players/ with existing player returns 409 Conflict"""
    # Arrange
    player = existing_player()
    # Act
    response = client.post(PATH, json=player.__dict__)
    # Assert
    assert response.status_code == 409


def test_request_post_player_body_existing_response_body_detail(client):
    """POST /players/ with existing player returns 409 with detail message"""
    # Arrange
    player = existing_player()
    # Act
    response = client.post(PATH, json=player.__dict__)
    # Assert
    assert (
        response.json()["detail"] == "A Player with this squad number already exists."
    )


def test_request_post_player_body_nonexistent_response_status_created(client):
    """POST /players/ with nonexistent player returns 201 Created with a valid UUID"""
    # Arrange
    player = nonexistent_player()
    try:
        # Act
        response = client.post(PATH, json=player.__dict__)
        # Assert
        assert response.status_code == 201
        body = response.json()
        assert "id" in body
        assert UUID(body["id"]).version == 4  # UUID v4 (API-created)
    finally:
        # Teardown — remove the created player
        client.delete(PATH + "squadnumber/" + str(player.squad_number))


# PUT /players/squadnumber/{squad_number} --------------------------------------


def test_request_put_player_squadnumber_existing_body_empty_response_status_unprocessable(
    client,
):
    """PUT /players/squadnumber/{squad_number} with empty body returns 422 Unprocessable Entity"""
    # Arrange
    squad_number = existing_player().squad_number
    # Act
    response = client.put(PATH + "squadnumber/" + str(squad_number), json={})
    # Assert
    assert response.status_code == 422


def test_request_put_player_squadnumber_unknown_response_status_not_found(client):
    """PUT /players/squadnumber/{squad_number} with unknown number returns 404 Not Found"""
    # Arrange
    squad_number = unknown_player().squad_number
    player = unknown_player()
    # Act
    response = client.put(
        PATH + "squadnumber/" + str(squad_number), json=player.__dict__
    )
    # Assert
    assert response.status_code == 404


def test_request_put_player_squadnumber_existing_response_status_no_content(client):
    """PUT /players/squadnumber/{squad_number} with existing number returns 204 No Content"""
    # Arrange
    squad_number = existing_player().squad_number
    player = existing_player()
    player.first_name = "Emiliano"
    player.middle_name = None
    try:
        # Act
        response = client.put(
            PATH + "squadnumber/" + str(squad_number), json=player.__dict__
        )
        # Assert
        assert response.status_code == 204
    finally:
        # Teardown — restore Damián Martínez to its seeded state
        seed = existing_player()
        client.put(PATH + "squadnumber/" + str(seed.squad_number), json=seed.__dict__)


def test_request_put_player_squadnumber_mismatch_response_status_bad_request(client):
    """PUT /players/squadnumber/{squad_number} with mismatched squad number in body returns 400 Bad Request"""
    # Arrange
    squad_number = existing_player().squad_number
    player = existing_player()
    player.squad_number = unknown_player().squad_number
    # Act
    response = client.put(
        PATH + "squadnumber/" + str(squad_number), json=player.__dict__
    )
    # Assert
    assert response.status_code == 400


# DELETE /players/squadnumber/{squad_number} -----------------------------------


def test_request_delete_player_squadnumber_unknown_response_status_not_found(client):
    """DELETE /players/squadnumber/{squad_number} with unknown number returns 404 Not Found"""
    # Arrange
    squad_number = unknown_player().squad_number
    # Act
    response = client.delete(PATH + "squadnumber/" + str(squad_number))
    # Assert
    assert response.status_code == 404


def test_request_delete_player_squadnumber_existing_response_status_no_content(
    client, nonexistent_player_in_db
):
    """DELETE /players/squadnumber/{squad_number} with existing number returns 204 No Content"""
    # Arrange
    player = nonexistent_player_in_db
    # Act
    response = client.delete(PATH + "squadnumber/" + str(player.squad_number))
    # Assert
    assert response.status_code == 204


def test_request_post_player_body_nonexistent_response_header_location(client):
    """POST /players/ with nonexistent player returns 201 with Location header"""
    # Arrange
    player = nonexistent_player()
    try:
        # Act
        response = client.post(PATH, json=player.__dict__)
        # Assert
        assert response.status_code == 201
        assert "Location" in response.headers
        assert (
            response.headers["Location"]
            == f"/players/squadnumber/{player.squad_number}"
        )
    finally:
        client.delete(PATH + "squadnumber/" + str(player.squad_number))
