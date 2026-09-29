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

    class FakeCompletions:

        def create(self, **kwargs):
            return FakeResponse()

    class FakeChat:

        completions = FakeCompletions()

    class FakeClient:

        chat = FakeChat()

    monkeypatch.setattr(
        evaluator,
        "get_client",
        lambda: FakeClient()
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
    assert result["reason"] == "Strong response."


def test_extract_json():

    text = """
    ```json
    {
        "relevance": 8,
        "accuracy": 9
    }
    """

    # Test the same JSON extraction logic directly
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