from rest_framework.test import APIClient


def test_root_not_found(client: APIClient) -> None:
    response = client.get('/')

    assert response.status_code == 404