# ------------------------------------------------------------------------------
# Test
# ------------------------------------------------------------------------------

import json
from tests.player_stub import existing_player, non_existing_player, unknown_player

PATH = "/players/"

# GET /players/ ----------------------------------------------------------------


def test_given_get_when_request_path_has_no_id_then_response_status_code_should_be_200_ok(client):
    response = client.get(PATH)
    assert response.status_code == 200


def test_given_get_when_request_path_has_no_id_then_response_body_should_be_collection_of_players(client):
    response = client.get(PATH)
    players = response.json()
    player_id = 0
    for player in players:
        player_id += 1
        assert player["id"] == player_id

# GET /players/{player_id} -----------------------------------------------------


def test_given_get_when_request_path_is_non_existing_id_then_response_status_code_should_be_404_not_found(client):
    player_id = 999
    response = client.get(PATH + str(player_id))
    assert response.status_code == 404


def test_given_get_when_request_path_is_existing_id_then_response_status_code_should_be_200_ok(client):
    player_id = 1
    response = client.get(PATH + str(player_id))
    assert response.status_code == 200


def test_given_get_when_request_path_is_existing_id_then_response_body_should_be_matching_player(client):
    player_id = 1
    response = client.get(PATH + str(player_id))
    player = response.json()
    assert player["id"] == player_id

# GET /players/squadnumber/{squad_number} --------------------------------------


def test_given_get_when_request_path_is_non_existing_squad_number_then_response_status_code_should_be_404_not_found(client):
    squad_number = 999
    response = client.get(PATH + "squadnumber" + "/" + str(squad_number))
    assert response.status_code == 404


def test_given_get_when_request_path_is_existing_squad_number_then_response_status_code_should_be_200_ok(client):
    squad_number = 10
    response = client.get(PATH + "squadnumber" + "/" + str(squad_number))
    assert response.status_code == 200


def test_given_get_when_request_path_is_existing_squad_number_then_response_body_should_be_matching_player(client):
    squad_number = 10
    response = client.get(PATH + "squadnumber" + "/" + str(squad_number))
    player = response.json()
    assert player["squadNumber"] == squad_number

# POST /players/ ---------------------------------------------------------------


def test_given_post_when_request_body_is_empty_then_response_status_code_should_be_422_unprocessable_entity(client):
    body = json.dumps({})
    response = client.post(PATH, data=body)
    assert response.status_code == 422


def test_given_post_when_request_body_is_existing_player_then_response_status_code_should_be_409_conflict(client):
    player = existing_player()
    body = json.dumps(player.__dict__)
    response = client.post(PATH, data=body)
    assert response.status_code == 409


def test_given_post_when_request_body_is_non_existing_player_then_response_status_code_should_be_201_created(client):
    player = non_existing_player()
    body = json.dumps(player.__dict__)
    response = client.post(PATH, data=body)
    assert response.status_code == 201

# PUT /players/{player_id} -----------------------------------------------------


def test_given_put_when_request_body_is_empty_then_response_status_code_should_be_422_unprocessable_entity(client):
    player_id = 1
    body = {}
    response = client.put(PATH + str(player_id), data=body)
    assert response.status_code == 422


def test_given_put_when_request_body_is_unknown_player_then_response_status_code_should_be_404_not_found(client):
    player_id = 999
    player = unknown_player()
    body = json.dumps(player.__dict__)
    response = client.put(PATH + str(player_id), data=body)
    assert response.status_code == 404


def test_given_put_when_request_body_is_existing_player_then_response_status_code_should_be_204_no_content(client):
    player_id = 1
    player = existing_player()
    player.first_name = "Emiliano"
    player.middle_name = ""
    body = json.dumps(player.__dict__)
    response = client.put(PATH + str(player_id), data=body)
    assert response.status_code == 204

# DELETE /players/{player_id} --------------------------------------------------


def test_given_delete_when_request_path_is_non_existing_id_then_response_status_code_should_be_404_not_found(client):
    player_id = 999
    response = client.delete(PATH + str(player_id))
    assert response.status_code == 404


def test_given_delete_when_request_path_is_existing_id_then_response_status_code_should_be__204_no_content(client):
    player_id = 12
    response = client.delete(PATH + str(player_id))
    assert response.status_code == 204
