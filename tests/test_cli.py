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


def test_cli_bundle(caplog, tmp_path):
    runner = CliRunner()

    # Invoke command.
    result = runner.invoke(
        cli,
        args=["bundle"],
        env={"OUTDIR": str(tmp_path)},
        catch_exceptions=False,
    )
    assert result.exit_code == 0, result.output

    # Verify log output.
    assert "Bundling llms-txt" in caplog.text
    assert "Ready." in caplog.text

    # Verify that the expected output files have been created.
    assert (tmp_path / "llms.txt").exists()
    assert (tmp_path / "llms-full.txt").exists()


def test_cli_bundle_without_outdir():
    runner = CliRunner()

    # Invoke command without OUTDIR environment variable.
    result = runner.invoke(
        cli,
        args=["bundle"],
        env={},  # No OUTDIR set
        catch_exceptions=False,
    )

    # Verify appropriate error handling.
    assert result.exit_code != 0, result.output
    assert "Error: Missing option '--outdir' / '-o'" in result.output


def test_cli_bundle_invalid_format(tmp_path):
    runner = CliRunner()

    # Invoke command.
    result = runner.invoke(
        cli,
        args=["bundle", "--format", "foobar"],
        env={"OUTDIR": str(tmp_path)},
        catch_exceptions=False,
    )

    # Verify appropriate error handling.
    assert result.exit_code != 0, result.output
    assert "Error: Invalid output format: foobar" in result.output
