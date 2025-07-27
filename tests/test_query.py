import sys

import hishel
import httpx
import openai
import pytest

from cratedb_about import CrateDbKnowledgeConversation
from cratedb_about.query.model import CrateDbKnowledgeContextLoader, Example


@pytest.fixture
def loader() -> CrateDbKnowledgeContextLoader:
    """
    Provide context loader instance for all test cases.
    """
    return CrateDbKnowledgeContextLoader()


def test_model_loader_default(loader):
    """
    Validate a few basic attributes of the context loader class.
    """
    assert loader.url == "https://cdn.crate.io/about/v1/llms-full.txt"
    assert "helpful" in loader.instructions


def test_model_loader_url_env_success(loader, mocker):
    mocker.patch.dict("os.environ", {"ABOUT_CONTEXT_URL": "http://example.com"})
    assert loader.url == "http://example.com"


def test_model_loader_url_env_empty(loader, mocker):
    mocker.patch.dict("os.environ", {"ABOUT_CONTEXT_URL": ""})
    with pytest.raises(ValueError) as excinfo:
        _ = loader.url
    assert excinfo.match(
        "Unable to operate without context URL. "
        "Please check `ABOUT_CONTEXT_URL` environment variable."
    )


def test_model_prompt(loader):
    """
    Validate the prompt context payload.
    """
    assert "The default TCP ports of CrateDB are" in loader.get_prompt()


def test_example_question():
    """
    Validate the example question bundle class.
    """
    assert "How to enumerate active jobs?" in Example.knowledgebase


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


def test_model_payload_from_file(loader, tmp_path, monkeypatch):
    # Create a temporary file with known content.
    test_file = tmp_path / "test_context.txt"
    test_content = "Test local file content"
    test_file.write_text(test_content)

    # Point `ABOUT_CONTEXT_URL` to the temporary file.
    monkeypatch.setenv("ABOUT_CONTEXT_URL", str(test_file))

    # Verify the outcome.
    result = loader.get_prompt()
    assert test_content in result
    assert "necessary context" in result


# TODO: Fix HTTP mocking with Hishel. Current implementation fails during test execution.
@pytest.mark.skip(reason="Test incompatible with Hishel caching implementation")
def test_model_payload_from_http(monkeypatch):
    # Mock HTTP URL and response.
    test_url = "http://example.com/context.txt"
    test_content = "Test HTTP content"

    # Point the environment variable `ABOUT_CONTEXT_URL` to the HTTP URL.
    monkeypatch.setenv("ABOUT_CONTEXT_URL", test_url)

    # Verify the outcome.
    with hishel.MockTransport() as transport:
        transport.add_responses([httpx.Response(status_code=200, text=test_content)])
        loader = CrateDbKnowledgeContextLoader()
        result = loader.get_prompt()

        assert loader.url == test_url
        assert test_content in result
        assert "necessary context" in result


def test_model_payload_invalid_source(loader, monkeypatch, caplog):
    # Set the environment variable to an invalid path.
    context_url = "/non/existent/path/that/is/not/http"
    monkeypatch.setenv("ABOUT_CONTEXT_URL", context_url)

    # Acquire prompt.
    result = loader.get_prompt()

    # Verify log output.
    assert f"Fetching context failed. Source: {context_url}" in caplog.messages

    # Verify fallback context is used.
    assert loader.fallback_context in result
    assert "minimal context" in result


def test_model_get_prompt_exception_handling(loader, monkeypatch, mocker):
    # Mock loader method to raise an exception.
    def _raise(*_args, **_kwargs):
        raise Exception("Test error")

    mocker.patch.object(loader, "fetch", _raise)

    # Acquire prompt.
    result = loader.get_prompt()

    # Verify fallback context is used.
    assert loader.fallback_context in result
    assert "minimal context" in result


def test_loader_valid_ttl(mocker):
    # Set a valid cache TTL value.
    ttl_value = "7200"  # 2 hours in seconds
    mocker.patch.dict("os.environ", {"ABOUT_CACHE_TTL": ttl_value})

    # Instantiate loader and verify TTL.
    loader = CrateDbKnowledgeContextLoader()
    assert loader.cache_ttl == 7200


def test_loader_invalid_ttl_string(mocker):
    # Use an invalid cache TTL value.
    mocker.patch.dict("os.environ", {"ABOUT_CACHE_TTL": "foo"})

    # Validate.
    with pytest.raises(ValueError) as ex:
        CrateDbKnowledgeContextLoader()
    assert ex.match("Environment variable `ABOUT_CACHE_TTL` invalid: invalid literal for int")


def test_loader_invalid_ttl_negative(mocker):
    # Use an invalid cache TTL value.
    mocker.patch.dict("os.environ", {"ABOUT_CACHE_TTL": "-42"})

    # Validate.
    with pytest.raises(ValueError) as ex:
        CrateDbKnowledgeContextLoader()
    assert ex.match("Environment variable `ABOUT_CACHE_TTL` invalid: Cache TTL must be positive")
