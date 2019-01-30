import json


def test_get_users(basic_api):
    r = basic_api.get("users")
    print(json.dumps(r.json(), indent=4))
    assert False