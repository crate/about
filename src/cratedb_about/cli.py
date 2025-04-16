import sys
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
@click.option("--backend", type=str, default="openai")
def ask(question: str, backend: t.Literal["claude", "openai"]):
    """
    Ask questions about CrateDB.
    """
    wizard = CrateDBConversation(
        backend=backend,
        use_knowledge=True,
    )
    if not question:
        question = Example.questions[4]

    sys.stdout.write(f"Question: {question}\nAnswer:\n")
    sys.stdout.write(wizard.ask(question))
    sys.stdout.write("\n")


@cli.command()
def list_questions():
    """
    List a few example questions about CrateDB.
    """
    sys.stdout.write("\n".join(Example.questions))
    sys.stdout.write("\n")
