import dataclasses
import typing as t
from importlib import resources

from cratedb_about.outline.model import OutlineDocument


@dataclasses.dataclass
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
        sections = outline.get_section_names()
        ```
    """

    url: t.Optional[str] = None

    BUILTIN = resources.files("cratedb_about.outline") / "cratedb-outline.yaml"

    def read(self) -> str:
        if self.url is None:
            return self.BUILTIN.read_text()
        from pueblo.io import to_io

        with to_io(self.url) as f:
            return f.read()

    @classmethod
    def load(cls, url=None) -> "OutlineDocument":
        return OutlineDocument.from_yaml(cls(url=url).read())
