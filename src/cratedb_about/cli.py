import logging
import typing as t
from pathlib import Path

import click
from pueblo.util.cli import boot_click

from cratedb_about.build.llmstxt import LllmsTxtBuilder
from cratedb_about.outline import CrateDbKnowledgeOutline
from cratedb_about.query.core import CrateDbKnowledgeConversation
from cratedb_about.query.model import Example

logger = logging.getLogger(__name__)


@click.group()
@click.version_option()
@click.pass_context
def cli(ctx: click.Context) -> None:
    boot_click(ctx=ctx)


@cli.command()
@click.option(
    "--url",
    "-u",
    envvar="ABOUT_OUTLINE_URL",
    type=str,
    required=False,
    default=None,
    help="URL to the outline file. By default, the built-in outline is used.",
)
@click.option(
    "--format",
    "-f",
    "format_",
    type=click.Choice(["llms-txt", "markdown", "yaml", "json"]),
    default="markdown",
    help="Output format",
)
@click.option(
    "--optional",
    "-o",
    is_flag=True,
    help='When producing llms-txt output, include the "Optional" section',
)
def outline(
    url: str,
    format_: t.Literal["llms-txt", "markdown", "yaml", "json"] = "markdown",
    optional: bool = False,
) -> None:
    """
    Display the outline of the CrateDB documentation.

    Available output formats: llms-txt, Markdown, YAML, JSON.
    """
    cratedb_outline = CrateDbKnowledgeOutline.load(url=url)
    if format_ == "json":
        print(cratedb_outline.to_json())  # noqa: T201
    elif format_ == "yaml":
        print(cratedb_outline.to_yaml())  # noqa: T201
    elif format_ == "markdown":
        print(cratedb_outline.to_markdown())  # noqa: T201
    elif format_ == "llms-txt":
        print(cratedb_outline.to_llms_txt(optional=optional))  # noqa: T201
    else:
        raise ValueError(f"Invalid output format: {format_}")


@cli.command()
@click.option("--outdir", "-o", envvar="OUTDIR", type=Path, required=True)
def build(outdir: Path) -> None:
    """
    Invoke the build. Now: Generate `llms.txt` files.
    """
    builder = LllmsTxtBuilder(outdir=outdir)
    builder.run()
    logger.info("Ready.")


@cli.command()
@click.argument("question", type=str, required=False)
@click.option("--backend", type=click.Choice(["openai", "claude"]), default="openai")
def ask(question: str, backend: t.Literal["claude", "openai"]) -> None:
    """
    Ask questions about CrateDB.

    Requires:
      - OpenAI backend: Set OPENAI_API_KEY environment variable
      - Claude backend: Set ANTHROPIC_API_KEY environment variable
    """
    wizard = CrateDbKnowledgeConversation(
        backend=backend,
        use_knowledge=True,
    )
    if not question:
        # Use the AUTOINCREMENT question or fall back to the first question if not found
        default_question = next(
            (q for q in Example.questions if "AUTOINCREMENT" in q),
            Example.questions[0] if Example.questions else "What is CrateDB?",
        )
        question = default_question
    click.echo(f"Question: {question}\nAnswer:\n")
    click.echo(wizard.ask(question))


@cli.command()
def list_questions() -> None:
    """
    List a few example questions about CrateDB.
    """
    click.echo("\n".join(Example.questions))
