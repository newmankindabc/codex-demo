from pathlib import Path
import sys

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from appcloud import app


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


@pytest.mark.parametrize(
    "endpoint,payload,expected",
    [
        ("/sum", {"a": 2, "b": 3}, {"code": 0, "data": 5}),
        ("/multiply", {"a": 4, "b": 6}, {"code": 0, "data": 24}),
    ],
)
def test_arithmetic_endpoints(client, endpoint, payload, expected):
    response = client.post(endpoint, json=payload)

    assert response.status_code == 200
    assert response.get_json() == expected
