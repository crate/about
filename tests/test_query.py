import sys

import openai
import pytest

from cratedb_about import CrateDbKnowledgeConversation
from cratedb_about.query.model import Example, Settings


def test_model_settings():
    """
    Validate a few basic attributes of the Settings bundle class.
    """
    assert Settings.llms_txt_url == "https://cdn.crate.io/about/v1/llms-full.txt"
    assert "helpful" in Settings.instructions


def test_model_prompt():
    """
    Validate the prompt contex payload.
    """
    assert "The default TCP ports of CrateDB are" in Settings.get_prompt()


def test_example_question():
    """
    Validate the example question bundle class.
    """
    assert "How to enumerate active jobs?" in Example.questions


def test_ask_openai_no_api_key():
    """
    Validate inquiry with OpenAI, failing without an API key.
    """
    with pytest.raises(ValueError) as ex:
        CrateDbKnowledgeConversation()
    assert ex.match("OPENAI_API_KEY environment variable is required when using 'openai' backend")


def test_ask_openai_invalid_api_key(mocker):
    """
    Validate inquiry with OpenAI, failing when using an invalid API key.
    """
    mocker.patch.dict("os.environ", {"OPENAI_API_KEY": "foo"})
    knowledge = CrateDbKnowledgeConversation()
    with pytest.raises(openai.AuthenticationError) as ex:
        knowledge.ask("CrateDB does not seem to provide an AUTOINCREMENT feature?")
    assert ex.match("Incorrect API key provided: foo")


@pytest.mark.skipif(sys.version_info < (3, 10), reason="requires Python 3.10 or higher")
def test_ask_claude_no_api_key():
    """
    Validate inquiry with Anthropic Claude, failing without an API key.
    """
    with pytest.raises(ValueError) as ex:
        CrateDbKnowledgeConversation(backend="claude")
    assert ex.match(
        "ANTHROPIC_API_KEY environment variable is required when using 'claude' backend"
    )


@pytest.mark.skipif(sys.version_info < (3, 10), reason="requires Python 3.10 or higher")
def test_ask_claude_invalid_api_key(mocker):
    """
    Validate inquiry with Anthropic Claude, failing when using an invalid API key.
    """
    mocker.patch.dict("os.environ", {"ANTHROPIC_API_KEY": "foo"})
    knowledge = CrateDbKnowledgeConversation(backend="claude")
    with pytest.raises(RuntimeError) as ex:
        knowledge.ask("CrateDB does not seem to provide an AUTOINCREMENT feature?")
    assert ex.match("Claude API error:.*authentication_error.*invalid x-api-key")
