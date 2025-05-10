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
        yaml_content = CrateDbKnowledgeOutline().read()

        # Load as structured document
        outline = CrateDbKnowledgeOutline.load()

        # Get all section names
        sections = outline.get_section_names()
        ```
    """

    url: t.Optional[str] = None

    BUILTIN = resources.files("cratedb_about.outline") / "cratedb-outline.yaml"

    def read(self) -> str:
        """
        Load the file from an external URL or the built-in resource.

        Returns:
            String containing the raw YAML content.

        Raises:
            FileNotFoundError: If the URL points to a non-existent file.
            ValueError: If the URL is invalid or the content cannot be parsed.
        """
        if self.url is None:
            return self.BUILTIN.read_text()

        # Import universal I/O interface lazily, because it's only available when
        # installing the package including its `manyio` extra.
        from pueblo.io import to_io

        try:
            with to_io(self.url) as f:
                return f.read()
        except FileNotFoundError as e:
            raise FileNotFoundError(f"Outline file not found: {self.url}") from e
        except (ValueError, IOError) as e:
            raise ValueError(f"Failed to read outline from {self.url}: {str(e)}") from e

    @classmethod
    def load(cls, url: t.Optional[str] = None) -> "OutlineDocument":
        """
        Load the outline document from the specified URL or the built-in resource.

        Args:
            url: Optional URL to load the outline from. Can be a local file path,
                 an HTTP/HTTPS URL, one of many other remote resources, or None
                 to use the built-in resource.

        Returns:
            Parsed OutlineDocument instance.

        Raises:
            FileNotFoundError: If the URL points to a non-existent file.
            ValueError: If the URL is invalid or the content cannot be parsed.
        """
        return OutlineDocument.from_yaml(cls(url=url).read())
