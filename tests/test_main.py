# ------------------------------------------------------------------------------
# Test
# ------------------------------------------------------------------------------

from main import app
from fastapi.testclient import TestClient
import warnings
# Suppress the DeprecationWarning from httpx
warnings.filterwarnings("ignore", category=DeprecationWarning)

client = TestClient(app)
PATH = "/players/"

# GET --------------------------------------------------------------------------


def test_given_get_when_request_has_no_parameters_then_response_status_code_should_be_200_ok():
    response = client.get(PATH)
    assert response.status_code == 200


def test_given_get_when_request_has_no_parameters_then_response_body_should_be_collection_of_players():
    response = client.get(PATH)
    players = response.json()
    player_id = 0
    for player in players:
        player_id += 1
        assert player["id"] == player_id


def test_given_get_when_request_parameter_does_not_identify_a_player_then_response_status_code_should_be_404_not_found():
    player_id = 999
    response = client.get(PATH + str(player_id))
    assert response.status_code == 404


def test_given_get_when_request_parameter_identifies_existing_player_then_response_status_code_should_be_200_ok():
    player_id = 1
    response = client.get(PATH + str(player_id))
    assert response.status_code == 200


def test_given_get_when_request_parameter_identifies_existing_player_then_response_body_should_be_matching_player():
    player_id = 1
    response = client.get(PATH + str(player_id))
    player = response.json()
    assert player["id"] == player_id


def test_given_get_when_request_parameter_is_non_existing_squad_number_then_response_status_code_should_be_404_not_found():
    squad_number = 999
    response = client.get(PATH + "squadnumber" + "/" + str(squad_number))
    assert response.status_code == 404


def test_given_get_when_request_parameter_is_existing_squad_number_then_response_status_code_should_be_200_ok():
    squad_number = 10
    response = client.get(PATH + "squadnumber" + "/" + str(squad_number))
    assert response.status_code == 200


def test_given_get_when_request_parameter_is_existing_squad_number_then_response_body_should_be_matching_player():
    squad_number = 10
    response = client.get(PATH + "squadnumber" + "/" + str(squad_number))
    player = response.json()
    assert player["squadNumber"] == squad_number
