# ruff: noqa: S603, S607
import dataclasses
import logging
import shutil
from importlib import resources
from pathlib import Path

from cratedb_about import CrateDbKnowledgeOutline

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
        shutil.copy(
            str(resources.files("cratedb_about.bundle") / "llmstxt-about.md"),
            self.outdir / "readme.md",
        )
        shutil.copy(
            str(resources.files("cratedb_about.outline") / "cratedb-outline.yaml"),
            self.outdir / "outline.yaml",
        )

        # TODO: Explore how to optimize this procedure that both steps do not need
        #       to acquire and process data redundantly.
        outline = CrateDbKnowledgeOutline.load(self.outline_url)
        Path(self.outdir / "llms.txt").write_text(outline.to_llms_txt())
        Path(self.outdir / "llms-full.txt").write_text(outline.to_llms_txt(optional=True))
