def test_get_users(basic_api):
    '''Test that the GET /users API returns a list of
    users and that the page length matches the users
    returned in `data`
    '''
    r = basic_api.get("users")
    assert r.ok
    assert r.json()['per_page'] == len(r.json()['data'])


def test_create_user(basic_api):
    '''Test that the POST /users works and returns a 201
    '''
    payload = {
        "first_name": "Keith",
        "last_name": "Knapp"
    }
    r = basic_api.post("users", json=payload)
    assert r.ok
    new_id = r.json()['id']
    assert new_id != 0
    g = basic_api.get("users/{}".format(new_id))
    print(basic_api.history)
    assert g.status_code == 201
    assert g.json()['first_name'] == payload['first_name']
