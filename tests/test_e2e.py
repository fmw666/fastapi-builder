"""
End-to-End Test Script

In a temp directory under root:
1. Create project using fastapi startproject
2. Create venv and install dependencies
3. Start the project and verify it runs correctly
4. Clean up temp directory

Usage:
    # Run from fastapi-builder root directory
    python tests/test_e2e.py

    # Keep temp directory (for debugging)
    python tests/test_e2e.py --keep

    # Specify project name
    python tests/test_e2e.py --name myproject
"""

import argparse
import os
import platform
import shutil
import signal
import subprocess
import sys
import time
from pathlib import Path
from typing import Optional

# Fix Windows console encoding
if platform.system() == "Windows":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

try:
    import requests
except ImportError:
    print("Installing requests...")
    subprocess.run([sys.executable, "-m", "pip", "install", "requests", "-q"])
    import requests


# Configuration
DEFAULT_PROJECT_NAME = "test_project"
TEMP_DIR = ".test_temp"
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 8000
SERVER_STARTUP_TIMEOUT = 60  # seconds
SERVER_CHECK_INTERVAL = 2  # seconds


def get_root_dir() -> Path:
    """Get fastapi-builder root directory"""
    return Path(__file__).parent.parent


def get_venv_python(project_dir: Path) -> Path:
    """Get venv Python path"""
    if platform.system() == "Windows":
        return project_dir / "venv" / "Scripts" / "python.exe"
    return project_dir / "venv" / "bin" / "python"


def get_venv_pip(project_dir: Path) -> Path:
    """Get venv pip path"""
    if platform.system() == "Windows":
        return project_dir / "venv" / "Scripts" / "pip.exe"
    return project_dir / "venv" / "bin" / "pip"


def get_venv_uvicorn(project_dir: Path) -> Path:
    """Get venv uvicorn path"""
    if platform.system() == "Windows":
        return project_dir / "venv" / "Scripts" / "uvicorn.exe"
    return project_dir / "venv" / "bin" / "uvicorn"


def run_command(
    cmd: list,
    cwd: Optional[Path] = None,
    check: bool = True,
    timeout: Optional[int] = None,
) -> subprocess.CompletedProcess:
    """Run command and print output"""
    print(f"\n{'='*60}")
    print(f"Running: {' '.join(str(c) for c in cmd)}")
    if cwd:
        print(f"Working directory: {cwd}")
    print("=" * 60)

    result = subprocess.run(
        cmd,
        cwd=cwd,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=timeout,
    )

    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)

    if check and result.returncode != 0:
        raise RuntimeError(f"Command failed with return code: {result.returncode}")

    return result


def create_temp_dir(root_dir: Path) -> Path:
    """Create temp directory"""
    temp_dir = root_dir / TEMP_DIR
    if temp_dir.exists():
        print(f"Cleaning existing temp directory: {temp_dir}")
        shutil.rmtree(temp_dir)
    temp_dir.mkdir(parents=True)
    print(f"Created temp directory: {temp_dir}")
    return temp_dir


def cleanup_temp_dir(root_dir: Path):
    """Clean up temp directory"""
    temp_dir = root_dir / TEMP_DIR
    if temp_dir.exists():
        print(f"\nCleaning temp directory: {temp_dir}")
        shutil.rmtree(temp_dir)


def install_fastapi_builder(root_dir: Path):
    """Install fastapi-builder in development mode"""
    print("\n[1/6] Installing fastapi-builder (dev mode)...")
    run_command([sys.executable, "-m", "pip", "install", "-e", "."], cwd=root_dir)


def create_project(temp_dir: Path, project_name: str) -> Path:
    """Create project using fastapi startproject"""
    print(f"\n[2/6] Creating project: {project_name}")

    # Get fastapi command path (same directory as python executable)
    if platform.system() == "Windows":
        fastapi_cmd = Path(sys.executable).parent / "fastapi.exe"
    else:
        fastapi_cmd = Path(sys.executable).parent / "fastapi"

    run_command([str(fastapi_cmd), "startproject", project_name], cwd=temp_dir)

    project_dir = temp_dir / project_name
    if not project_dir.exists():
        raise RuntimeError(f"Project directory not created: {project_dir}")

    print(f"[OK] Project created: {project_dir}")
    return project_dir


def create_venv(project_dir: Path):
    """Create virtual environment"""
    print("\n[3/6] Creating virtual environment...")
    run_command([sys.executable, "-m", "venv", "venv"], cwd=project_dir)
    print("[OK] Virtual environment created")


def install_dependencies(project_dir: Path):
    """Install project dependencies"""
    print("\n[4/6] Installing dependencies...")
    pip_path = get_venv_pip(project_dir)

    # Upgrade pip
    run_command(
        [str(pip_path), "install", "--upgrade", "pip"],
        cwd=project_dir,
        check=False,
    )

    # Install dependencies
    run_command(
        [str(pip_path), "install", "-r", "requirements.txt"],
        cwd=project_dir,
        timeout=300,  # 5 minutes timeout
    )
    print("[OK] Dependencies installed")


def start_server(project_dir: Path) -> subprocess.Popen:
    """Start server"""
    print(f"\n[5/6] Starting server (http://{SERVER_HOST}:{SERVER_PORT})...")
    uvicorn_path = get_venv_uvicorn(project_dir)

    # Set environment variables for UTF-8
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"

    # Start uvicorn
    process = subprocess.Popen(
        [
            str(uvicorn_path),
            "main:app",
            "--host",
            SERVER_HOST,
            "--port",
            str(SERVER_PORT),
        ],
        cwd=project_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace",
        env=env,
    )

    return process


def wait_for_server(timeout: int = SERVER_STARTUP_TIMEOUT) -> bool:
    """Wait for server to start"""
    print(f"Waiting for server to start (max {timeout} seconds)...")
    url = f"http://{SERVER_HOST}:{SERVER_PORT}/docs"

    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            response = requests.get(url, timeout=2)
            if response.status_code == 200:
                elapsed = time.time() - start_time
                print(f"[OK] Server started! (took {elapsed:.1f}s)")
                return True
        except requests.exceptions.RequestException:
            pass
        time.sleep(SERVER_CHECK_INTERVAL)

    print(f"[FAIL] Server startup timeout ({timeout}s)")
    return False


def test_api_endpoints():
    """Test API endpoints"""
    print("\n[6/6] Testing API endpoints...")

    endpoints = [
        (f"http://{SERVER_HOST}:{SERVER_PORT}/docs", "Swagger UI"),
        (f"http://{SERVER_HOST}:{SERVER_PORT}/redoc", "ReDoc"),
        (f"http://{SERVER_HOST}:{SERVER_PORT}/openapi.json", "OpenAPI Schema"),
    ]

    success = True
    for url, name in endpoints:
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                print(f"  [OK] {name}: {url}")
            else:
                print(f"  [FAIL] {name}: {url} (status: {response.status_code})")
                success = False
        except requests.exceptions.RequestException as e:
            print(f"  [FAIL] {name}: {url} (error: {e})")
            success = False

    return success


def stop_server(process: subprocess.Popen):
    """Stop server"""
    print("\nStopping server...")
    if platform.system() == "Windows":
        process.terminate()
    else:
        process.send_signal(signal.SIGTERM)

    try:
        process.wait(timeout=5)
        print("[OK] Server stopped")
    except subprocess.TimeoutExpired:
        print("[WARN] Server not responding, force killing...")
        process.kill()
        process.wait()


def main():
    parser = argparse.ArgumentParser(description="FastAPI-Builder End-to-End Test")
    parser.add_argument("--name", default=DEFAULT_PROJECT_NAME, help="Project name")
    parser.add_argument(
        "--keep", action="store_true", help="Keep temp directory (for debugging)"
    )
    parser.add_argument(
        "--skip-install", action="store_true", help="Skip installing fastapi-builder"
    )
    args = parser.parse_args()

    root_dir = get_root_dir()
    project_name = args.name
    server_process = None
    success = False

    print("=" * 60)
    print("FastAPI-Builder End-to-End Test")
    print("=" * 60)
    print(f"Root directory: {root_dir}")
    print(f"Project name: {project_name}")
    print(f"Python: {sys.executable}")
    print(f"Platform: {platform.system()}")

    try:
        # 1. Install fastapi-builder
        if not args.skip_install:
            install_fastapi_builder(root_dir)

        # 2. Create temp directory
        temp_dir = create_temp_dir(root_dir)

        # 3. Create project
        project_dir = create_project(temp_dir, project_name)

        # 4. Create virtual environment
        create_venv(project_dir)

        # 5. Install dependencies
        install_dependencies(project_dir)

        # 6. Start server
        server_process = start_server(project_dir)

        # 7. Wait for server to start
        if wait_for_server():
            # 8. Test API
            if test_api_endpoints():
                success = True
                print("\n" + "=" * 60)
                print("ALL TESTS PASSED!")
                print("=" * 60)
            else:
                print("\n[FAIL] API tests failed")
        else:
            # Print server output for debugging
            print("\nServer output:")
            if server_process.stdout:
                for line in server_process.stdout:
                    print(line, end="")
                    if server_process.poll() is not None:
                        break

    except Exception as e:
        print(f"\n[FAIL] Test failed: {e}")
        import traceback

        traceback.print_exc()

    finally:
        # Stop server
        if server_process:
            stop_server(server_process)

        # Clean up temp directory
        if not args.keep:
            cleanup_temp_dir(root_dir)
        else:
            print(f"\nTemp directory kept: {root_dir / TEMP_DIR}")

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
