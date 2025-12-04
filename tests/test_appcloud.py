import sys
from pathlib import Path

import pytest

# Ensure the application module can be imported when running tests from the repository root.
sys.path.append(str(Path(__file__).resolve().parent.parent))
from appcloud import app  # noqa: E402


@pytest.fixture()
def client():
    app.config.update(TESTING=True, PROPAGATE_EXCEPTIONS=False)
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
    assert response.status_code >= 400


def test_sum_type_error_returns_error(client):
    response = client.post("/sum", json={"a": "1", "b": 2})
    assert response.status_code >= 400


def test_multiply_with_integers(client):
    response = client.post("/multiply", json={"a": 2, "b": 3})
    assert response.status_code == 200
    assert response.get_json() == {"code": 0, "data": 6}


def test_multiply_with_floats(client):
    response = client.post("/multiply", json={"a": 1.5, "b": 2.0})
    assert response.status_code == 200
    assert response.get_json() == {"code": 0, "data": 3.0}


def test_multiply_missing_parameter_returns_error(client):
    response = client.post("/multiply", json={"a": 2})
    assert response.status_code >= 400


def test_multiply_type_error_returns_error(client):
    response = client.post("/multiply", json={"a": "x", "b": "y"})
    assert response.status_code >= 400
