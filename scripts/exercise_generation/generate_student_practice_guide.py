#!/usr/bin/env python3
"""
Generate Student Practice Guide

Creates a markdown file with data dictionaries and problem statements for offline practice.
Students can work on SQL queries without database access, then test them later.

Usage: python generate_student_practice_guide.py [week_number]
"""

import argparse
import json
import sys
from pathlib import Path


def load_exercise_key(week):
    """Load exercise key for the specified week."""
    # Look for the latest version of the exercise key
    exercises_dir = Path(__file__).parent.parent.parent / "exercises" / f"week_{week}"

    if not exercises_dir.exists():
        raise FileNotFoundError(f"Exercises directory not found: {exercises_dir}")

    # Find the latest version file
    key_files = list(exercises_dir.glob(f"week_{week}_key*.json"))
    if not key_files:
        raise FileNotFoundError(f"No exercise key files found for week {week}")

    # Sort by version (assumes naming like week_4_key_v1.json, week_4_key_v2.json, etc.)
    key_files.sort(key=lambda x: x.name)
    latest_file = key_files[-1]

    print(f"📋 Loading exercise key: {latest_file}")

    with open(latest_file, encoding="utf-8") as f:
        return json.load(f)


def load_data_schema(dataset_name):
    """Load data schema for the specified dataset."""
    schema_path = (
        Path(__file__).parent.parent.parent
        / "schemas"
        / f"data_schema_{dataset_name}.json"
    )

    if not schema_path.exists():
        raise FileNotFoundError(f"Data schema not found: {schema_path}")

    print(f"📊 Loading data schema: {schema_path}")

    with open(schema_path, encoding="utf-8") as f:
        return json.load(f)


def extract_dataset_name(exercise_key):
    """Extract dataset name from exercise key metadata."""
    metadata = exercise_key.get("metadata", {})

    # Try to get dataset name from database field
    database = metadata.get("database", "")
    if database.endswith(".db"):
        dataset_name = database[:-3]  # Remove .db extension
        if dataset_name.startswith("data_"):
            return dataset_name[5:]  # Remove data_ prefix
        return dataset_name

    # Fallback to direct dataset field if available
    return metadata.get("dataset", "jobs")


def generate_data_dictionary_markdown(schema_data, allowed_tables=None):
    """Generate markdown for data dictionary section.

    Args:
        schema_data: Schema data containing table information
        allowed_tables: List of table names to include (from exercise metadata schema_tables field)
    """
    markdown = []

    markdown.append("## 📚 Data Dictionary")
    markdown.append("")

    # Add table information (filter based on allowed_tables from exercise metadata)
    tables = schema_data.get("tables", [])

    for table in tables:
        table_name = table.get("name", "Unknown")
        row_count = table.get("row_count", 0)

        # Filter tables based on allowed_tables list from exercise metadata
        # If allowed_tables is provided, only include tables in that list
        # This prevents students from seeing raw dataset tables
        if allowed_tables is not None and table_name not in allowed_tables:
            continue

        markdown.append(f"### {table_name}")
        markdown.append(f"**Row Count:** {row_count:,}")
        markdown.append("")

        # Add columns table
        columns = table.get("columns", [])
        if columns:
            markdown.append("| Column | Type | Nullable | Key | Description |")
            markdown.append("|--------|------|----------|-----|-------------|")

            for col in columns:
                col_name = col.get("name", "")
                col_type = col.get("type", "")
                nullable = "Yes" if col.get("nullable", True) else "No"

                # Determine key type
                key_info = ""
                if col.get("primary_key", False):
                    key_info = "PK"
                elif col.get("foreign_key", ""):
                    key_info = "FK"

                description = col.get("description", "")

                markdown.append(
                    f"| {col_name} | {col_type} | {nullable} | {key_info} | {description} |"
                )

            markdown.append("")

    return "\n".join(markdown)


def generate_exercises_markdown(exercise_key):
    """Generate markdown for exercises section."""
    markdown = []

    markdown.append("## 🎯 Practice Exercises")
    markdown.append("")

    # Add exercises
    exercises = exercise_key.get("exercises", [])

    for exercise in exercises:
        exercise_id = exercise.get("id", "Unknown")
        title = exercise.get("title", "Unknown")
        statement = exercise.get("statement", "No statement available")

        markdown.append(f"### Exercise {exercise_id}: {title}")
        markdown.append("")

        markdown.append("**Problem Statement:**")
        markdown.append(statement)
        markdown.append("")
        markdown.append("---")
        markdown.append("")

    return "\n".join(markdown)


def generate_practice_guide(week):
    """Generate the complete practice guide for the specified week."""
    try:
        # Load exercise key
        exercise_key = load_exercise_key(week)

        # Extract dataset name
        dataset_name = extract_dataset_name(exercise_key)
        print(f"📊 Detected dataset: {dataset_name}")

        # Load data schema
        schema_data = load_data_schema(f"data_{dataset_name}")

        # Extract allowed tables from exercise metadata (schema_tables field)
        # This ensures offline practice files only show the same tables as the web app
        allowed_tables = exercise_key.get("metadata", {}).get("schema_tables", None)
        if allowed_tables:
            print(
                f"📋 Filtering to {len(allowed_tables)} allowed tables: {allowed_tables}"
            )
        else:
            print(
                "⚠️  No schema_tables field found in exercise metadata - showing all tables"
            )

        # Generate markdown content
        markdown_content = []

        # Header
        title = f"Week {week} Practice"
        markdown_content.append(f"# {title}")
        markdown_content.append("")
        markdown_content.append(
            "The data cards for a collection of tables is provided. For each exercise, come up with a SQL query that addresses the problem statement."
        )
        markdown_content.append("")

        # Data Dictionary (filtered by allowed_tables from exercise metadata)
        data_dict_md = generate_data_dictionary_markdown(schema_data, allowed_tables)
        markdown_content.append(data_dict_md)

        markdown_content.append("---")
        markdown_content.append("")

        # Exercises
        exercises_md = generate_exercises_markdown(exercise_key)
        markdown_content.append(exercises_md)

        return "\n".join(markdown_content)

    except Exception as e:
        print(f"❌ Error generating practice guide: {e}")
        return None


def main():
    """Main function to parse arguments and generate practice guide."""
    parser = argparse.ArgumentParser(
        description="Generate student practice guide with data dictionary and problem statements"
    )
    parser.add_argument(
        "week", nargs="?", type=int, default=4, help="Week number (default: 4)"
    )
    parser.add_argument(
        "--output",
        "-o",
        help="Output file path (default: practice/week_X_offline_practice.md)",
    )

    args = parser.parse_args()

    print(f"🔧 Generating practice guide for Week {args.week}")
    print("=" * 60)

    # Generate practice guide
    markdown_content = generate_practice_guide(args.week)

    if markdown_content is None:
        print("❌ Failed to generate practice guide")
        sys.exit(1)

    # Determine output path
    if args.output:
        output_path = Path(args.output)
    else:
        # Default to practice directory
        output_path = (
            Path(__file__).parent.parent.parent
            / "practice"
            / f"week_{args.week}_offline_practice.md"
        )

    # Create output directory if it doesn't exist
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Write the file
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(markdown_content)

    print("✅ Practice guide generated successfully!")
    print(f"📁 Output: {output_path}")
    print(f"📊 File size: {output_path.stat().st_size / 1024:.1f} KB")

    # Print summary
    exercise_key = load_exercise_key(args.week)
    exercise_count = len(exercise_key.get("exercises", []))
    dataset_name = extract_dataset_name(exercise_key)

    print("📋 Summary:")
    print(f"  • Week: {args.week}")
    print(f"  • Dataset: {dataset_name}")
    print(f"  • Exercises: {exercise_count}")
    print("  • Format: Markdown with data dictionary and problem statements")


if __name__ == "__main__":
    main()
