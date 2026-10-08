import pytest
from app import app, calculate_bmi, members


@pytest.fixture
def client():
    app.config["TESTING"] = True
    members.clear()
    with app.test_client() as c:
        yield c


def test_home(client):
    assert client.get("/").status_code == 200


def test_health(client):
    assert client.get("/health").get_json()["status"] == "ok"


def test_programs(client):
    assert "fat_loss" in client.get("/programs").get_json()


def test_add_member(client):
    r = client.post("/members", json={"name": "Ravi", "program": "beginner"})
    assert r.status_code == 201 and r.get_json()["id"] == 1


def test_list_members(client):
    client.post("/members", json={"name": "Ravi", "program": "beginner"})
    assert len(client.get("/members").get_json()) == 1


def test_add_member_invalid(client):
    assert client.post("/members", json={"name": "X"}).status_code == 400


def test_bmi_calc():
    assert calculate_bmi(70, 1.75) == 22.86


def test_bmi_invalid():
    with pytest.raises(ValueError):
        calculate_bmi(0, 1.7)


def test_bmi_endpoint_ok(client):
    r = client.post("/bmi", json={"weight": 70, "height": 1.75})
    assert r.get_json()["bmi"] == 22.86


def test_bmi_endpoint_bad_input(client):
    assert client.post("/bmi", json={"weight": 70}).status_code == 400
