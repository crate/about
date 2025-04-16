import typing as t

import click

from cratedb_about.core import CrateDBConversation
from cratedb_about.model import Example


@click.group()
@click.version_option()
@click.pass_context
def cli(ctx: click.Context) -> None:
    pass


@cli.command()
@click.argument("question", type=str, required=False)
@click.option("--backend", type=click.Choice(["openai", "claude"]), default="openai")
def ask(question: str, backend: t.Literal["claude", "openai"]):
    """
    Ask questions about CrateDB.

    Requires:
      - OpenAI backend: Set OPENAI_API_KEY environment variable
      - Claude backend: Set ANTHROPIC_API_KEY environment variable
    """
    wizard = CrateDBConversation(
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
def list_questions():
    """
    List a few example questions about CrateDB.
    """
    click.echo("\n".join(Example.questions))
