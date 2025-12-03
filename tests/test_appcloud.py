import os
import sys
import pytest

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from appcloud import app


@pytest.fixture()
def client():
    with app.test_client() as client:
        yield client


def test_sum_with_integers(client):
    response = client.post("/sum", json={"a": 1, "b": 2})
    assert response.status_code == 200
    assert response.get_json() == {"code": 0, "data": 3}


def test_sum_with_floats(client):
    response = client.post("/sum", json={"a": 1.5, "b": 2.5})
    assert response.status_code == 200
    assert response.get_json() == {"code": 0, "data": 4.0}


def test_sum_missing_parameter_returns_error(client):
    response = client.post("/sum", json={"a": 1})
    assert response.status_code == 500


def test_sum_type_error_returns_error(client):
    response = client.post("/sum", json={"a": "1", "b": 2})
    assert response.status_code == 500


def test_multiply_with_integers(client):
    response = client.post("/multiply", json={"a": 3, "b": 4})
    assert response.status_code == 200
    assert response.get_json() == {"code": 0, "data": 12}


def test_multiply_with_floats(client):
    response = client.post("/multiply", json={"a": 1.5, "b": 2.0})
    assert response.status_code == 200
    assert response.get_json() == {"code": 0, "data": 3.0}


def test_multiply_missing_parameter_returns_error(client):
    response = client.post("/multiply", json={"a": 3})
    assert response.status_code == 500


def test_multiply_type_error_returns_error(client):
    response = client.post("/multiply", json={"a": 3, "b": {"x": 1}})
    assert response.status_code == 500
