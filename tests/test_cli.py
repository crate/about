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


def test_cli_build(caplog, tmp_path):
    runner = CliRunner()

    result = runner.invoke(
        cli,
        args=["build"],
        env={"OUTDIR": str(tmp_path)},
        catch_exceptions=False,
    )
    assert result.exit_code == 0, result.output

    assert "Building llms-txt" in caplog.text
    assert "Dumping outline source file" in caplog.text
    assert "Generating llms-txt files" in caplog.text
    assert "Ready." in caplog.text

    # Verify that the expected output files are created
    assert (tmp_path / "llms.txt").exists()
    assert (tmp_path / "llms-full.txt").exists()


def test_cli_build_without_outdir():
    runner = CliRunner()

    # Test without OUTDIR environment variable.
    result = runner.invoke(
        cli,
        args=["build"],
        env={},  # No OUTDIR set
        catch_exceptions=False,
    )

    # Verify appropriate error handling.
    assert result.exit_code != 0, result.output
    assert "Error: Missing option '--outdir' / '-o'" in result.output
