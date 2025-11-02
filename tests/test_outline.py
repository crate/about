import pytest
import requests
from click.testing import CliRunner

from cratedb_about import CrateDbKnowledgeOutline
from cratedb_about.cli import cli
from cratedb_about.outline import OutlineDocument

CRATEDB_OUTLINE_FILE = "src/cratedb_about/outline/cratedb-outline.yaml"
CRATEDB_OUTLINE_URL = "https://github.com/crate/about/raw/refs/tags/v0.0.3/src/cratedb_about/outline/cratedb-outline.yaml"

TESTING_OUTLINE_FILE = "tests/assets/outline.yaml"


@pytest.fixture
def cratedb_outline_builtin() -> OutlineDocument:
    return CrateDbKnowledgeOutline.load()


def test_outline_cli_markdown():
    runner = CliRunner()

    result = runner.invoke(
        cli,
        args=["outline", "--format", "markdown"],
        catch_exceptions=False,
    )
    assert result.exit_code == 0, result.output

    assert "# CrateDB" in result.output
    assert "Things to remember when working with CrateDB" in result.output
    assert "Concept: Clustering" in result.output


def test_outline_cli_json():
    runner = CliRunner()

    result = runner.invoke(
        cli,
        args=["outline", "--format", "json"],
        catch_exceptions=False,
    )
    assert result.exit_code == 0, result.output

    assert "Things to remember when working with CrateDB" in result.output
    assert "Concept: Clustering" in result.output


def test_outline_cli_yaml():
    runner = CliRunner()

    result = runner.invoke(
        cli,
        args=["outline", "--format", "yaml"],
        catch_exceptions=False,
    )
    assert result.exit_code == 0, result.output

    assert "Things to remember when working with CrateDB" in result.output
    assert "Concept: Clustering" in result.output


def test_outline_cli_llms_txt_default():
    runner = CliRunner()

    result = runner.invoke(
        cli,
        args=["outline", "--format", "llms-txt"],
        env={"ABOUT_OUTLINE_URL": TESTING_OUTLINE_FILE},
        catch_exceptions=False,
    )
    assert result.exit_code == 0, result.output

    assert "Things to remember when working with Testing" in result.output
    assert "for use in documentation examples" in result.output
    assert "RFC 2606" not in result.output, (
        "The text must not be included within the non-optional bundle"
    )


def test_outline_cli_llms_txt_optional():
    runner = CliRunner()

    result = runner.invoke(
        cli,
        args=["outline", "--format", "llms-txt", "--optional"],
        env={"ABOUT_OUTLINE_URL": TESTING_OUTLINE_FILE},
        catch_exceptions=False,
    )
    assert result.exit_code == 0, result.output

    assert "Things to remember when working with Testing" in result.output
    assert "for use in documentation examples" in result.output
    assert "RFC 2606" in result.output, "The text must be included within the optional bundle"


def test_outline_cli_url_argument():
    runner = CliRunner()

    result = runner.invoke(
        cli,
        args=["outline", "--url", TESTING_OUTLINE_FILE],
        catch_exceptions=False,
    )
    assert result.exit_code == 0, result.output

    assert "# Testing" in result.output
    assert "Things to remember when working with Testing" in result.output
    assert "Example Domain" in result.output


def test_outline_cli_url_envvar():
    runner = CliRunner()

    result = runner.invoke(
        cli,
        args=["outline"],
        env={"ABOUT_OUTLINE_URL": TESTING_OUTLINE_FILE},
        catch_exceptions=False,
    )
    assert result.exit_code == 0, result.output

    assert "# Testing" in result.output
    assert "Things to remember when working with Testing" in result.output
    assert "Example Domain" in result.output


def test_outline_get_section_names(cratedb_outline_builtin):
    names = cratedb_outline_builtin.get_section_names()
    assert "Docs" in names
    assert "Optional" in names


def test_outline_item_titles_all(cratedb_outline_builtin):
    titles = cratedb_outline_builtin.get_item_titles()
    assert "CrateDB reference documentation" in titles
    assert "CrateDB SQL reference: Syntax" in titles
    assert "Concept: Resiliency" in titles
    assert len(titles) >= 30


def test_outline_item_titles_docs(cratedb_outline_builtin):
    titles = cratedb_outline_builtin.get_item_titles(section_name="Docs")
    assert "CrateDB reference documentation" in titles
    assert len(titles) >= 15


def test_outline_get_section(cratedb_outline_builtin):
    section_examples = cratedb_outline_builtin.get_section("Examples")
    titles = [item.title for item in section_examples.items]
    assert "CrateDB GTFS / GTFS-RT Transit Data Demo" in titles


def test_outline_section_not_found(cratedb_outline_builtin):
    section_not_found = cratedb_outline_builtin.get_section("Not Found")
    assert section_not_found is None


def test_outline_section_items_list(cratedb_outline_builtin):
    items = cratedb_outline_builtin.find_items(section_name="Docs").to_list()
    assert items[0]["title"] == "CrateDB README"


def test_outline_section_items_objects(cratedb_outline_builtin):
    items = cratedb_outline_builtin.find_items(section_name="Docs")
    assert items[0].title == "CrateDB README"


def test_outline_section_items_not_found(cratedb_outline_builtin):
    with pytest.raises(ValueError) as ex:
        cratedb_outline_builtin.find_items(section_name="Not Found")
    assert ex.match("Section 'Not Found' not found")


def test_outline_section_all_items(cratedb_outline_builtin):
    items = cratedb_outline_builtin.find_items()
    assert len(items) >= 30


def test_outline_find_items_list(cratedb_outline_builtin):
    items = cratedb_outline_builtin.find_items(title="gtfs").to_list()
    assert "Capture GTFS and GTFS-RT data" in items[0]["description"]


def test_outline_find_items_objects(cratedb_outline_builtin):
    items = cratedb_outline_builtin.find_items(title="gtfs")
    assert "Capture GTFS and GTFS-RT data" in items[0].description


def test_outline_find_items_not_found_in_section(cratedb_outline_builtin):
    items = cratedb_outline_builtin.find_items(title="gtfs", section_name="Docs")
    assert items == []


def test_outline_find_items_not_found_anywhere(cratedb_outline_builtin):
    items = cratedb_outline_builtin.find_items(title="foobar")
    assert items == []


def test_outline_with_valid_file_url():
    outline = CrateDbKnowledgeOutline.load(CRATEDB_OUTLINE_FILE)
    names = outline.get_section_names()
    assert "Docs" in names
    assert "Optional" in names


def test_outline_with_valid_http_url():
    outline = CrateDbKnowledgeOutline.load(CRATEDB_OUTLINE_URL)
    names = outline.get_section_names()
    assert "Docs" in names
    assert "Optional" in names


def test_outline_with_invalid_file_url():
    with pytest.raises(FileNotFoundError) as ex:
        CrateDbKnowledgeOutline.load("foobar.yaml")
    assert ex.match("Outline file not found: foobar.yaml")


def test_outline_with_invalid_http_url(monkeypatch):
    # Simulate a 404 response for an HTTP URL
    class FakeResponse:
        status_code = 404
        raise_for_status = lambda self: (_ for _ in ()).throw(requests.HTTPError("404 Not Found"))  # noqa: E731

    monkeypatch.setattr(requests, "get", lambda *_: FakeResponse())
    with pytest.raises(FileNotFoundError) as ex:
        CrateDbKnowledgeOutline.load("https://example.com/not-found.yaml")
    assert ex.match("Outline file not found")


def test_outline_with_non_yaml_content(tmp_path):
    non_yaml = tmp_path / "bad.txt"
    non_yaml.write_text("not: valid: yaml: [")
    with pytest.raises(Exception) as ex:
        CrateDbKnowledgeOutline.load(str(non_yaml))
    assert "YAML" in str(ex.value) or "mapping" in str(ex.value)


def test_outline_with_auth_required_http_url(monkeypatch):
    # Simulate a 401 response
    class Unauthorized:
        status_code = 401
        raise_for_status = lambda self: (_ for _ in ()).throw(  # noqa: E731
            requests.HTTPError("401 Unauthorized")
        )

    monkeypatch.setattr(requests, "get", lambda *_: Unauthorized())
    with pytest.raises(FileNotFoundError) as ex:
        CrateDbKnowledgeOutline.load("https://secure.example.com/outline.yaml")
    assert ex.match("Outline file not found")


def test_outline_with_io_error(monkeypatch):
    """Test that CrateDbKnowledgeOutline.read() properly handles IOError."""

    # Mock the to_io function to raise IOError
    def mock_to_io(url):
        class MockContextManager:
            def __enter__(self):
                raise IOError("Simulated IO error")

            def __exit__(self, exc_type, exc_val, exc_tb):
                pass

        return MockContextManager()

    monkeypatch.setattr("pueblo.io.to_io", mock_to_io)

    # Create outline instance with a URL and verify exception
    outline = CrateDbKnowledgeOutline(url="dummy://url")
    with pytest.raises(ValueError) as excinfo:
        outline.read()

    # Verify error message format
    assert str(excinfo.value).startswith("Failed to read outline from dummy://url:")
    assert "Simulated IO error" in str(excinfo.value)
