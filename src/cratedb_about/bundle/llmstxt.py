import dataclasses
import logging
import shutil
import sys
from importlib import resources

if sys.version_info < (3, 11):
    from importlib.abc import Traversable
else:
    from importlib.resources.abc import Traversable
from pathlib import Path

from markdown import markdown

from cratedb_about import CrateDbKnowledgeOutline
from cratedb_about.bundle.util import count_tokens
from cratedb_about.outline import OutlineDocument
from cratedb_about.util import get_hostname, get_now

logger = logging.getLogger(__name__)


@dataclasses.dataclass
class LllmsTxtBuilder:
    """
    Generate llms.txt files.

    This is a base class intended to be subclassed. The non-init fields
    (outline, readme_md, outline_yaml) should be initialized by subclasses.
    """

    outline_url: str
    outdir: Path
    outline: OutlineDocument = dataclasses.field(init=False)
    readme_md: Traversable = dataclasses.field(init=False)
    outline_yaml: Traversable = dataclasses.field(init=False)

    def run(self):
        logger.info(f"Creating bundle. Format: llms-txt. Output directory: {self.outdir}")
        self.outdir.mkdir(parents=True, exist_ok=True)

        logger.info("Copying source and documentation files")
        self.copy_readme()
        self.copy_sources()

        # Generate llms-txt resources.
        # See also https://github.com/crate/about/issues/39
        #
        # - The `llms.txt` is just a Markdown file, unexpanded. It is essentially a sitemap,
        #   listing all the pages in the documentation.
        # - The `llms-full.txt` contains the entire documentation, expanded from the `llms.txt`
        #   file. Note this may exceed the context window of your LLM.
        llms_txt = Path(self.outdir / "llms.txt")
        llms_txt_full = Path(self.outdir / "llms-full.txt")

        llms_txt.write_text(self.outline.to_markdown())
        llms_txt_full.write_text(self.outline.to_llms_txt(optional=False))

        count_tokens(llms_txt_full)

        return self

    def copy_readme(self):
        """
        Provide README / "About" information to the bundle, in Markdown and HTML formats.
        """
        readme_md = self.outdir / "readme.md"
        shutil.copy(
            str(self.readme_md),
            readme_md,
        )
        try:
            readme_md_text = readme_md.read_text()
            readme_md_text = readme_md_text.format(host=get_hostname(), timestamp=get_now())
            (self.outdir / "readme.html").write_text(markdown(readme_md_text))
        except Exception as e:
            logger.warning(f"Failed to generate HTML readme: {e}")

    def copy_sources(self):
        """
        Provide the source document in the original YAML format, but also converted to HTML.
        The intermediary Markdown format is already covered by the `llms.txt` file itself.
        """
        shutil.copy(
            str(self.outline_yaml),
            self.outdir / "outline.yaml",
        )
        try:
            Path(self.outdir / "outline.html").write_text(self.outline.to_html())
        except Exception as e:
            logger.warning(f"Failed to generate HTML outline: {e}")


@dataclasses.dataclass
class CrateDbLllmsTxtBuilder(LllmsTxtBuilder):
    """
    Generate llms.txt files for CrateDB.
    """

    readme_md: Traversable = resources.files("cratedb_about.bundle") / "readme.md"
    outline_yaml: Traversable = resources.files("cratedb_about.outline") / "cratedb-outline.yaml"

    def __post_init__(self):
        self.outline = CrateDbKnowledgeOutline.load(self.outline_url)
