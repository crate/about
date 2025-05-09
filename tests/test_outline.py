import pytest

from cratedb_about import CrateDbKnowledgeOutline
from cratedb_about.outline.model import OutlineDocument


@pytest.fixture
def cratedb_outline() -> OutlineDocument:
    return CrateDbKnowledgeOutline.load()


def test_outline_section_names(cratedb_outline):
    names = cratedb_outline.section_names
    assert "Docs" in names
    assert "Optional" in names


def test_outline_get_section(cratedb_outline):
    section_examples = cratedb_outline.get_section("Examples")
    titles = [item.title for item in section_examples.items]
    assert "CrateDB GTFS / GTFS-RT Transit Data Demo" in titles


def test_outline_section_not_found(cratedb_outline):
    section_not_found = cratedb_outline.get_section("Not Found")
    assert section_not_found is None


def test_outline_section_items_as_dict(cratedb_outline):
    items = cratedb_outline.get_items("Docs", as_dict=True)
    assert items[0]["title"] == "CrateDB README"


def test_outline_section_items_as_objects(cratedb_outline):
    items = cratedb_outline.get_items("Docs")
    assert items[0].title == "CrateDB README"


def test_outline_section_items_not_found(cratedb_outline):
    with pytest.raises(ValueError) as ex:
        cratedb_outline.get_items("Not Found")
    assert ex.match("Section 'Not Found' not found")


def test_outline_section_all_items(cratedb_outline):
    items = cratedb_outline.get_items()
    assert len(items) >= 30
