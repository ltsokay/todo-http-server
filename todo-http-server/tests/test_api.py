import requests

BASE = "http://127.0.0.1:5000"


def test_create():
    r = requests.post(f"{BASE}/tasks", json={"title": "Test", "priority": "low"})
    assert r.status_code == 201


def test_list():
    r = requests.get(f"{BASE}/tasks")
    assert isinstance(r.json(), list)


def test_complete():
    r = requests.post(f"{BASE}/tasks/1/complete")
    assert r.status_code in (200, 404)