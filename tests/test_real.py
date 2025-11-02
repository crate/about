from click.testing import CliRunner

from cratedb_about.cli import cli


def test_outline_cli_llms_txt_real():
    """
    Validate processing the real `src/cratedb_about/outline/cratedb-outline.yaml`.
    """
    runner = CliRunner()

    result = runner.invoke(
        cli,
        args=["outline", "--format", "llms-txt"],
        catch_exceptions=False,
    )
    assert result.exit_code == 0, result.output

    assert "CrateDB is a distributed database written in Java" in result.output
    assert "CrateDB node-specific settings" in result.output
    assert "CrateDB Toolkit: Import example datasets" in result.output
