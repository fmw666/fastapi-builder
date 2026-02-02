from pathlib import Path
from typer.testing import CliRunner
from fastapi_builder.main import app

runner = CliRunner()
CREATED_SUCCESSFULLY = "\nFastAPI project created successfully! 🎉\n"

def test_postgres_project(tmp_path: Path):
    with runner.isolated_filesystem(temp_dir=tmp_path):
        # Use poetry to check pyproject.toml
        result = runner.invoke(app, ["startproject", "pg_demo", "--database", "PostgreSQL", "--packaging", "poetry"], catch_exceptions=False)
        assert result.exit_code == 0
        assert CREATED_SUCCESSFULLY in result.output
        
        # Check pyproject.toml
        with open("pg_demo/pyproject.toml", "r") as f:
            content = f.read()
            assert "asyncpg" in content
            assert "psycopg2-binary" in content
            assert "aiomysql" not in content

def test_sqlite_project(tmp_path: Path):
    with runner.isolated_filesystem(temp_dir=tmp_path):
        # Use pip to check requirements.txt
        result = runner.invoke(app, ["startproject", "sqlite_demo", "--database", "SQLite", "--packaging", "pip"], catch_exceptions=False)
        assert result.exit_code == 0
        assert CREATED_SUCCESSFULLY in result.output
        
        # Check requirements.txt
        with open("sqlite_demo/requirements.txt", "r") as f:
            content = f.read()
            assert "aiosqlite" in content
            assert "pymysql" not in content

        # Check fastapi-builder.ini
        with open("sqlite_demo/fastapi-builder.ini", "r") as f:
             content = f.read()
             assert "database = SQLite" in content
