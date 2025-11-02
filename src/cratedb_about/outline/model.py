import typing as t
from io import StringIO
from unittest import mock

from attr import Factory
from attrs import define
from markdown import markdown

from cratedb_about.util import DictTools, Dumpable, Metadata, get_cache_client


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
    markdown_enabled: bool = True

    def __attrs_post_init__(self):
        # FIXME: Currently, `llms_txt` does not accept newlines in description fields.
        if isinstance(self.description, str):
            self.description = self.description.replace("\n", " ")


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


class OutlineItems(list):
    """List of `OutlineItem` elements, including additional features"""

    def to_list(self):
        return [item.to_dict() for item in self]


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
                if not item.markdown_enabled:
                    continue
                buffer.write(f"- [{item.title}]({item.link}): {item.description}\n")
            buffer.write("\n")
        return buffer.getvalue().strip()

    def to_html(self) -> str:
        """
        Convert outline into HTML format using Markdown as an intermediate step.
        """
        return markdown(self.to_markdown())

    def to_llms_txt(self, optional: bool = False) -> str:
        """
        Convert this outline into the llms.txt format.

        Args:
            optional: If True, include the optional sections in the output.

        Returns:
            The string representation of the context in llms.txt format.
        """

        def get_doc_content(url):
            """
            Fetch content from local file if in nbdev repo.

            Source: https://github.com/AnswerDotAI/llms-txt/blob/0.0.4/llms_txt/core.py#L74-L80
            Patched to invoke `raise_for_status()`.
            :return:
            """
            from urllib.parse import urlparse

            import httpx
            from llms_txt.core import _get_config, _local_docs_pth

            if (cfg := _get_config()) and url.startswith(cfg.doc_host):
                relative_path = urlparse(url).path.lstrip("/")
                local_path = _local_docs_pth(cfg) / relative_path
                if local_path.exists():
                    return local_path.read_text()
            response = httpx.get(url, follow_redirects=True)
            response.raise_for_status()
            return response.text

        # Patch `llms_txt` package to use caching via Hishel.
        # https://hishel.com/
        http_client = get_cache_client()
        with http_client as client:
            # Patch the client object.
            with mock.patch("llms_txt.core.httpx", client):
                # Import module lazily to relax dependency surface.
                import llms_txt

                llms_txt.core.get_doc_content = get_doc_content

                # Expand links and output in Markdown format.
                markdown = self.to_markdown()
                ctx = llms_txt.create_ctx(markdown, optional=optional, n_workers=None)
                return str(ctx)

    def get_item_titles(self, section_name: t.Optional[str] = None) -> t.List[str]:
        """
        Return all item titles across all sections.

        By default, return item titles from all sections.
        When `section_name` is provided, limit search to that section.
        """
        items_in = self.collect_items(section_name=section_name)
        return [item.title for item in items_in]

    def get_section_names(self) -> t.List[str]:
        """Return all section names."""
        return [section.name for section in self.data.sections]

    def get_section(self, name: str) -> t.Optional[OutlineSection]:
        """
        Return an individual section element by its name, or `None` if not found.

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

    def get_section_safe(self, name: str) -> OutlineSection:
        """
        Return an individual section element by its name, or raise an exception if not found.
        """
        section = self.get_section(name=name)
        if not section:
            raise ValueError(
                f"Section '{name}' not found. Available sections: {self.get_section_names()}"
            )
        return section

    def find_items(
        self,
        title: t.Optional[str] = None,
        section_name: t.Optional[str] = None,
    ) -> OutlineItems:
        """
        Find `OutlineItem` elements by their titles, per lower-cased "contains" search.

        By default, return all titles from all sections.
        When `title` is provided, search for matching titles.
        When `section_name` is provided, limit search to that section.
        When no item can be found, return an empty list.
        """
        items_in = self.collect_items(section_name=section_name)
        items_out = []
        needle = None
        if title:
            needle = title.casefold()
        for item in items_in:
            if not needle or needle in item.title.casefold():
                items_out.append(item)
        return OutlineItems(items_out)

    def collect_items(self, section_name: t.Optional[str] = None) -> t.List[OutlineItem]:
        """
        Return the list of `OutlineItem` elements, optionally filtered by `section_name`.
        """
        items = []
        if section_name is None:
            for section in self.data.sections:
                items += section.items
        else:
            section_ = self.get_section_safe(name=section_name)
            items += section_.items
        return items
