import pytest
import os
from fastapi.testclient import TestClient
from src import create_app
from dotenv import load_dotenv

load_dotenv()

test_url = os.getenv("TEST_URL")
app = create_app()

API_USERNAME = os.getenv("API_USERNAME") or ""
API_PASSWORD = os.getenv("API_PASSWORD") or ""


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c


def test_crawl_with_javascript(client):
    response = client.post("/crawl", json={"url": test_url, "render_js": True}, auth=(API_USERNAME, API_PASSWORD))
    json = response.json()
    assert response.status_code == 200
    assert json['content'] is not None

def test_crawl_without_javascript(client):
    response = client.post("/crawl", json={"url": test_url, "render_js": False}, auth=(API_USERNAME, API_PASSWORD))
    json = response.json()
    assert response.status_code == 200
    assert json['content'] is not None

def test_crawl_returns_valid_structure(client):
    response = client.post("/crawl", json={"url": test_url, "render_js": False}, auth=(API_USERNAME, API_PASSWORD))
    json = response.json()
    assert 'url' in json
    assert 'content' in json
    assert 'status_code' in json
