from pathlib import Path

from typer.testing import CliRunner

from fastapi_builder.main import app

runner = CliRunner()


def test_venv_on_macos_uses_posix_activate(tmp_path: Path, monkeypatch):
    """The `venv on` command must work on macOS instead of raising KeyError."""
    monkeypatch.chdir(tmp_path)
    Path("myenv").mkdir()
    calls = []
    monkeypatch.setattr("platform.system", lambda: "Darwin")
    monkeypatch.setattr("os.system", lambda cmd: calls.append(cmd) or 0)
    result = runner.invoke(app, ["venv", "on"])
    assert result.exit_code == 0
    assert "myenv" in result.output
    assert calls == ["source ./myenv/bin/activate"]
