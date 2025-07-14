#!/usr/bin/env python3
"""
SQL Study Group Setup Script

This script sets up the complete environment for practicing SQL with any week/dataset:
1. Reads the chosen week's exercise file to determine the dataset
2. Downloads the dataset from HuggingFace
3. Creates the database tables using the defined table creation queries
4. Starts the Flask practice app

Usage:
    python setup.py [week_number]

Examples:
    python setup.py       # Uses Week 4 (default)
    python setup.py 5     # Uses Week 5
    SQL_WEEK=5 python setup.py  # Uses Week 5 via environment variable
"""

import json
import os
import subprocess
import sys
from pathlib import Path

# Add project root to path so we can import our modules
sys.path.insert(0, str(Path(__file__).parent))


def get_week_config():
    """Get week configuration from command line args or environment variables."""
    # Check for help request
    if len(sys.argv) > 1 and sys.argv[1] in ["-h", "--help", "help"]:
        print(__doc__)
        print("Environment Variables:")
        print("  SQL_WEEK=N    Set week number (default: 4)")
        print(
            "\nThis script will automatically detect the dataset from exercise metadata."
        )
        return None

    # Check command line arguments
    if len(sys.argv) > 1:
        try:
            return int(sys.argv[1])
        except ValueError:
            print(
                f"Warning: Invalid week argument '{sys.argv[1]}', using default week 4"
            )

    # Check environment variable
    week = os.environ.get("SQL_WEEK", "4")
    try:
        return int(week)
    except ValueError:
        print(
            f"Warning: Invalid SQL_WEEK environment variable '{week}', using default week 4"
        )
        return 4


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


def setup_environment(week):
    """Complete environment setup for the given week."""
    print(f"🚀 Setting up SQL Study Group environment for Week {week}")
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

    # Check if we have table creation queries for this dataset
    table_queries_file = f"scripts/data_schema_generation/table_creation_queries_{metadata['dataset_name']}.json"
    if os.path.exists(table_queries_file):
        print(f"✅ Found table creation queries: {table_queries_file}")

        # Use the existing table creation process
        try:
            from scripts.data_schema_generation.create_tables_from_queries import (
                execute_table_creation,
            )

            success = execute_table_creation(metadata["dataset_name"], verbose=True)
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

    # Step 5: Start the app
    print("\n🎉 Setup complete! Starting the SQL Practice App...")
    print("=" * 60)
    print(f"🎯 Week {week}: {metadata['title']}")
    print(f"📊 Dataset: {metadata['dataset_name']}")
    print("🚀 Starting app at http://localhost:5000")
    print("💡 Press Ctrl+C to stop the server")
    print("=" * 60)

    # Start the Flask app with the correct week
    try:
        os.environ["SQL_WEEK"] = str(week)
        subprocess.run([sys.executable, "app.py"], check=True)
    except KeyboardInterrupt:
        print("\n👋 App stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ App failed to start: {e}")
        print("💡 Try running: python app.py")
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
    week = get_week_config()
    if week is None:  # Help was requested
        return

    success = setup_environment(week)
    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main()
