#!/usr/bin/env python3
"""
Phase 1: Deterministic Table Creation Script

Loads table creation queries from table_creation_queries_[dataset].json
and executes them against the target database.

Usage: python create_tables_from_queries.py --dataset jobs
"""

import json
import sys
import os
import argparse
from pathlib import Path

# Add core directory to path for sql_helper
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'core'))
from sql_helper import SQLHelper

def load_table_queries(dataset_name):
    """Load table creation queries from JSON file."""
    queries_file = Path(__file__).parent / f'table_creation_queries_{dataset_name}.json'
    
    if not queries_file.exists():
        raise FileNotFoundError(f"Table queries file not found: {queries_file}")
    
    with open(queries_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def execute_table_creation(dataset_name, verbose=True):
    """Execute all table creation queries for the given dataset."""
    print(f"🔧 Creating tables for dataset: {dataset_name}")
    
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
    db_path = f'../../datasets/data_{dataset_name}.db'
    if not os.path.exists(db_path):
        print(f"❌ Database not found: {db_path}")
        return False
    
    helper = SQLHelper(db_path)
    
    # Execute queries
    successful_tables = []
    failed_tables = []
    
    for table_name, table_info in queries_data['tables'].items():
        if verbose:
            print(f"\n📝 Creating table: {table_name}")
            print(f"   Purpose: {table_info.get('educational_purpose', 'N/A')}")
            print(f"   Expected rows: {table_info.get('row_count_estimate', 'Unknown')}")
        
        query = table_info['query']
        
        try:
            # Execute the CREATE TABLE query
            result = helper.execute_query(query)
            
            if result['status'] == 'success':
                # Get actual row count
                count_result = helper.execute_query(f"SELECT COUNT(*) as count FROM {table_name}")
                if count_result['status'] == 'success':
                    actual_count = count_result['data'].iloc[0]['count']
                    if verbose:
                        print(f"   ✅ Success: {actual_count} rows created")
                    successful_tables.append((table_name, actual_count))
                else:
                    if verbose:
                        print(f"   ✅ Success: Table created (count unknown)")
                    successful_tables.append((table_name, 'unknown'))
            else:
                error_msg = result.get('error', 'Unknown error')
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
        print(f"\n✅ Successfully created tables:")
        for table_name, count in successful_tables:
            print(f"   • {table_name}: {count} rows")
    
    if failed_tables:
        print(f"\n❌ Failed to create tables:")
        for table_name, error in failed_tables:
            print(f"   • {table_name}: {error}")
    
    return len(failed_tables) == 0

def main():
    parser = argparse.ArgumentParser(description='Create tables from JSON query definitions')
    parser.add_argument('--dataset', required=True, help='Dataset name (e.g., jobs, movies)')
    parser.add_argument('--quiet', action='store_true', help='Suppress verbose output')
    
    args = parser.parse_args()
    
    success = execute_table_creation(args.dataset, verbose=not args.quiet)
    
    if success:
        print(f"\n🎉 All tables created successfully for {args.dataset}!")
        sys.exit(0)
    else:
        print(f"\n💥 Some tables failed to create for {args.dataset}")
        sys.exit(1)

if __name__ == "__main__":
    main() 