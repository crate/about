import pytest

from cratedb_about import CrateDbKnowledgeOutline
from cratedb_about.outline import OutlineDocument


@pytest.fixture
def cratedb_outline_builtin() -> OutlineDocument:
    return CrateDbKnowledgeOutline.load()


def test_outline_get_section_names(cratedb_outline_builtin):
    names = cratedb_outline_builtin.get_section_names()
    assert "Docs" in names
    assert "Optional" in names


def test_outline_item_titles_all(cratedb_outline_builtin):
    titles = cratedb_outline_builtin.get_item_titles()
    assert "CrateDB reference documentation" in titles
    assert "CrateDB SQL syntax" in titles
    assert "Concept: Resiliency" in titles
    assert len(titles) >= 30


def test_outline_item_titles_docs(cratedb_outline_builtin):
    titles = cratedb_outline_builtin.get_item_titles(section_name="Docs")
    assert "CrateDB reference documentation" in titles
    assert len(titles) < 15


def test_outline_get_section(cratedb_outline_builtin):
    section_examples = cratedb_outline_builtin.get_section("Examples")
    titles = [item.title for item in section_examples.items]
    assert "CrateDB GTFS / GTFS-RT Transit Data Demo" in titles


def test_outline_section_not_found(cratedb_outline_builtin):
    section_not_found = cratedb_outline_builtin.get_section("Not Found")
    assert section_not_found is None


def test_outline_section_items_as_dict(cratedb_outline_builtin):
    items = cratedb_outline_builtin.find_items(section_name="Docs", as_dict=True)
    assert items[0]["title"] == "CrateDB README"


def test_outline_section_items_as_objects(cratedb_outline_builtin):
    items = cratedb_outline_builtin.find_items(section_name="Docs")
    assert items[0].title == "CrateDB README"


def test_outline_section_items_not_found(cratedb_outline_builtin):
    with pytest.raises(ValueError) as ex:
        cratedb_outline_builtin.find_items(section_name="Not Found")
    assert ex.match("Section 'Not Found' not found")


def test_outline_section_all_items(cratedb_outline_builtin):
    items = cratedb_outline_builtin.find_items()
    assert len(items) >= 30


def test_outline_find_items_as_dict(cratedb_outline_builtin):
    items = cratedb_outline_builtin.find_items(title="gtfs", as_dict=True)
    assert "Capture GTFS and GTFS-RT data" in items[0]["description"]


def test_outline_find_items_as_objects(cratedb_outline_builtin):
    items = cratedb_outline_builtin.find_items(title="gtfs")
    assert "Capture GTFS and GTFS-RT data" in items[0].description


def test_outline_find_items_not_found_in_section(cratedb_outline_builtin):
    items = cratedb_outline_builtin.find_items(title="gtfs", section_name="Docs")
    assert items == []


def test_outline_find_items_not_found_anywhere(cratedb_outline_builtin):
    items = cratedb_outline_builtin.find_items(title="foobar")
    assert items == []


def test_outline_with_valid_file_url():
    outline = CrateDbKnowledgeOutline.load("src/cratedb_about/outline/cratedb-outline.yaml")
    names = outline.get_section_names()
    assert "Docs" in names
    assert "Optional" in names


def test_outline_with_valid_http_url():
    outline = CrateDbKnowledgeOutline.load(
        "https://github.com/crate/about/raw/refs/tags/v0.0.3/src/cratedb_about/outline/cratedb-outline.yaml"
    )
    names = outline.get_section_names()
    assert "Docs" in names
    assert "Optional" in names


def test_outline_with_invalid_url():
    with pytest.raises(FileNotFoundError) as ex:
        CrateDbKnowledgeOutline.load("foobar.yaml")
    assert ex.match("No such file or directory")
