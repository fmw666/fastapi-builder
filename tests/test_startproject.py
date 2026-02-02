from pathlib import Path

from typer.testing import CliRunner
from utils import rm_tmp_dir

from fastapi_builder.main import app

runner = CliRunner()

CREATED_SUCCESSFULLY = "\nFastAPI project created successfully! 🎉\n"
ALREADY_EXISTS = "\nFolder 'demo' already exists. 😞\n"


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


CURRENT_PATH = "."

test_startproject_default(Path(CURRENT_PATH))
test_startproject_already_exists(Path(CURRENT_PATH))

rm_tmp_dir(CURRENT_PATH)
