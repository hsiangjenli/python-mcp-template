import pytest
from fastapi.testclient import TestClient
from mcp_tools.main import app


@pytest.fixture(scope="module")
def client():
    return TestClient(app)


def test_new_endpoint_success(client):
    resp = client.post("/new/endpoint/", json={"name": "developer"})
    assert resp.status_code == 200
    assert resp.json() == {"message": "Hello, developer!"}


def test_new_endpoint_validation_error(client):
    # Missing required field 'name'
    resp = client.post("/new/endpoint/", json={})
    assert resp.status_code == 422
    body = resp.json()
    assert "detail" in body
    # Ensure the validation error refers to the 'name' field
    assert any(
        isinstance(err, dict) and "loc" in err and "name" in err.get("loc", [])
        for err in body.get("detail", [])
    )
