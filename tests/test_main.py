# test_main.py

from fastapi.testclient import TestClient
from main import fast_api

client = TestClient(fast_api)

# GET /songs


def test_when_request_has_no_parameters_then_response_status_code_should_be_200_ok():
    response = client.get("/songs")
    assert response.status_code == 200

# GET /songs/year/{year}


def test_when_request_parameter_does_not_match_any_year_then_response_status_code_should_be_404_not_found():
    response = client.get("/songs/year/1776")
    assert response.status_code == 404


def test_when_request_parameter_matches_a_year_then_response_status_code_should_be_200_ok():
    response = client.get("/songs/year/1977")
    assert response.status_code == 200


def test_when_request_parameter_matches_a_year_then_response_body_should_contain_songs_from_that_year():
    response = client.get("/songs/year/1977")
    songs = response.json()
    for song in songs:
        assert song["year"] == "1977"

# GET /songs/rank/{rank}


def test_when_request_parameter_does_not_match_any_rank_then_response_status_code_should_be_404_not_found():
    response = client.get("/songs/rank/501")
    assert response.status_code == 404


def test_when_request_parameter_matches_a_rank_then_response_status_code_should_be_200_ok():
    response = client.get("/songs/rank/42")
    assert response.status_code == 200


def test_when_request_parameter_matches_a_rank_then_response_body_should_contain_the_song_with_such_rank():
    response = client.get("/songs/rank/42")
    song = response.json()
    assert song["rank"] == 42
