#!/usr/bin/env python3
"""
Solution Testing Script

Tests all SQL solutions in an exercise key and captures:
- Execution time
- Row count
- Sample results
- Error handling

Usage:
    python test_solutions.py --exercise-key ../../exercises/week_4_key.json --dataset data_jobs
"""

import json
import argparse
import time
from pathlib import Path
import sys
import os
import pandas as pd

# Add the core directory to path to import sql_helper
sys.path.append(str(Path(__file__).parent.parent / "core"))
from sql_helper import SQLHelper

def load_exercise_key(file_path):
    """Load the exercise key JSON file"""
    with open(file_path, 'r') as f:
        return json.load(f)

def test_single_solution(db_manager, exercise):
    """Test a single SQL solution and return results"""
    result = {
        "working": False,
        "execution_time": None,
        "row_count": None,
        "columns": None,
        "sample_results": None,
        "error": None
    }
    
    try:
        # Execute the solution using SQLHelper
        sql_result = db_manager.execute_query(exercise["solution"])
        
        if sql_result["status"] == "error":
            result["error"] = sql_result["error"]
            print(f"❌ Exercise {exercise['id']}: {sql_result['error']}")
            return result
        
        # Extract results from SQLHelper response
        result["working"] = True
        result["execution_time"] = sql_result["execution_time"]
        result["row_count"] = sql_result["row_count"]
        result["columns"] = sql_result["columns"]
        
        # Get sample results (first 3 rows)
        sample_results = []
        if sql_result["data"] is not None and not sql_result["data"].empty:
            for _, row in sql_result["data"].head(3).iterrows():
                sample_dict = {}
                for col in sql_result["columns"]:
                    value = row[col]
                    # Convert values to strings for JSON serialization
                    if pd.isna(value):
                        sample_dict[col] = "None"
                    elif isinstance(value, (int, float)):
                        sample_dict[col] = str(value)
                    else:
                        sample_dict[col] = str(value)
                sample_results.append(sample_dict)
        
        result["sample_results"] = sample_results
        
        print(f"✅ Exercise {exercise['id']}: {result['row_count']} rows in {result['execution_time']}s")
        
    except Exception as e:
        result["error"] = str(e)
        print(f"❌ Exercise {exercise['id']}: {str(e)}")
    
    return result

def test_all_solutions(exercise_key, dataset):
    """Test all solutions in the exercise key"""
    print(f"🧪 Testing solutions for: {exercise_key['metadata']['title']}")
    print(f"📊 Dataset: {dataset}")
    print(f"🔢 Total exercises: {len(exercise_key['exercises'])}")
    print()
    
    # Initialize database manager
    db_path = Path(f"../../datasets/{dataset}.db")
    if not db_path.exists():
        print(f"❌ Database not found: {db_path}")
        return None
    
    db_manager = SQLHelper(str(db_path))
    
    # Test each exercise
    working_count = 0
    total_time = 0
    
    for exercise in exercise_key["exercises"]:
        print(f"Testing Exercise {exercise['id']}: {exercise['title']}")
        
        # Test the solution
        result = test_single_solution(db_manager, exercise)
        
        # Update exercise with results
        exercise["result"] = result
        
        if result["working"]:
            working_count += 1
            total_time += result["execution_time"]
    
    # Close database connection
    db_manager.close()
    
    # Update metadata with test results
    exercise_key["metadata"]["test_results"] = {
        "total_exercises": len(exercise_key["exercises"]),
        "working_exercises": working_count,
        "failed_exercises": len(exercise_key["exercises"]) - working_count,
        "success_rate": round(working_count / len(exercise_key["exercises"]) * 100, 1),
        "total_execution_time": round(total_time, 3),
        "average_execution_time": round(total_time / working_count, 3) if working_count > 0 else 0,
        "test_date": time.strftime("%Y-%m-%d %H:%M:%S")
    }
    
    print("\n📊 Test Results Summary:")
    print(f"✅ Working: {working_count}/{len(exercise_key['exercises'])}")
    print(f"❌ Failed: {len(exercise_key['exercises']) - working_count}")
    print(f"📈 Success rate: {exercise_key['metadata']['test_results']['success_rate']}%")
    print(f"⏱️  Total execution time: {exercise_key['metadata']['test_results']['total_execution_time']}s")
    print(f"⏱️  Average execution time: {exercise_key['metadata']['test_results']['average_execution_time']}s")
    
    return exercise_key

def save_updated_exercise_key(exercise_key, output_path):
    """Save the updated exercise key with test results"""
    with open(output_path, 'w') as f:
        json.dump(exercise_key, f, indent=2)
    print(f"💾 Updated exercise key saved to: {output_path}")

def validate_database_tables(db_manager, expected_tables):
    """Validate that expected tables exist in the database"""
    print("🔍 Validating database tables...")
    
    # Get list of tables using SQLHelper
    result = db_manager.execute_query("SELECT name FROM sqlite_master WHERE type='table';")
    
    if result["status"] == "error":
        print(f"❌ Error getting table list: {result['error']}")
        return False
    
    existing_tables = result["data"]["name"].tolist() if result["data"] is not None else []
    
    missing_tables = []
    for table in expected_tables:
        if table not in existing_tables:
            missing_tables.append(table)
    
    if missing_tables:
        print(f"❌ Missing tables: {missing_tables}")
        return False
    
    print(f"✅ All expected tables found: {expected_tables}")
    return True

def main():
    parser = argparse.ArgumentParser(description='Test SQL solutions in exercise key')
    parser.add_argument('--exercise-key', type=str, required=True, help='Path to exercise key JSON file')
    parser.add_argument('--dataset', type=str, required=True, help='Dataset name (e.g., data_jobs)')
    parser.add_argument('--output', type=str, help='Output file path (optional, defaults to input file)')
    
    args = parser.parse_args()
    
    # Load exercise key
    exercise_key_path = Path(args.exercise_key)
    if not exercise_key_path.exists():
        print(f"❌ Exercise key not found: {exercise_key_path}")
        return
    
    exercise_key = load_exercise_key(exercise_key_path)
    
    # Validate database exists
    db_path = Path(f"../../datasets/{args.dataset}.db")
    if not db_path.exists():
        print(f"❌ Database not found: {db_path}")
        return
    
    # Expected tables for data_jobs dataset
    expected_tables = ["companies", "data_jobs", "job_platforms", "job_postings", "locations", "salary_ranges"]
    
    # Validate database tables
    db_manager = SQLHelper(str(db_path))
    if not validate_database_tables(db_manager, expected_tables):
        print("❌ Database validation failed")
        db_manager.close()
        return
    db_manager.close()
    
    # Test all solutions
    updated_exercise_key = test_all_solutions(exercise_key, args.dataset)
    
    if updated_exercise_key is None:
        print("❌ Solution testing failed")
        return
    
    # Save updated exercise key
    output_path = Path(args.output) if args.output else exercise_key_path
    save_updated_exercise_key(updated_exercise_key, output_path)
    
    print(f"\n🎉 Solution testing completed successfully!")

if __name__ == "__main__":
    main() 