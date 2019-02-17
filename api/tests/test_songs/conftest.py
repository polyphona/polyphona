import pytest


@pytest.fixture
def song1():
    return {
        "name": "Song 01",
        "tracks": [
            {
                "id": 1,
                "name": "Cello",
                "isMuted": False,
                "notes": [
                    {
                        "midi": 10,
                        "time": 10,
                        "note": "A2",
                        "velocity": 64,
                        "duration": 16,
                        "instrumentNumber": 8,
                    }
                ],
                "startTime": 0,
                "duration": 10,
                "instrument": "Cello",
            }
        ],
    }


@pytest.fixture
def song2():
    return {
        "name": "Song 02",
        "tracks": [
            {
                "id": 1,
                "name": "Drums",
                "isMuted": False,
                "notes": [
                    {
                        "midi": 10,
                        "time": 10,
                        "note": "A2",
                        "velocity": 64,
                        "duration": 16,
                        "instrumentNumber": 8,
                    }
                ],
                "startTime": 0,
                "duration": 10,
                "instrument": "Drums",
            }
        ],
    }
