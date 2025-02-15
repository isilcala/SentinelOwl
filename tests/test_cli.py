from click.testing import CliRunner
from sentinelowl.cli import cli

def test_cli_version():
    """Test the version command"""
    runner = CliRunner()
    result = runner.invoke(cli, ["version"])
    assert result.exit_code == 0
    assert "SentinelOwl version" in result.output

# def test_cli_start():
#     """Test the start command"""
#     runner = CliRunner()
#     result = runner.invoke(cli, ["start", "--camera-url", "http://192.168.50.231/webcam/?action=snapshot"])
#     assert result.exit_code == 0
#     assert "Starting SentinelOwl" in result.output