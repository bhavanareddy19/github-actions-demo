"""Tests for the Flask web layer using Flask's test client."""
import pytest

from app.main import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_home(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert resp.get_json()["service"] == "calculator-api"


def test_health(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.get_json()["status"] == "healthy"


def test_calc_add(client):
    resp = client.get("/calc?op=add&a=2&b=3")
    assert resp.status_code == 200
    assert resp.get_json()["result"] == 5


def test_calc_divide_by_zero(client):
    resp = client.get("/calc?op=divide&a=1&b=0")
    assert resp.status_code == 400


def test_calc_bad_numbers(client):
    resp = client.get("/calc?op=add&a=foo&b=3")
    assert resp.status_code == 400
