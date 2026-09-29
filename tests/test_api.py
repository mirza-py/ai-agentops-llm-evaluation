from fastapi.testclient import TestClient

import app.main as main


client = TestClient(main.app)


def test_home():
    response = client.get("/")

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == "AI AgentOps Platform is running"
    assert data["version"] == "2.0.0"


def test_health():
    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "healthy"


def test_chat(monkeypatch):
    """
    Test /chat without calling the real Groq API.
    """

    def fake_generate_response(prompt):
        return (
            "Python is a high-level programming language "
            "used for web development, data science, "
            "automation and machine learning."
        )

    def fake_evaluate_response(prompt, response):
        return {
            "relevance": 9.0,
            "accuracy": 9.0,
            "completeness": 8.0,
            "clarity": 9.0,
            "quality_score": 8.75,
            "failure": False,
            "reason": "Good response."
        }

    monkeypatch.setattr(
        main,
        "generate_response",
        fake_generate_response
    )

    monkeypatch.setattr(
        main,
        "evaluate_response",
        fake_evaluate_response
    )

    response = client.post(
        "/chat",
        json={
            "prompt": "What is Python?",
            "prompt_version": "v1"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["prompt"] == "What is Python?"
    assert data["prompt_version"] == "v1"
    assert data["model"] == "qwen/qwen3.8-27b"

    assert "response" in data
    assert "evaluation" in data

    assert data["evaluation"]["quality_score"] == 8.75
    assert data["evaluation"]["failure"] is False

    assert data["database_status"] == "saved"


def test_chat_invalid_prompt_version(monkeypatch):

    def fake_generate_response(prompt):
        return "Test response"

    monkeypatch.setattr(
        main,
        "generate_response",
        fake_generate_response
    )

    response = client.post(
        "/chat",
        json={
            "prompt": "Hello",
            "prompt_version": "invalid_version"
        }
    )

    assert response.status_code == 500


def test_chat_missing_prompt():

    response = client.post(
        "/chat",
        json={
            "prompt_version": "v1"
        }
    )

    assert response.status_code == 422