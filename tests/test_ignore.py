from time import time
from snapshottest.ignore import clear_ignore_keys

DATA = {
    "name": {
        "id": time(),
        "first": "Manual",
        "last": "gonazales",
        "cities": ["1", "2", {"id": time()}],
    }
}

DATA_EXPECTED = {
    "name": {
        "id": None,
        "first": "Manual",
        "last": "gonazales",
        "cities": [None, "2", {"id": None}],
    }
}


def test_clear_works():
    clean_data = clear_ignore_keys(
        DATA, ignore_keys=["name.id", "name.cities[0]", "name.cities[2].id"]
    )
    assert clean_data == DATA_EXPECTED
