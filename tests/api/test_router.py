from unittest.mock import MagicMock

from fastapi.testclient import TestClient

from app.api.dependencies import get_ai_service
from app.main import app
from app.services.ai_service import AIService


def _client_with_fake_service(fake_service):
    app.dependency_overrides[get_ai_service] = lambda: fake_service
    client = TestClient(app)
    return client


def teardown_function():
    app.dependency_overrides.clear()


def test_health():

    client = _client_with_fake_service(MagicMock(spec=AIService))

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_chat_success():

    fake_service = MagicMock(spec=AIService)
    fake_service.chat.return_value = {
        "answer": "Employees get 20 days of annual leave.",
        "sources": [
            {"document": "policy.pdf", "page": 1, "section": "Leave"}
        ],
        "confidence": 0.91,
    }

    client = _client_with_fake_service(fake_service)

    response = client.post(
        "/chat",
        json={"question": "what is the leave policy?"},
    )

    assert response.status_code == 200

    body = response.json()

    assert body["answer"] == "Employees get 20 days of annual leave."
    assert body["confidence"] == 0.91
    assert body["sources"][0]["document"] == "policy.pdf"

    fake_service.chat.assert_called_once_with("what is the leave policy?")


def test_chat_rejects_empty_question():

    client = _client_with_fake_service(MagicMock(spec=AIService))

    response = client.post("/chat", json={"question": ""})

    assert response.status_code == 422


def test_chat_maps_value_error_to_400():

    fake_service = MagicMock(spec=AIService)
    fake_service.chat.side_effect = ValueError("No arithmetic expression found")

    client = _client_with_fake_service(fake_service)

    response = client.post("/chat", json={"question": "1+"})

    assert response.status_code == 400
    assert "No arithmetic expression found" in response.json()["detail"]


def test_chat_maps_unexpected_error_to_500():

    fake_service = MagicMock(spec=AIService)
    fake_service.chat.side_effect = RuntimeError("boom")

    client = _client_with_fake_service(fake_service)

    response = client.post("/chat", json={"question": "hello"})

    assert response.status_code == 500
