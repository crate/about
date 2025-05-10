import pytest

from cratedb_about import CrateDbKnowledgeOutline
from cratedb_about.outline.model import OutlineDocument


@pytest.fixture
def cratedb_outline() -> OutlineDocument:
    return CrateDbKnowledgeOutline.load()


def test_outline_get_section_names(cratedb_outline):
    names = cratedb_outline.get_section_names()
    assert "Docs" in names
    assert "Optional" in names


def test_outline_item_titles_all(cratedb_outline):
    titles = cratedb_outline.get_item_titles()
    assert "CrateDB reference documentation" in titles
    assert "CrateDB SQL syntax" in titles
    assert "Concept: Resiliency" in titles
    assert len(titles) >= 30


def test_outline_item_titles_docs(cratedb_outline):
    titles = cratedb_outline.get_item_titles(section_name="Docs")
    assert "CrateDB reference documentation" in titles
    assert len(titles) < 15


def test_outline_get_section(cratedb_outline):
    section_examples = cratedb_outline.get_section("Examples")
    titles = [item.title for item in section_examples.items]
    assert "CrateDB GTFS / GTFS-RT Transit Data Demo" in titles


def test_outline_section_not_found(cratedb_outline):
    section_not_found = cratedb_outline.get_section("Not Found")
    assert section_not_found is None


def test_outline_section_items_as_dict(cratedb_outline):
    items = cratedb_outline.find_items(section_name="Docs", as_dict=True)
    assert items[0]["title"] == "CrateDB README"


def test_outline_section_items_as_objects(cratedb_outline):
    items = cratedb_outline.find_items(section_name="Docs")
    assert items[0].title == "CrateDB README"


def test_outline_section_items_not_found(cratedb_outline):
    with pytest.raises(ValueError) as ex:
        cratedb_outline.find_items(section_name="Not Found")
    assert ex.match("Section 'Not Found' not found")


def test_outline_section_all_items(cratedb_outline):
    items = cratedb_outline.find_items()
    assert len(items) >= 30


def test_outline_find_items_as_dict(cratedb_outline):
    items = cratedb_outline.find_items(title="gtfs", as_dict=True)
    assert "Capture GTFS and GTFS-RT data" in items[0]["description"]


def test_outline_find_items_as_objects(cratedb_outline):
    items = cratedb_outline.find_items(title="gtfs")
    assert "Capture GTFS and GTFS-RT data" in items[0].description


def test_outline_find_items_not_found_in_section(cratedb_outline):
    items = cratedb_outline.find_items(title="gtfs", section_name="Docs")
    assert items == []


def test_outline_find_items_not_found_anywhere(cratedb_outline):
    items = cratedb_outline.find_items(title="foobar")
    assert items == []
