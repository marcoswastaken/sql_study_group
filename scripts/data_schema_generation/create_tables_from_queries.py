#!/usr/bin/env python3
"""
Phase 1: Deterministic Table Creation Script

Loads table creation queries from table_creation_queries_[dataset].json
and executes them against the target database.

Usage: python create_tables_from_queries.py --dataset jobs
"""

import argparse
import json
import sys
from pathlib import Path

from scripts.core.sql_helper import SQLHelper


def load_table_queries(dataset_name):
    """Load table creation queries from JSON file."""
    queries_file = Path(__file__).parent / f"table_creation_queries_{dataset_name}.json"

    if not queries_file.exists():
        raise FileNotFoundError(f"Table queries file not found: {queries_file}")

    with open(queries_file, encoding="utf-8") as f:
        return json.load(f)


def execute_table_creation(dataset_name, verbose=True, force_recreate=False):
    """Execute all table creation queries for the given dataset."""
    print(f"🔧 Creating tables for dataset: {dataset_name}")
    if force_recreate:
        print("⚠️  Force recreate mode: existing tables will be dropped")

    # Load queries
    try:
        queries_data = load_table_queries(dataset_name)
        if verbose:
            print(f"📋 Loaded queries for {len(queries_data['tables'])} tables")
    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        return False
    except json.JSONDecodeError as e:
        print(f"❌ Error parsing JSON: {e}")
        return False

    # Connect to database
    # Handle dataset naming: if dataset_name contains '/', extract just the name part
    # If it doesn't start with 'data_', prefix it
    if "/" in dataset_name:
        # Extract name from HuggingFace format (e.g., "lukebarousse/data_jobs" -> "data_jobs")
        db_name = dataset_name.split("/")[-1]
    else:
        db_name = dataset_name

    # Convert dashes to underscores for consistency (e.g., "movies-dataset" -> "movies_dataset")
    db_name = db_name.replace("-", "_")

    # Ensure db_name starts with 'data_' if it doesn't already
    if not db_name.startswith("data_"):
        db_name = f"data_{db_name}"

    # Use absolute path to ensure correct database location
    # This script can be called from various directories
    from pathlib import Path

    project_root = Path(__file__).parent.parent.parent
    db_path = project_root / "datasets" / f"{db_name}.db"

    if not db_path.exists():
        print(f"❌ Database not found: {db_path}")
        return False

    helper = SQLHelper(str(db_path))

    # Check which tables already exist
    existing_tables = set()
    try:
        tables_result = helper.execute_query(
            "SELECT name FROM sqlite_master WHERE type='table'"
        )
        if tables_result["status"] == "success" and tables_result["data"] is not None:
            existing_tables = set(tables_result["data"]["name"].tolist())
    except Exception as e:
        if verbose:
            print(f"   ⚠️  Could not check existing tables: {str(e)}")

    # Handle existing tables based on force_recreate flag
    if force_recreate:
        print("🗑️  Dropping existing tables...")
        for table_name in queries_data["tables"].keys():
            if table_name in existing_tables:
                try:
                    drop_result = helper.execute_query(
                        f"DROP TABLE IF EXISTS {table_name}"
                    )
                    if drop_result["status"] == "success":
                        if verbose:
                            print(f"   ✅ Dropped table: {table_name}")
                    else:
                        if verbose:
                            print(
                                f"   ⚠️  Could not drop table {table_name}: {drop_result.get('error', 'Unknown error')}"
                            )
                except Exception as e:
                    if verbose:
                        print(f"   ⚠️  Error dropping table {table_name}: {str(e)}")
    else:
        # In preserve mode, skip tables that already exist
        existing_required_tables = [
            t for t in queries_data["tables"].keys() if t in existing_tables
        ]
        if existing_required_tables:
            if verbose:
                print(
                    f"📋 Skipping existing tables: {', '.join(existing_required_tables)}"
                )

    # Execute queries
    successful_tables = []
    failed_tables = []

    for table_name, table_info in queries_data["tables"].items():
        # Skip table creation if it already exists and we're not force recreating
        if not force_recreate and table_name in existing_tables:
            # Get current row count
            try:
                count_result = helper.execute_query(
                    f"SELECT COUNT(*) as count FROM {table_name}"
                )
                if count_result["status"] == "success":
                    actual_count = count_result["data"].iloc[0]["count"]
                    if verbose:
                        print(f"\n📝 Table {table_name} already exists")
                        print(f"   ✅ Preserved: {actual_count} rows exist")
                    successful_tables.append((table_name, actual_count))
                else:
                    if verbose:
                        print(f"\n📝 Table {table_name} already exists")
                        print("   ✅ Preserved: Table exists (count unknown)")
                    successful_tables.append((table_name, "preserved"))
            except Exception:
                if verbose:
                    print(f"\n📝 Table {table_name} already exists")
                    print("   ✅ Preserved: Table exists")
                successful_tables.append((table_name, "preserved"))
            continue
        if verbose:
            print(f"\n📝 Creating table: {table_name}")
            print(f"   Purpose: {table_info.get('educational_purpose', 'N/A')}")
            print(
                f"   Expected rows: {table_info.get('row_count_estimate', 'Unknown')}"
            )

        query = table_info["query"]

        try:
            # Execute the CREATE TABLE query
            result = helper.execute_query(query)

            if result["status"] == "success":
                # Get actual row count
                count_result = helper.execute_query(
                    f"SELECT COUNT(*) as count FROM {table_name}"
                )
                if count_result["status"] == "success":
                    actual_count = count_result["data"].iloc[0]["count"]
                    if verbose:
                        print(f"   ✅ Success: {actual_count} rows created")
                    successful_tables.append((table_name, actual_count))
                else:
                    if verbose:
                        print("   ✅ Success: Table created (count unknown)")
                    successful_tables.append((table_name, "unknown"))
            else:
                error_msg = result.get("error", "Unknown error")
                if verbose:
                    print(f"   ❌ Failed: {error_msg}")
                failed_tables.append((table_name, error_msg))

        except Exception as e:
            if verbose:
                print(f"   ❌ Exception: {str(e)}")
            failed_tables.append((table_name, str(e)))

    # Close database connection
    helper.close()

    # Print summary
    print(f"\n📊 Summary for {dataset_name}:")
    print(f"   ✅ Successful: {len(successful_tables)} tables")
    print(f"   ❌ Failed: {len(failed_tables)} tables")

    if successful_tables:
        print("\n✅ Successfully created tables:")
        for table_name, count in successful_tables:
            print(f"   • {table_name}: {count} rows")

    if failed_tables:
        print("\n❌ Failed to create tables:")
        for table_name, error in failed_tables:
            print(f"   • {table_name}: {error}")

    return len(failed_tables) == 0


def main():
    parser = argparse.ArgumentParser(
        description="Create tables from JSON query definitions"
    )
    parser.add_argument(
        "--dataset", required=True, help="Dataset name (e.g., jobs, movies)"
    )
    parser.add_argument("--quiet", action="store_true", help="Suppress verbose output")
    parser.add_argument(
        "--force-recreate",
        action="store_true",
        help="Drop existing tables before creating new ones",
    )

    args = parser.parse_args()

    success = execute_table_creation(
        args.dataset, verbose=not args.quiet, force_recreate=args.force_recreate
    )

    if success:
        print(f"\n🎉 All tables created successfully for {args.dataset}!")
        sys.exit(0)
    else:
        print(f"\n💥 Some tables failed to create for {args.dataset}")
        sys.exit(1)


if __name__ == "__main__":
    main()
