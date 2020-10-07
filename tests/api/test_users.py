import pytest
from src.ReusableTests.BaseTest import RequestTestGet, RequestTestPost


@pytest.fixture(scope='module')
def get_response(basic_api):
    return basic_api.get(url_path="users")


@pytest.fixture(scope='module')
def get_bad_response(basic_api):
    return basic_api.get(url_path="users/-1")


def test_response_code(get_response):
    assert get_response.status_code == 200


def test_status(get_response):
    assert get_response.json()['page'] == 1
    assert get_response.json()['total'] == 12
    # assert get_response.json()['status'] == 'healthy'
    # assert get_response.json()['component1Status'] == 'healthy'


def test_properties_defined(get_response):
    properties_are_defined(get_response.json())


def test_execution_time(get_response):
    assert get_response.json()['total_pages'] * get_response.json()['per_page'] >= get_response.json()['total']
    # assert get_response.json()['component1ResponseTime'] > 0


def test_bad_response_code(get_bad_response):
    assert get_bad_response.status_code == 404, str(get_bad_response)


def test_bad_status(get_bad_response):
    print(get_bad_response.json())
    assert get_bad_response.json()['page'] == 1
    assert get_bad_response.json()['total'] == 12
    # assert get_bad_response.json()['status'] == 'healthy'
    # assert get_bad_response.json()['component1Status'] == 'healthy'


def test_bad_properties_defined(get_bad_response):
    properties_are_defined(get_bad_response.json())


def test_bad_execution_time(get_bad_response):
    assert get_bad_response.json()['total_pages'] * get_bad_response.json()['per_page'] >= get_bad_response.json()['total']
    # assert get_bad_response.json()['component1ResponseTime'] > 0


def test_bad_errors_is_array(get_bad_response):
    assert isinstance(get_bad_response.json()['data'], list)
    assert len(get_bad_response.json()['data']) == get_bad_response.json()['per_page']
    # assert isinstance(get_bad_response.json()['errors'], list)
    # assert len(get_bad_response.json()['errors']) == 0


def test_bad_errors_is_array(get_bad_response):
    assert isinstance(get_bad_response.json()['data'], list)
    assert len(get_bad_response.json()['data']) == get_bad_response.json()['per_page']
    # assert isinstance(get_bad_response.json()['errors'], list)
    # assert len(get_bad_response.json()['errors']) == 0


def properties_are_defined(response):
    # properties = ['dbStatus', 'version', 'region', 'environmentName', 'logLevel']
    properties = ['page', 'per_page', 'total', 'total_pages', 'data']
    for property_name in properties:
        assert property_name in response.keys()


# def test_get_users(basic_api):
#     '''Test that the GET /users API returns a list of
#     users and that the page length matches the users
#     returned in `data`
#     '''
#     a = RequestTestGet(
#         session=basic_api,
#         resource="users",
#         model={"id": "int", "first_name": "str", "last_name": "str", "avatar": "str"},
#         mapping="data")
#     assert a, a.result_str


# def test_create_user(basic_api):
#     '''Test that the POST /users works and returns a 201
#     '''
#     payload = {
#         "first_name": "Keith",
#         "last_name": "Knapp"
#     }
#     a = RequestTestPost(
#         session=basic_api,
#         resource="users",
#         payload=payload,
#         model={"id": "int", "first_name": "str", "last_name": "str", "createdAt": "str"})
#     assert a, a.result_str + str(basic_api.history[-1].json())

#     print(basic_api.history[-1].cURL)
#     print(basic_api.history[-1])
#     assert False


