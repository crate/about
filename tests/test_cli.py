from click.testing import CliRunner

from cratedb_about.cli import cli


def test_cli_version():
    runner = CliRunner()

    result = runner.invoke(
        cli,
        args="--version",
        catch_exceptions=False,
    )
    assert result.exit_code == 0, result.output

    assert "cli, version" in result.output


def test_cli_help():
    runner = CliRunner()

    result = runner.invoke(
        cli,
        args="--help",
        catch_exceptions=False,
    )
    assert result.exit_code == 0, result.output

    assert "Options:" in result.output
    assert "Ask questions about CrateDB" in result.output
    assert "Display the outline of the CrateDB documentation" in result.output


def test_cli_list_questions():
    runner = CliRunner()

    result = runner.invoke(
        cli,
        args=["list-questions"],
        catch_exceptions=False,
    )
    assert result.exit_code == 0, result.output

    assert "Please tell me how CrateDB stores data." in result.output


def test_cli_outline():
    runner = CliRunner()

    result = runner.invoke(
        cli,
        args=["outline", "--format", "markdown"],
        catch_exceptions=False,
    )
    assert result.exit_code == 0, result.output

    assert "# CrateDB" in result.output
    assert "Things to remember when working with CrateDB" in result.output
    assert "Concept: Clustering" in result.output
