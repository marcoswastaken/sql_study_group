#!/usr/bin/env python3
"""
SQL Study Group Setup Script

This script sets up the complete environment for practicing SQL with any week/dataset:
1. Creates or activates the virtual environment
2. Installs dependencies
3. Reads the chosen week's exercise file to determine the dataset
4. Downloads the dataset from HuggingFace
5. Creates the database tables using the defined table creation queries
6. Starts the Flask practice app

Usage:
    python setup.py [week_number]

Examples:
    python setup.py       # Uses Week 4 (default)
    python setup.py 5     # Uses Week 5
    SQL_WEEK=5 python setup.py  # Uses Week 5 via environment variable
"""

import json
import os
import socket
import subprocess
import sys
from pathlib import Path

# Add project root to path so we can import our modules
sys.path.insert(0, str(Path(__file__).parent))


def is_virtual_environment():
    """Check if we're running in a virtual environment."""
    return hasattr(sys, "real_prefix") or (
        hasattr(sys, "base_prefix") and sys.base_prefix != sys.prefix
    )


def find_available_port(start_port=5001, max_attempts=10):
    """Find an available port starting from start_port with clear messaging."""
    for port in range(start_port, start_port + max_attempts):
        try:
            # Create a socket and try to bind to the port
            # Don't use SO_REUSEADDR for port detection - we want accurate availability
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.bind(("localhost", port))
                return port
        except OSError:
            # Port is already in use, show message and try the next one
            if port == start_port:
                print(
                    f"🔄 Another process running on port {port}, trying another port..."
                )
            else:
                print(f"🔄 Port {port} also busy, trying port {port + 1}...")
            continue

    # If we couldn't find an available port, raise an exception
    raise RuntimeError(
        f"Could not find an available port in range {start_port}-{start_port + max_attempts - 1}"
    )


def is_port_available(port):
    """Check if a specific port is available."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind(("localhost", port))
            return True
    except OSError:
        return False


def setup_virtual_environment():
    """Create or activate the virtual environment and restart the script."""
    venv_dir = Path("sql-study-group-venv")

    if is_virtual_environment():
        print("✅ Running in virtual environment")
        return True

    print("🔧 Setting up virtual environment...")

    # Create virtual environment if it doesn't exist
    if not venv_dir.exists():
        print("📦 Creating new virtual environment...")
        try:
            subprocess.run(
                [sys.executable, "-m", "venv", str(venv_dir)],
                check=True,
                capture_output=True,
            )
            print("✅ Virtual environment created successfully")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to create virtual environment: {e}")
            return False
    else:
        print("✅ Virtual environment already exists")

    # Determine the python executable in the virtual environment
    if os.name == "nt":  # Windows
        venv_python = venv_dir / "Scripts" / "python.exe"
    else:  # Unix/Mac
        venv_python = venv_dir / "bin" / "python"

    if not venv_python.exists():
        print(f"❌ Virtual environment Python not found at {venv_python}")
        return False

    # Re-run the script with the virtual environment Python
    print("🔄 Restarting script in virtual environment...")
    try:
        subprocess.run([str(venv_python)] + sys.argv, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to restart script in virtual environment: {e}")
        return False


def get_week_config():
    """Get week configuration from command line args or environment variables."""
    force_recreate = True  # Default to True for setup script (fresh start)
    week = None

    # Parse command line arguments
    for arg in sys.argv[1:]:
        if arg == "--keep-tables":
            force_recreate = False  # Don't recreate tables if this flag is present
        elif arg == "--force":
            force_recreate = True  # Explicitly recreate tables
        elif arg.startswith("--"):
            continue  # Skip other options
        else:
            try:
                week = int(arg)
            except ValueError:
                print(f"Warning: Invalid week argument '{arg}', using default week 4")

    # If no week specified, check environment variable
    if week is None:
        week_env = os.environ.get("SQL_WEEK", "4")
        try:
            week = int(week_env)
        except ValueError:
            print(
                f"Warning: Invalid SQL_WEEK environment variable '{week_env}', using default week 4"
            )
            week = 4

    return week, force_recreate


def find_exercise_file(week):
    """Find the exercise file for the given week."""
    import glob
    import re

    # Look for versioned files first
    pattern = f"exercises/week_{week}/week_{week}_key_v*.json"
    files = glob.glob(pattern)

    if files:
        # Find the highest version
        def extract_version(filename):
            match = re.search(r"_v(\d+)\.json$", filename)
            return int(match.group(1)) if match else 0

        latest_file = max(files, key=extract_version)
        return latest_file

    # Fallback to non-versioned file
    fallback = f"exercises/week_{week}/week_{week}_key.json"
    if os.path.exists(fallback):
        return fallback

    raise FileNotFoundError(f"No exercise files found for week {week}")


def load_exercise_metadata(exercise_file):
    """Load exercise metadata to get dataset information."""
    with open(exercise_file) as f:
        data = json.load(f)

    metadata = data.get("metadata", {})
    database_file = metadata.get("database", "data_jobs.db")
    dataset_name = database_file.replace(".db", "")

    return {
        "dataset_name": dataset_name,
        "week": metadata.get("week", 4),
        "title": metadata.get("title", f'Week {metadata.get("week", 4)} Practice'),
        "database_file": database_file,
    }


def setup_environment(week, force_recreate=False):
    """Complete environment setup for the given week."""
    print(f"🚀 Setting up SQL Study Group environment for Week {week}")
    if force_recreate:
        print("🔄 Fresh setup mode: existing tables will be recreated for clean start")
    else:
        print(
            "📋 Preserve mode: existing tables will be kept (use --keep-tables to preserve)"
        )
    print(
        "💡 Tip: Use --keep-tables to preserve existing data, or --force to ensure fresh tables"
    )
    print("=" * 60)

    # Step 1: Find and load exercise file
    print(f"📋 Loading Week {week} exercise configuration...")
    try:
        exercise_file = find_exercise_file(week)
        metadata = load_exercise_metadata(exercise_file)
        print(f"✅ Found exercise file: {exercise_file}")
        print(f"📊 Dataset: {metadata['dataset_name']}")
        print(f"🎯 Title: {metadata['title']}")
    except FileNotFoundError as e:
        print(f"❌ {e}")
        print(f"💡 Available weeks: {list_available_weeks()}")
        return False
    except Exception as e:
        print(f"❌ Error loading exercise file: {e}")
        return False

    # Step 2: Install dependencies
    print("\n📦 Installing dependencies...")
    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
            check=True,
            capture_output=True,
        )
        print("✅ Dependencies installed successfully")
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        print("💡 Try: pip install -r requirements.txt")
        return False

    # Step 3: Setup dataset and database
    print(f"\n🗄️  Setting up {metadata['dataset_name']} database...")

    # First, ensure the base database exists with the raw dataset
    db_path = Path("datasets") / f"{metadata['dataset_name']}.db"

    # Create datasets directory if it doesn't exist
    Path("datasets").mkdir(exist_ok=True)

    if not db_path.exists():
        print("📥 Database not found, creating from HuggingFace dataset...")
        try:
            from scripts.core.explore_dataset import DatasetExplorer

            # Map dataset name to HuggingFace identifier
            dataset_map = {
                "data_jobs": "lukebarousse/data_jobs",
                "data_movies_dataset": "Pablinho/movies-dataset",
            }

            hf_dataset = dataset_map.get(
                metadata["dataset_name"], metadata["dataset_name"]
            )
            print(f"📥 Downloading dataset: {hf_dataset}")

            explorer = DatasetExplorer(hf_dataset)
            if not explorer.load_dataset():
                print("❌ Failed to load dataset")
                return False

            if not explorer.create_database(str(db_path)):
                print("❌ Failed to create database")
                return False

            print("✅ Base database created successfully")

        except Exception as e:
            print(f"❌ Error creating base database: {e}")
            return False
    else:
        print(f"✅ Base database exists: {db_path}")

    # Check if we have table creation queries for this dataset
    table_queries_file = f"scripts/data_schema_generation/table_creation_queries_{metadata['dataset_name']}.json"
    if os.path.exists(table_queries_file):
        print(f"✅ Found table creation queries: {table_queries_file}")

        # Use the existing table creation process
        try:
            from scripts.data_schema_generation.create_tables_from_queries import (
                execute_table_creation,
            )

            success = execute_table_creation(
                metadata["dataset_name"], verbose=True, force_recreate=force_recreate
            )
            if success:
                print("✅ Database tables created successfully")
            else:
                print("❌ Some tables failed to create")
                return False
        except Exception as e:
            print(f"❌ Error creating tables: {e}")
            return False
    else:
        print(f"⚠️  No table creation queries found for {metadata['dataset_name']}")
        print("💡 Using fallback setup for data_jobs dataset...")

        # Fallback to the original setup for data_jobs
        if metadata["dataset_name"] == "data_jobs":
            try:
                from scripts.utilities.setup_sql_environment import (
                    setup_sql_environment,
                )

                setup_sql_environment()
                print("✅ Database setup completed using fallback method")
            except Exception as e:
                print(f"❌ Error setting up database: {e}")
                return False
        else:
            print(
                f"❌ Cannot setup database for {metadata['dataset_name']} without table creation queries"
            )
            return False

    # Step 4: Verify environment
    print("\n🔍 Verifying environment...")
    try:
        import contextlib

        # Capture the output to check if verification passed
        import io

        from scripts.utilities.verify_environment import main as verify_env

        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            verify_env()

        output = f.getvalue()
        if "All checks passed" in output:
            print("✅ Environment verification passed")
        else:
            print("⚠️  Environment verification had warnings (check output above)")
    except Exception as e:
        print(f"⚠️  Environment verification failed: {e}")
        print("💡 You can still try to run the app")

    # Step 5: Find available port and start the app
    print("\n🎉 Setup complete! Starting the SQL Practice App...")
    print("=" * 60)
    print(f"🎯 Week {week}: {metadata['title']}")
    print(f"📊 Dataset: {metadata['dataset_name']}")

    # Find an available port
    try:
        port = find_available_port(start_port=5001, max_attempts=10)
        if port != 5001:
            print(f"✅ Found available port {port}")
        print(f"🚀 Starting app at http://localhost:{port}")
        print("💡 Press Ctrl+C to stop the server")
    except RuntimeError as e:
        print(f"❌ {e}")
        print("💡 Please check for running services and try again")
        return False

    print("=" * 60)

    # Start the Flask app with the correct week and port
    try:
        os.environ["SQL_WEEK"] = str(week)
        os.environ["SQL_PORT"] = str(port)
        subprocess.run([sys.executable, "app.py"], check=True)
    except KeyboardInterrupt:
        print("\n👋 App stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ App failed to start: {e}")
        print(f"💡 Try running: SQL_PORT={port} python app.py")
        return False

    return True


def list_available_weeks():
    """List all available weeks with exercise files."""
    weeks = []
    exercises_dir = Path("exercises")

    if exercises_dir.exists():
        for week_dir in exercises_dir.iterdir():
            if week_dir.is_dir() and week_dir.name.startswith("week_"):
                try:
                    week_num = int(week_dir.name.split("_")[1])
                    weeks.append(week_num)
                except ValueError:
                    continue

    return sorted(weeks)


def main():
    """Main setup function."""
    # First, handle help requests without setting up virtual environment
    if len(sys.argv) > 1 and sys.argv[1] in ["-h", "--help", "help"]:
        print(__doc__)
        print("Environment Variables:")
        print("  SQL_WEEK=N    Set week number (default: 4)")
        print("\nOptions:")
        print("  --force       Recreate database tables if they already exist")
        print(
            "\nThis script will automatically detect the dataset from exercise metadata."
        )
        return

    # Setup virtual environment first (this may restart the script)
    if not setup_virtual_environment():
        print("❌ Failed to setup virtual environment")
        sys.exit(1)

    # If we're not in a virtual environment, the script was restarted
    # so we don't need to continue
    if not is_virtual_environment():
        return

    # Now proceed with the actual setup
    week, force_recreate = get_week_config()
    if week is None:  # Help was requested (shouldn't happen here)
        return

    success = setup_environment(week, force_recreate)
    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main()
