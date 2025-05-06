import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.api.routes import router
from unittest.mock import patch, AsyncMock

app = FastAPI()
app.include_router(router)

def test_status_route():
    with patch("shared.helper.is_process_active", return_value=True):
        client = TestClient(app)
        response = client.get("/status")
        assert response.status_code == 200
        assert response.json() == {"running": True}

def test_current_house_route():
    with patch("app.api.routes.redis_client.get", new_callable=AsyncMock) as mock_get:
        mock_get.return_value = "1"
        with patch("shared.helper.get_redis_house_key", return_value="house_status"):
            client = TestClient(app)
            response = client.get("/current_house")
        assert response.status_code == 200
        assert response.json() == {"house": 1}
