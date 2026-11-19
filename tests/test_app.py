import pytest

from app import app, reset_tickets


@pytest.fixture
def client():
    reset_tickets()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_list_tickets_returns_200(client):
    response = client.get("/api/tickets")
    assert response.status_code == 200
    assert len(response.get_json()) == 5


def test_list_tickets_sorts_by_priority(client):
    response = client.get("/api/tickets")

    priorities = [ticket["priority"] for ticket in response.get_json()]
    assert priorities == ["High", "High", "Medium", "Medium", "Low"]


def test_get_ticket_1_has_a_title(client):
    response = client.get("/api/tickets/1")
    assert response.status_code == 200
    assert response.get_json()["title"] == "Laptop not charging"


def test_unknown_ticket_returns_404(client):
    response = client.get("/api/tickets/9999")
    assert response.status_code == 404


def test_create_ticket_rejects_missing_title(client):
    response = client.post("/api/tickets", json={"category": "Hardware"})
    assert response.status_code == 400


def test_create_ticket_rejects_empty_title(client):
    response = client.post("/api/tickets", json={"title": ""})
    assert response.status_code == 400


def test_create_ticket_rejects_unknown_category(client):
    response = client.post(
        "/api/tickets",
        json={"title": "Broken laptop", "category": "Furniture"},
    )
    assert response.status_code == 400


def test_create_ticket_rejects_unknown_priority(client):
    response = client.post(
        "/api/tickets",
        json={"title": "Broken laptop", "priority": "Urgent"},
    )
    assert response.status_code == 400


def test_change_status_rejects_unknown_status(client):
    response = client.patch(
        "/api/tickets/1/status",
        json={"status": "Pending"},
    )
    assert response.status_code == 400



# Add your own tests below: one failing test for each bug you find,
# plus at least 5 negative tests.
