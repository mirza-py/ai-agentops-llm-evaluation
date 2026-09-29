import pytest

from app.prompt_manager import load_prompt


def test_load_v1():

    prompt = load_prompt("v1")

    assert isinstance(prompt, str)
    assert len(prompt) > 0


def test_load_v2():

    prompt = load_prompt("v2")

    assert isinstance(prompt, str)
    assert len(prompt) > 0


def test_invalid_prompt_version():

    with pytest.raises(FileNotFoundError):

        load_prompt("invalid_version")