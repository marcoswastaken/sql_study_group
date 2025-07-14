#!/usr/bin/env python3
"""
Environment Verification Script for SQL Study Group
Run this script to verify that your environment is set up correctly.
"""

import os
import sys
from pathlib import Path


def print_status(message, status):
    """Print a status message with appropriate emoji"""
    emoji = "✅" if status else "❌"
    print(f"{emoji} {message}")


def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major == 3 and version.minor >= 8:
        print_status(f"Python {version.major}.{version.minor}.{version.micro}", True)
        return True
    else:
        print_status(
            f"Python {version.major}.{version.minor}.{version.micro} (requires 3.8+)",
            False,
        )
        return False


def check_packages():
    """Check if required packages are installed"""
    required_packages = [
        ("pandas", "1.5.0"),
        ("datasets", "2.0.0"),
        ("duckdb", "0.8.0"),
        ("jupyter", "1.0.0"),
        ("notebook", "6.0.0"),
    ]

    all_good = True
    for package, _min_version in required_packages:
        try:
            module = __import__(package)
            if hasattr(module, "__version__"):
                version = module.__version__
                print_status(f"{package} {version}", True)
            else:
                print_status(f"{package} (version unknown)", True)
        except ImportError:
            print_status(f"{package} not installed", False)
            all_good = False

    # Special check for ipython-sql
    try:
        import importlib.util

        if importlib.util.find_spec("sql"):
            print_status("ipython-sql installed", True)
        else:
            raise ImportError()
    except ImportError:
        print_status("ipython-sql not installed", False)
        all_good = False

    # Check for duckdb-engine (required for SQL magic)
    try:
        if importlib.util.find_spec("duckdb_engine"):
            print_status("duckdb-engine installed", True)
        else:
            raise ImportError()
    except ImportError:
        print_status("duckdb-engine not installed", False)
        all_good = False

    return all_good


def check_database():
    """Check if the database file exists and is accessible"""
    db_path = Path("datasets/data_jobs.db")
    if db_path.exists():
        try:
            import duckdb

            conn = duckdb.connect(str(db_path))
            result = conn.execute("SELECT COUNT(*) FROM jobs").fetchone()
            job_count = result[0]
            conn.close()
            print_status(f"Database connected: {job_count:,} jobs loaded", True)
            return True
        except Exception as e:
            print_status(f"Database error: {e}", False)
            return False
    else:
        print_status("Database file not found (will be created during process)", None)
        return None


def check_jupyter():
    """Check if Jupyter notebook is available"""
    try:
        import importlib.util

        if importlib.util.find_spec("notebook"):
            print_status("Jupyter notebook available", True)
            return True
        else:
            raise ImportError()
    except ImportError:
        print_status("Jupyter notebook not available", False)
        return False


def check_kernel():
    """Check if the sql-study-group kernel is registered"""
    try:
        import subprocess

        result = subprocess.run(
            ["jupyter", "kernelspec", "list"], capture_output=True, text=True
        )
        if "sql-study-group" in result.stdout:
            print_status("SQL Study Group kernel registered", True)
            return True
        else:
            print_status("SQL Study Group kernel not registered", False)
            return False
    except Exception as e:
        print_status(f"Kernel check failed: {e}", False)
        return False


def check_sql_magic():
    """Check if SQL magic can connect to DuckDB"""
    db_path = Path("data/data_jobs.db")
    if not db_path.exists():
        print_status("SQL magic test skipped (database not found)", None)
        return None

    try:
        import sqlalchemy
        from sqlalchemy import create_engine

        # Test the connection string that the notebook uses
        engine = create_engine(f"duckdb:///{db_path}")
        with engine.connect() as conn:
            result = conn.execute(sqlalchemy.text("SELECT 1")).fetchone()
            if result[0] == 1:
                print_status("SQL magic connection test passed", True)
                return True
            else:
                print_status("SQL magic connection test failed", False)
                return False
    except Exception as e:
        print_status(f"SQL magic connection failed: {e}", False)
        return False


def check_pyenv():
    """Check if pyenv environment is active"""
    virtual_env = os.environ.get("PYENV_VIRTUAL_ENV")
    if virtual_env and "sql-study-group" in virtual_env:
        print_status("pyenv virtual environment active", True)
        return True
    else:
        print_status("pyenv virtual environment not active (optional)", None)
        return None


def main():
    """Run all checks and provide summary"""
    print("🚀 SQL Study Group Environment Verification")
    print("=" * 50)

    checks = [
        ("Python Version", check_python_version()),
        ("Required Packages", check_packages()),
        ("Database", check_database()),
        ("SQL Magic Connection", check_sql_magic()),
        ("Jupyter", check_jupyter()),
        ("Kernel Registration", check_kernel()),
    ]

    # pyenv check is optional
    pyenv_status = check_pyenv()
    if pyenv_status is not None:
        checks.append(("pyenv Environment", pyenv_status))

    print("\n" + "=" * 50)

    # Summary
    failed = sum(1 for _, status in checks if status is False)

    if failed == 0:
        print("🎉 All checks passed! Your environment is ready for SQL practice.")
        print("\nNext steps:")
        print("1. Run: jupyter notebook notebooks/week_4_sql_practice.ipynb")
        print("2. Start practicing SQL queries!")
    else:
        print(f"⚠️  {failed} check(s) failed. Please fix the issues above.")
        print("\nTroubleshooting:")
        print("- Run: pip install -r requirements.txt")
        print("- Run: python setup_sql_environment.py")
        print(
            '- Run: python -m ipykernel install --user --name=sql-study-group --display-name="SQL Study Group"'
        )
        print("- Check the README.md for detailed setup instructions")


if __name__ == "__main__":
    main()
