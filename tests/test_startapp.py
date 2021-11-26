from pathlib import Path

from typer.testing import CliRunner

from fastapi_cli.main import app

runner = CliRunner()

CREATED_SUCCESSFULLY = "FastAPI app created successfully! 🎉\n"
ALREADY_EXISTS = "Folder 'demo' already exists. 😞\n"


def test_startproject_default(tmp_path: Path):
    with runner.isolated_filesystem(temp_dir=tmp_path):
        result = runner.invoke(app, ["startapp", "demo"])
        assert result.output == CREATED_SUCCESSFULLY
        assert result.exit_code == 0
