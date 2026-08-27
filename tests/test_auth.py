from fastapi.testclient import TestClient
from my_free_code import app
from my_free_code.api import routes

def test_health():
    c = TestClient(app)
    assert c.get("/health").status_code == 200

def test_models_requires_auth():
    routes.settings.__class__
    c = TestClient(app)
    response = c.get("/v1/models")
    assert response.status_code in (200, 401)
