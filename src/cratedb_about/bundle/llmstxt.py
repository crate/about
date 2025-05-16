import dataclasses
import logging
import shutil
from importlib import resources
from pathlib import Path

from markdown import markdown

from cratedb_about import CrateDbKnowledgeOutline
from cratedb_about.util import get_hostname, get_now

logger = logging.getLogger(__name__)


@dataclasses.dataclass
class LllmsTxtBuilder:
    """
    Build llms.txt files for CrateDB.
    """

    outline_url: str
    outdir: Path

    def run(self):
        logger.info(f"Creating bundle. Format: llms-txt. Output directory: {self.outdir}")
        self.outdir.mkdir(parents=True, exist_ok=True)

        logger.info("Copying source and documentation files")
        self.copy_readme()
        self.copy_sources()

        outline = CrateDbKnowledgeOutline.load(self.outline_url)
        Path(self.outdir / "outline.md").write_text(outline.to_markdown())
        # TODO: Explore how to optimize this procedure that both steps do not need
        #       to acquire and process data redundantly.
        Path(self.outdir / "llms.txt").write_text(outline.to_llms_txt())
        Path(self.outdir / "llms-full.txt").write_text(outline.to_llms_txt(optional=True))

        return self

    def copy_readme(self):
        readme_md = self.outdir / "readme.md"
        shutil.copy(
            str(resources.files("cratedb_about.bundle") / "readme.md"),
            readme_md,
        )
        try:
            readme_md_text = readme_md.read_text()
            readme_md_text = readme_md_text.format(host=get_hostname(), timestamp=get_now())
            (self.outdir / "readme.html").write_text(markdown(readme_md_text))
        except Exception as e:
            logger.warning(f"Failed to generate HTML readme: {e}")

    def copy_sources(self):
        shutil.copy(
            str(resources.files("cratedb_about.outline") / "cratedb-outline.yaml"),
            self.outdir / "outline.yaml",
        )
