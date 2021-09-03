from fastapi.testclient import TestClient
from main import fast_api

client = TestClient(fast_api)


def test_get_songs_when_request_has_no_parameters_then_response_status_code_should_be_200_ok():
    response = client.get("/songs")
    assert response.status_code == 200


def test_get_songs_by_year_when_request_parameter_does_not_match_songs_then_response_status_code_should_be_404_not_found():
    response = client.get("/songs/year/42")
    assert response.status_code == 404


def test_get_songs_by_year_when_request_parameter_matches_songs_then_response_status_code_should_be_200_ok():
    response = client.get("/songs/year/1977")
    assert response.status_code == 200


def test_get_song_by_rank_when_request_parameter_does_not_match_song_then_response_status_code_should_be_404_not_found():
    response = client.get("/songs/rank/501")
    assert response.status_code == 404


def test_get_songs_by_rank_when_request_parameter_matches_song_then_response_status_code_should_be_200_ok():
    response = client.get("/songs/rank/10")
    assert response.status_code == 200
