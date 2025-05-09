import typing as t
from importlib import resources
from io import StringIO

from attr import Factory
from attrs import define

from cratedb_about.util import DictTools, Dumpable, Metadata


class CrateDbKnowledgeOutline:
    """
    Load CrateDB knowledge outline from YAML file `cratedb-outline.yaml`.

    This class provides methods to read the raw YAML content and to load it
    as a structured document model.

    Examples:
        ```python
        # Get raw YAML content
        yaml_content = CrateDbKnowledgeOutline.read()

        # Load as structured document
        outline = CrateDbKnowledgeOutline.load()

        # Get all section names
        sections = outline.section_names
        ```
    """

    @classmethod
    def read(cls):
        return resources.read_text("cratedb_about.outline", "cratedb-outline.yaml")

    @classmethod
    def load(cls) -> "OutlineDocument":
        return OutlineDocument.from_yaml(cls.read())


@define
class OutlineHeader(DictTools):
    """Data model element of an `OutlineDocument`"""

    title: t.Union[str, None] = None
    link: t.Union[str, None] = None
    description: str = ""


@define
class OutlineItem(DictTools):
    """Data model element of an `OutlineDocument`"""

    title: str
    link: str
    description: str


@define
class OutlineSection(DictTools):
    """Data model element of an `OutlineDocument`"""

    name: str
    items: t.List[OutlineItem] = Factory(list)


@define
class OutlineData(DictTools):
    """Data model element of an `OutlineDocument`"""

    header: OutlineHeader = Factory(OutlineHeader)
    sections: t.List[OutlineSection] = Factory(list)


@define
class OutlineDocument(Dumpable):
    """
    Manage a set of curated knowledgebase documents.

    - It is the root element of the data model.
    - It provides conversion utility functions.
    - Also, it provides convenience functionality to query the data model.
    """

    meta: Metadata = Factory(lambda: Metadata(version=1, type="outline"))
    data: OutlineData = Factory(OutlineData)

    def to_markdown(self) -> str:
        """Convert outline into Markdown format."""
        buffer = StringIO()
        buffer.write(f"# {self.data.header.title or 'Knowledge Outline'}\n\n")
        buffer.write(f"{self.data.header.description.strip()}\n\n")
        for section in self.data.sections:
            buffer.write(f"## {section.name}\n\n")
            for item in section.items:
                buffer.write(f"- [{item.title}]({item.link}): {item.description}\n")
            buffer.write("\n")
        return buffer.getvalue().strip()

    @property
    def section_names(self) -> t.List[str]:
        """Return all section names."""
        return [section.name for section in self.data.sections]

    def get_section(self, name: str) -> t.Optional[OutlineSection]:
        """
        Return an individual section by name.

        Args:
            name: The name of the section to retrieve

        Returns:
            The section if found, None otherwise

        Example:
            ```python
            outline = CrateDbKnowledgeOutline.load()
            section = outline.get_section("Getting Started")
            ```
        """
        for section in self.data.sections:
            if section.name == name:
                return section
        return None

    def get_items(
        self, section_name: t.Optional[str] = None, as_dict: bool = False
    ) -> t.Union[t.List[t.Dict[str, t.Any]], t.List[OutlineItem]]:
        """Return `OutlineItem` elements from an individual section, or return all items."""
        buffer = OutlineSection(name="_")
        if section_name is None:
            for section in self.data.sections:
                buffer.items += section.items
        else:
            section_ = self.get_section(name=section_name)
            if not section_:
                raise ValueError(
                    f"Section '{section_name}' not found. Available sections: {self.section_names}"
                )
            buffer.items += section_.items
        if as_dict:
            return buffer.to_dict()["items"]
        return buffer.items
