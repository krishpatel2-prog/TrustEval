"""Text processing, length measurement, and prompt formatting utilities."""

import re
from typing import Dict, List


def calculate_response_length(text: str, method: str = "character") -> int:
    """Calculate the length of a response text independently of model tokenizers.

    Parameters
    ----------
    text : str
        The input response string.
    method : str, default="character"
        Method of measurement: 'character' (raw length), 'word' (whitespace/punctuation tokens),
        or 'char_nowhitespace'.

    Returns
    -------
    int
        Calculated length.

    Raises
    ------
    ValueError
        If an unsupported method is specified.
    """
    if text is None:
        return 0

    if not isinstance(text, str):
        text = str(text)

    if method == "character":
        return len(text)
    elif method == "char_nowhitespace":
        return len(re.sub(r"\s+", "", text))
    elif method == "word":
        words = re.findall(r"\b\w+\b", text)
        return len(words)
    else:
        raise ValueError(f"Unsupported length calculation method: '{method}'. Choose 'character', 'word', or 'char_nowhitespace'.")


def format_prompt(template: str, system_message: str, context: str, response: str) -> List[Dict[str, str]]:
    """Construct standard chat messages from context, response, and template.

    Parameters
    ----------
    template : str
        Prompt string containing `{context}` and `{response}` placeholders.
    system_message : str
        System instructions string.
    context : str
        Multi-turn conversational context.
    response : str
        Chatbot's final response turn.

    Returns
    -------
    List[Dict[str, str]]
        List of message dictionaries with 'role' and 'content' keys.
    """
    user_content = template.format(context=context.strip(), response=response.strip())
    messages = [
        {"role": "system", "content": system_message.strip()},
        {"role": "user", "content": user_content},
    ]
    return messages

