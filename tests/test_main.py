# test_main.py

from fastapi.testclient import TestClient
from main import fast_api

client = TestClient(fast_api)


# -----------------------------------------------------------------------------------------------------------------------------
# GET /songs
# -----------------------------------------------------------------------------------------------------------------------------


def test_when_request_has_no_param_then_response_status_code_should_be_200_ok():
    response = client.get("/songs")
    assert response.status_code == 200


def test_when_request_has_no_param_then_response_body_should_contain_all_songs():
    response = client.get("/songs")
    songs = response.json()
    rank = 0
    for song in songs:
        rank += 1
        assert song["rank"] == rank


# -----------------------------------------------------------------------------------------------------------------------------
# GET /songs/year/{year}
# -----------------------------------------------------------------------------------------------------------------------------


def test_when_request_param_out_of_range_of_years_then_response_status_code_should_be_422_unprocessable_entity():
    response = client.get("/songs/year/1234")
    assert response.status_code == 422


def test_when_request_param_within_range_of_years_but_does_not_match_songs_then_response_status_code_should_be_404_not_found():
    response = client.get("/songs/year/1999")  # Verified against collection that there are no songs from 1999
    assert response.status_code == 404


def test_when_request_param_within_range_of_years_and_matches_songs_then_response_status_code_should_be_200_ok():
    response = client.get("/songs/year/1977")
    assert response.status_code == 200


def test_when_request_param_within_range_of_years_and_matches_songs_then_response_body_should_contain_songs_from_that_year():
    response = client.get("/songs/year/1977")
    songs = response.json()
    for song in songs:
        assert song["year"] == 1977


# -----------------------------------------------------------------------------------------------------------------------------
# GET /songs/rank/{rank}
# -----------------------------------------------------------------------------------------------------------------------------


def test_when_request_param_out_of_range_of_ranks_then_response_status_code_should_be_422_unprocessable_entity():
    response = client.get("/songs/rank/555")
    assert response.status_code == 422


def test_when_request_param_within_range_of_ranks_then_response_status_code_should_be_200_ok():
    response = client.get("/songs/rank/42")
    assert response.status_code == 200


def test_when_request_param_within_range_of_ranks_then_response_body_should_contain_the_song_with_such_rank():
    response = client.get("/songs/rank/42")
    song = response.json()
    assert song["rank"] == 42
