"""Unit tests for text processing and length measurement utilities."""

import pytest
from trusteval.utils.text import calculate_response_length, format_prompt


def test_calculate_response_length_character():
    text = "Hello world! 123"
    assert calculate_response_length(text, method="character") == len(text)
    assert calculate_response_length("", method="character") == 0
    assert calculate_response_length(None, method="character") == 0


def test_calculate_response_length_char_nowhitespace():
    text = "Hello  world \n \t"
    # "Helloworld" -> length 10
    assert calculate_response_length(text, method="char_nowhitespace") == 10


def test_calculate_response_length_word():
    text = "The quick brown fox jumps over the lazy dog."
    assert calculate_response_length(text, method="word") == 9
    assert calculate_response_length("One", method="word") == 1
    assert calculate_response_length("   ", method="word") == 0


def test_calculate_response_length_invalid_method():
    with pytest.raises(ValueError, match="Unsupported length calculation method"):
        calculate_response_length("Sample text", method="tokens")


def test_format_prompt():
    template = "Context:\n{context}\n\nResponse:\n{response}"
    system = "You are a judge."
    context = "User: Hi\nBot: Hello"
    response = "How can I help?"

    messages = format_prompt(
        template=template,
        system_message=system,
        context=context,
        response=response,
    )

    assert len(messages) == 2
    assert messages[0]["role"] == "system"
    assert messages[0]["content"] == "You are a judge."
    assert messages[1]["role"] == "user"
    assert "Context:\nUser: Hi\nBot: Hello" in messages[1]["content"]
    assert "Response:\nHow can I help?" in messages[1]["content"]

