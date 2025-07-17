#!/usr/bin/env python3
"""
Generic Exercise Generation Script

Processes existing exercise JSON files to add metadata, validate structure,
and enhance with syllabus and schema information.

Usage:
    python generate_exercises.py --exercise-file exercises/week_5/week_5_key.json --dataset movies-dataset
"""

import argparse
import json
from datetime import datetime
from pathlib import Path


def load_syllabus_schema():
    """Load syllabus schema to get week-specific topics"""
    project_root = Path(__file__).parent.parent.parent
    syllabus_path = (
        project_root / "scripts" / "asset_generation" / "syllabus_schema.json"
    )
    with open(syllabus_path) as f:
        return json.load(f)


def load_data_schema(dataset):
    """Load data schema to understand table structure"""
    project_root = Path(__file__).parent.parent.parent
    schema_path = project_root / "schemas" / f"data_schema_{dataset}.json"
    with open(schema_path) as f:
        return json.load(f)


def get_week_info(syllabus, week_num):
    """Extract information for specific week"""
    for week in syllabus["weeks"]:
        if week["number"] == week_num:
            return week
    return None


def load_exercise_file(exercise_file_path):
    """Load existing exercise JSON file"""
    with open(exercise_file_path) as f:
        return json.load(f)


def enhance_exercise_metadata(exercise_key, week_info, schema_info, dataset):
    """Enhance exercise metadata with syllabus and schema information"""

    # Extract week number from metadata or week_info
    week_num = exercise_key.get("metadata", {}).get("week") or week_info.get("number")

    # Update metadata with enhanced information
    enhanced_metadata = {
        "title": f"Week {week_num} Practice - {dataset.replace('_', ' ').title()} Dataset",
        "description": exercise_key.get("metadata", {}).get(
            "description",
            f"{week_info.get('title', 'SQL Practice')} using {dataset} dataset",
        ),
        "week": week_num,
        "total_exercises": len(exercise_key.get("exercises", [])),
        "database": f"{dataset}.db",
        "focus_topics": week_info.get("core_concepts", []),
        "generated_date": datetime.now().isoformat(),
        "difficulty_levels": ["Easy", "Medium", "Hard"],
        "syllabus_topics": week_info.get("core_concepts", []),
        "learning_objectives": week_info.get("learning_objectives", []),
        "schema_tables": [table["name"] for table in schema_info.get("tables", [])],
        "total_records": schema_info.get("metadata", {}).get("total_records", 0),
    }

    # Preserve any existing metadata fields
    existing_metadata = exercise_key.get("metadata", {})
    for key, value in existing_metadata.items():
        if key not in enhanced_metadata and value:
            enhanced_metadata[key] = value

    exercise_key["metadata"] = enhanced_metadata
    return exercise_key


def validate_exercise_structure(exercise_key):
    """Validate that exercise follows expected structure"""

    required_fields = ["metadata", "exercises"]
    missing_fields = [field for field in required_fields if field not in exercise_key]

    if missing_fields:
        print(f"❌ Missing required fields: {missing_fields}")
        return False

    # Validate metadata
    metadata = exercise_key["metadata"]
    required_metadata = ["title", "week", "database", "total_exercises"]
    missing_metadata = [field for field in required_metadata if field not in metadata]

    if missing_metadata:
        print(f"❌ Missing required metadata fields: {missing_metadata}")
        return False

    # Validate exercises
    exercises = exercise_key["exercises"]
    if not exercises:
        print("❌ No exercises found")
        return False

    for i, exercise in enumerate(exercises):
        required_exercise_fields = [
            "id",
            "title",
            "statement",
            "solution",
            "topics",
            "difficulty",
        ]
        missing_exercise_fields = [
            field for field in required_exercise_fields if field not in exercise
        ]

        if missing_exercise_fields:
            print(
                f"❌ Exercise {i+1} missing required fields: {missing_exercise_fields}"
            )
            return False

    print("✅ Exercise structure validation passed")
    print(f"📊 Found {len(exercises)} exercises")
    return True


def analyze_topic_coverage(exercise_key, week_info):
    """Analyze how well exercises cover the week's topics"""

    week_topics = set(week_info.get("core_concepts", []))
    covered_topics = set()

    for exercise in exercise_key.get("exercises", []):
        for topic in exercise.get("topics", []):
            covered_topics.add(topic)

    # Find which week topics are covered (fuzzy matching)
    covered_week_topics = set()
    for week_topic in week_topics:
        for covered_topic in covered_topics:
            if (
                week_topic.lower() in covered_topic.lower()
                or covered_topic.lower() in week_topic.lower()
            ):
                covered_week_topics.add(week_topic)
                break

    missing_topics = week_topics - covered_week_topics

    print("\n📚 Topic Coverage Analysis:")
    print(
        f"✅ Week {week_info.get('number')} topics covered: {len(covered_week_topics)}/{len(week_topics)}"
    )
    if covered_week_topics:
        print(f"   Covered: {', '.join(sorted(covered_week_topics))}")
    if missing_topics:
        print(f"❌ Missing topics: {', '.join(sorted(missing_topics))}")

    return len(covered_week_topics) / len(week_topics) if week_topics else 0


def main():
    parser = argparse.ArgumentParser(
        description="Process and enhance SQL exercise files"
    )
    parser.add_argument(
        "--exercise-file", required=True, help="Path to exercise JSON file"
    )
    parser.add_argument(
        "--dataset", required=True, help="Dataset name (e.g., movies-dataset)"
    )
    parser.add_argument("--output", help="Output file path (optional)")

    args = parser.parse_args()

    # Load input files
    print(f"📁 Loading exercise file: {args.exercise_file}")
    exercise_key = load_exercise_file(args.exercise_file)

    print("📚 Loading syllabus schema...")
    syllabus = load_syllabus_schema()

    print(f"📊 Loading data schema for {args.dataset}...")
    schema_info = load_data_schema(args.dataset)

    # Get week information from exercise metadata
    week_num = exercise_key.get("metadata", {}).get("week")
    if not week_num:
        print("❌ No week number found in exercise metadata")
        return

    week_info = get_week_info(syllabus, week_num)
    if not week_info:
        print(f"❌ Week {week_num} not found in syllabus")
        return

    print(f"🎯 Processing Week {week_num}: {week_info['title']}")
    print(f"📋 Core concepts: {', '.join(week_info['core_concepts'])}")

    # Validate exercise structure
    if not validate_exercise_structure(exercise_key):
        print("❌ Exercise structure validation failed")
        return

    # Enhance metadata
    exercise_key = enhance_exercise_metadata(
        exercise_key, week_info, schema_info, args.dataset
    )

    # Analyze topic coverage
    coverage_pct = analyze_topic_coverage(exercise_key, week_info)

    # Output file
    if args.output:
        output_path = Path(args.output)
    else:
        input_path = Path(args.exercise_file)
        output_path = input_path.parent / f"{input_path.stem}_enhanced.json"

    # Write enhanced file
    with open(output_path, "w") as f:
        json.dump(exercise_key, f, indent=2)

    print("\n✅ Exercise processing completed!")
    print(f"📁 Enhanced file: {output_path}")
    print(f"📊 Topic coverage: {coverage_pct:.1%}")
    print(f"🎯 Total exercises: {len(exercise_key['exercises'])}")

    # Summary
    difficulties = {}
    all_topics = set()
    for exercise in exercise_key["exercises"]:
        diff = exercise.get("difficulty", "Unknown")
        difficulties[diff] = difficulties.get(diff, 0) + 1
        all_topics.update(exercise.get("topics", []))

    print(f"📈 Difficulty distribution: {dict(difficulties)}")
    print(f"🏷️  Unique topics covered: {len(all_topics)}")


if __name__ == "__main__":
    main()
