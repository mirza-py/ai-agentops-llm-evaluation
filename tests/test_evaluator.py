import app.evaluator as evaluator


def test_empty_response():

    result = evaluator.evaluate_response(
        "What is Python?",
        ""
    )

    assert result["failure"] is True
    assert result["quality_score"] == 0


def test_llm_judge(monkeypatch):

    class FakeMessage:
        content = """
        {
            "relevance": 9,
            "accuracy": 8,
            "completeness": 9,
            "clarity": 10,
            "overall_score": 9,
            "failure": false,
            "feedback": "Strong response."
        }
        """

    class FakeChoice:
        message = FakeMessage()

    class FakeResponse:
        choices = [FakeChoice()]

    def fake_create(**kwargs):
        return FakeResponse()

    monkeypatch.setattr(
        evaluator.client.chat.completions,
        "create",
        fake_create
    )

    result = evaluator.llm_judge(
        "What is Python?",
        "Python is a programming language."
    )

    assert result["relevance"] == 9.0
    assert result["accuracy"] == 8.0
    assert result["completeness"] == 9.0
    assert result["clarity"] == 10.0
    assert result["quality_score"] == 9.0
    assert result["failure"] is False


def test_extract_json():

    text = """
    ```json
    {
        "relevance": 8,
        "accuracy": 9
    }
    ```
    """

    result = evaluator.extract_json(text)

    assert result["relevance"] == 8
    assert result["accuracy"] == 9