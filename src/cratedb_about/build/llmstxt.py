# ruff: noqa: S603, S607
import dataclasses
import logging
import shutil
import subprocess
from importlib import resources
from pathlib import Path

logger = logging.getLogger(__name__)


@dataclasses.dataclass
class LllmsTxtBuilder:
    """
    Build llms.txt files for CrateDB.
    """

    outdir: Path

    def run(self):
        logger.info(f"Building llms-txt. Output directory: {self.outdir}")
        self.outdir.mkdir(parents=True, exist_ok=True)

        logger.info("Copying source and documentation files")
        shutil.copy(
            str(resources.files("cratedb_about.build") / "llmstxt-about.md"),
            self.outdir / "readme.md",
        )
        shutil.copy(
            str(resources.files("cratedb_about.outline") / "cratedb-outline.yaml"),
            self.outdir / "outline.yaml",
        )

        logger.info("Dumping outline source file")
        subprocess.run(
            ["cratedb-about", "outline", "--format=markdown"],
            stdout=open(f"{self.outdir}/outline.md", "w"),
            check=True,
        )

        logger.info("Generating llms-txt files")
        subprocess.run(
            ["llms_txt2ctx", "--optional=false", f"{self.outdir}/outline.md"],
            stdout=open(f"{self.outdir}/llms.txt", "w"),
            check=True,
        )
        subprocess.run(
            ["llms_txt2ctx", "--optional=true", f"{self.outdir}/outline.md"],
            stdout=open(f"{self.outdir}/llms-full.txt", "w"),
            check=True,
        )
