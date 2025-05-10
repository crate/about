from importlib import resources

from cratedb_about.outline.model import OutlineDocument


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

    @classmethod
    def read(cls):
        return resources.read_text("cratedb_about.outline", "cratedb-outline.yaml")

    @classmethod
    def load(cls) -> "OutlineDocument":
        return OutlineDocument.from_yaml(cls.read())
