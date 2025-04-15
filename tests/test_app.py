# tests/test_app.py
import pytest
import re
from main import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_index(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Welcome to the Conversational AI Service!" in response.data


def test_chat_missing_question(client):
    client.set_cookie("session_id", "sesssion_id")
    response = client.post("/chat", json={})
    assert response.status_code == 400
    json_data = response.get_json()
    assert "error" in json_data


def test_chat_plain_response(client, monkeypatch):
    client.set_cookie("session_id", "sesssion_id")
    sample_question = "What is the capital of South Africa?"
    sample_answer = ["The capital of France is Paris."]

    def fake_get_answer(user_message, session_id) -> list:
        return sample_answer

    monkeypatch.setattr("app.chat_routes.get_response", fake_get_answer)
    response = client.post("/chat", json={"message": sample_question})
    assert response.status_code == 200
    json_data = response.get_json()
    print(json_data)
    assert json_data["response"] == sample_answer[0]


def test_chat_with_history(client, monkeypatch):
    client.set_cookie("session_id", "sesssion_id")
    sample_question = ["My name is Bob.", "What is my name?"]
    response1 = client.post("/chat", json={"message": sample_question[0]})
    assert response1.status_code == 200
    json_data = response1.get_json()
    assert re.search(".*Bob.*", json_data["response"]) is not None

    # Ask from history of chat
    response2 = client.post("/chat", json={"message": sample_question[1]})
    assert response2.status_code == 200
    json_data = response2.get_json()
    assert re.search(".*Bob.*", json_data["response"]) is not None
