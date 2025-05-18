# ------------------------------------------------------------------------------
# Test
# ------------------------------------------------------------------------------

import json
from tests.player_stub import existing_player, nonexistent_player, unknown_player

PATH = "/players/"

# GET /health/ -----------------------------------------------------------------

def test_given_get_when_request_path_is_health_then_response_status_code_should_be_200_ok(client):
    """
        Given   GET /health/
        when    request
        then    response Status Code should be 200 OK
    """
    # Act
    response = client.get("/health/")
    # Assert
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

# GET /players/ ----------------------------------------------------------------


def test_given_get_when_request_is_initial_then_response_header_x_cache_should_be_miss(client):
    """
        Given   GET /players/
        when    request is initial
        then    response Header X-Cache value should be MISS
    """
    # Act
    response = client.get(PATH)

    # Assert
    assert "X-Cache" in response.headers
    assert response.headers.get("X-Cache") == "MISS"

def test_given_get_when_request_is_subsequent_then_response_header_x_cache_should_be_hit(client):
    """
        Given   GET /players/
        when    request is subsequent
        then    response Header X-Cache should be HIT
    """
    # Act
    client.get(PATH) # initial
    response = client.get(PATH) # subsequent (cached)

    # Assert
    assert "X-Cache" in response.headers
    assert response.headers.get("X-Cache") == "HIT"

def test_given_get_when_request_path_has_no_id_then_response_status_code_should_be_200_ok(client):
    """
        Given   GET /players/
        when    request path has no ID
        then    response Status Code should be 200 OK
    """
    # Act
    response = client.get(PATH)
    # Assert
    assert response.status_code == 200


def test_given_get_when_request_path_has_no_id_then_response_body_should_be_collection_of_players(client):
    """
        Given   GET /players/
        when    request path has no ID
        then    response Body should be collection of players
    """
    # Act
    response = client.get(PATH)
    # Assert
    players = response.json()
    player_id = 0
    for player in players:
        player_id += 1
        assert player["id"] == player_id

# GET /players/{player_id} -----------------------------------------------------


def test_given_get_when_request_path_is_nonexistent_id_then_response_status_code_should_be_404_not_found(client):
    """
        Given   GET /players/{player_id}
        when    request path is nonexistent ID
        then    response Status Code should be 404 (Not Found)
    """
    # Arrange
    player_id = nonexistent_player().id
    # Act
    response = client.get(PATH + str(player_id))
    # Assert
    assert response.status_code == 404


def test_given_get_when_request_path_is_existing_id_then_response_status_code_should_be_200_ok(client):
    """
        Given   GET /players/{player_id}
        when    request path is existing ID
        then    response Status Code should be 200 (OK)
    """
    # Arrange
    player_id = existing_player().id
    # Act
    response = client.get(PATH + str(player_id))
    # Assert
    assert response.status_code == 200


def test_given_get_when_request_path_is_existing_id_then_response_body_should_be_matching_player(client):
    """
        Given   GET /players/{player_id}
        when    request path is existing ID
        then    response body should be matching Player
    """
    # Arrange
    player_id = existing_player().id
    # Act
    response = client.get(PATH + str(player_id))
    # Assert
    player = response.json()
    assert player["id"] == player_id

# GET /players/squadnumber/{squad_number} --------------------------------------


def test_given_get_when_request_path_is_nonexistent_squad_number_then_response_status_code_should_be_404_not_found(client):
    """
        Given   GET /players/squadnumber/{squad_number}
        when    request path is nonexistent Squad Number
        then    response Status Code should be 404 (Not Found)
    """
    # Arrange
    squad_number = nonexistent_player().squad_number
    # Act
    response = client.get(PATH + "squadnumber" + "/" + str(squad_number))
    # Assert
    assert response.status_code == 404


def test_given_get_when_request_path_is_existing_squad_number_then_response_status_code_should_be_200_ok(client):
    """
        Given   GET /players/squadnumber/{squad_number}
        when    request path is existing Squad Number
        then    response Status Code should be 200 (OK)
    """
    # Arrange
    squad_number = existing_player().squad_number
    # Act
    response = client.get(PATH + "squadnumber" + "/" + str(squad_number))
    # Assert
    assert response.status_code == 200


def test_given_get_when_request_path_is_existing_squad_number_then_response_body_should_be_matching_player(client):
    """
        Given   GET /players/squadnumber/{squad_number}
        when    request path is existing Squad Number
        then    response body should be matching Player
    """
    # Arrange
    squad_number = existing_player().squad_number
    # Act
    response = client.get(PATH + "squadnumber" + "/" + str(squad_number))
    # Assert
    player = response.json()
    assert player["squadNumber"] == squad_number

# POST /players/ ---------------------------------------------------------------


def test_given_post_when_request_body_is_empty_then_response_status_code_should_be_422_unprocessable_entity(client):
    """
        Given   POST /players/
        when    request body is empty
        then    response Status Code should be 422 (Unprocessable Entity)
    """
    # Arrange
    body = {}
    # Act
    response = client.post(PATH, data=body)
    # Assert
    assert response.status_code == 422


def test_given_post_when_request_body_is_existing_player_then_response_status_code_should_be_409_conflict(client):
    """
        Given   POST /players/
        when    request body is existing Player
        then    response Status Code should be 409 (Conflict)
    """
    # Arrange
    player = existing_player()
    body = json.dumps(player.__dict__)
    # Act
    response = client.post(PATH, data=body)
    # Assert
    assert response.status_code == 409


def test_given_post_when_request_body_is_nonexistent_player_then_response_status_code_should_be_201_created(client):
    """
        Given   POST /players/
        when    request body is nonexistent Player
        then    response Status Code should be 201 (Created)
    """
    # Arrange
    player = nonexistent_player()
    body = json.dumps(player.__dict__)
    # Act
    response = client.post(PATH, data=body)
    # Assert
    assert response.status_code == 201

# PUT /players/{player_id} -----------------------------------------------------


def test_given_put_when_request_body_is_empty_then_response_status_code_should_be_422_unprocessable_entity(client):
    """
        Given   PUT /players/{player_id}
        when    request body is empty
        then    response Status Code should be 422 (Unprocessable Entity)
    """
    # Arrange
    player_id = existing_player().id
    body = {}
    # Act
    response = client.put(PATH + str(player_id), data=body)
    # Assert
    assert response.status_code == 422


def test_given_put_when_request_path_is_unknown_id_then_response_status_code_should_be_404_not_found(client):
    """
        Given   PUT /players/{player_id}
        when    request path is unknown ID
        then    response Status Code should be 404 (Not Found)
    """
    # Arrange
    player_id = unknown_player().id
    player = unknown_player()
    body = json.dumps(player.__dict__)
    # Act
    response = client.put(PATH + str(player_id), data=body)
    # Assert
    assert response.status_code == 404


def test_given_put_when_request_path_is_existing_id_then_response_status_code_should_be_204_no_content(client):
    """
        Given   PUT /players/{player_id}
        when    request path is existing ID
        then    response Status Code should be 204 (No Content)
    """
    # Arrange
    player_id = existing_player().id
    player = existing_player()
    player.first_name = "Emiliano"
    player.middle_name = ""
    body = json.dumps(player.__dict__)
    # Act
    response = client.put(PATH + str(player_id), data=body)
    # Assert
    assert response.status_code == 204

# DELETE /players/{player_id} --------------------------------------------------


def test_given_delete_when_request_path_is_unknown_id_then_response_status_code_should_be_404_not_found(client):
    """
        Given   DELETE /players/{player_id}
        when    request path is unknown ID
        then    response Status Code should be 404 (Not Found)
    """
    # Arrange
    player_id = unknown_player().id
    # Act
    response = client.delete(PATH + str(player_id))
    # Assert
    assert response.status_code == 404


def test_given_delete_when_request_path_is_existing_id_then_response_status_code_should_be__204_no_content(client):
    """
        Given   DELETE /players/{player_id}
        when    request path is existing ID
        then    response Status Code should be 204 (No Content)
    """
    # Arrange
    player_id = 12  # nonexistent_player() previously created
    # Act
    response = client.delete(PATH + str(player_id))
    # Assert
    assert response.status_code == 204
