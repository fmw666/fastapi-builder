from pathlib import Path

from typer.testing import CliRunner

from fastapi_cli.main import app

runner = CliRunner()

CREATED_SUCCESSFULLY = "FastAPI project created successfully! 🎉\n"
ALREADY_EXISTS = "Folder 'demo' already exists. 😞\n"


def test_startproject_default(tmp_path: Path):
    with runner.isolated_filesystem(temp_dir=tmp_path):
        result = runner.invoke(app, ["startproject", "demo"])
        assert result.output == CREATED_SUCCESSFULLY
        assert result.exit_code == 0


def test_startproject_already_exists(tmp_path: Path):
    with runner.isolated_filesystem(temp_dir=tmp_path):
        result = runner.invoke(app, ["startproject", "demo"])
        assert result.output == CREATED_SUCCESSFULLY
        assert result.exit_code == 0

        result = runner.invoke(app, ["startproject", "demo"])
        assert result.output == ALREADY_EXISTS
        assert result.exit_code == 0
