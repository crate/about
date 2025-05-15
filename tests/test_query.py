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


def test_settings_context_url_default():
    assert Settings.llms_txt_url == "https://cdn.crate.io/about/v1/llms-full.txt"


def test_settings_context_url_env(mocker):
    mocker.patch.dict("os.environ", {"ABOUT_CONTEXT_URL": "http://example.com"})
    assert Settings.llms_txt_url == "http://example.com"


def test_llms_txt_payload_from_file(tmp_path, monkeypatch):
    # Create a temporary file with known content.
    test_file = tmp_path / "test_context.txt"
    test_content = "Test CrateDB context content"
    test_file.write_text(test_content)

    # Point `ABOUT_CONTEXT_URL` to the temporary file.
    monkeypatch.setenv("ABOUT_CONTEXT_URL", str(test_file))

    # Verify the classproperty correctly reads the file.
    assert Settings.llms_txt_payload == test_content


def test_llms_txt_payload_from_http(monkeypatch, requests_mock):
    # Mock HTTP URL and response.
    test_url = "http://example.com/context.txt"
    test_content = "Test CrateDB HTTP content"
    requests_mock.get(test_url, text=test_content)

    # Set the environment variable to the HTTP URL.
    # Point `ABOUT_CONTEXT_URL` to the temporary URL.
    monkeypatch.setenv("ABOUT_CONTEXT_URL", test_url)

    # Verify HTTP request is made and content is returned.
    assert Settings.llms_txt_payload == test_content


def test_llms_txt_payload_invalid_source(monkeypatch):
    # Set the environment variable to an invalid path.
    monkeypatch.setenv("ABOUT_CONTEXT_URL", "/non/existent/path/that/is/not/http")

    # Verify appropriate error is raised.
    with pytest.raises(NotImplementedError) as ex:
        _ = Settings.llms_txt_payload
    assert ex.match("Unable to load context file. Source:")


def test_get_prompt_exception_handling(monkeypatch, mocker):
    # Mock llms_txt_payload to raise an exception.
    mocker.patch.object(Settings, "llms_txt_payload", lambda x: Exception("Test error"))

    # Call get_prompt and verify fallback behavior
    Settings.llms_txt = None
    result = Settings.get_prompt()

    # Verify fallback context is used
    assert Settings.default_context in result
    assert "minimal context" in result
