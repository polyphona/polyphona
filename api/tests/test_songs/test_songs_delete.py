import pytest

from api.db import Database, DoesNotExist


@pytest.fixture
def song_id(db: Database, song1) -> int:
    return db.create_song(**song1)


def test_if_token_missing_then_bad_request(client, song_id):
    result = client.simulate_delete(f"/songs/{song_id}")
    assert result.status_code == 401


def test_if_song_does_not_exist_then_not_found(
    client, auth_headers: dict, song_id: int
):
    result = client.simulate_delete(
        f"/songs/{song_id + 10}", headers=auth_headers
    )
    assert result.status_code == 404


def test_delete_song(client, db: Database, auth_headers: dict, song_id: int):
    db.create_song_user_link(song_id=song_id, username="admin")
    result = client.simulate_delete(f"/songs/{song_id}", headers=auth_headers)
    assert result.status_code == 204

    with pytest.raises(DoesNotExist):
        db.get_song_by_id(id=song_id)
