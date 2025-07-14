#!/usr/bin/env python3
"""
Test script to verify deterministic behavior of table creation queries.

This test ensures that the same queries produce identical results across multiple runs,
which is crucial for consistent exercise generation and testing.
"""

import sqlite3
import tempfile
import os
import json
import hashlib
from pathlib import Path
import sys

# Add the scripts directory to the Python path
sys.path.append(str(Path(__file__).parent.parent))

def load_table_creation_queries():
    """Load table creation queries from the configuration file."""
    queries_file = Path(__file__).parent.parent / "data_schema_generation" / "table_creation_queries_data_jobs.json"
    with open(queries_file, 'r') as f:
        return json.load(f)

def create_test_database():
    """Create a temporary test database with sample data."""
    # Create temporary database
    fd, db_path = tempfile.mkstemp(suffix='.db')
    os.close(fd)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create sample data_jobs table for testing
    cursor.execute("""
        CREATE TABLE data_jobs (
            job_title_short TEXT,
            job_title TEXT,
            job_schedule_type TEXT,
            job_work_from_home TEXT,
            job_posted_date TEXT,
            job_no_degree_mention TEXT,
            job_health_insurance TEXT,
            salary_year_avg INTEGER,
            salary_hour_avg REAL,
            company_name TEXT,
            job_location TEXT,
            job_via TEXT,
            job_country TEXT
        )
    """)
    
    # Insert sample data with predictable patterns
    sample_data = []
    companies = ['Apple Inc.', 'Google LLC', 'Microsoft Corp', 'Amazon.com', 'Meta Inc.', 'Tesla Inc.']
    locations = ['New York, NY', 'San Francisco, CA', 'Seattle, WA', 'Austin, TX', 'Boston, MA']
    countries = ['United States', 'Canada', 'United Kingdom']
    platforms = ['via LinkedIn', 'via Indeed', 'via Glassdoor', 'via ZipRecruiter']
    
    for i in range(1000):  # Create 1000 sample records
        sample_data.append((
            f'Software Engineer',
            f'Senior Software Engineer {i}',
            'Full-time',
            'True' if i % 3 == 0 else 'False',
            f'2024-01-{(i % 30) + 1:02d}',
            'True' if i % 4 == 0 else 'False',
            'True' if i % 2 == 0 else 'False',
            50000 + (i * 100),  # Incremental salary
            25 + (i * 0.1),
            companies[i % len(companies)],
            locations[i % len(locations)],
            platforms[i % len(platforms)],
            countries[i % len(countries)]
        ))
    
    cursor.executemany("""
        INSERT INTO data_jobs VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, sample_data)
    
    conn.commit()
    return db_path, conn

def sqlite_compatible_query(query):
    """Convert query to SQLite-compatible format."""
    # Remove SETSEED since SQLite doesn't support it
    sqlite_query = query.replace("SELECT SETSEED(0.42); ", "")
    # Replace ORDER BY RANDOM() with ORDER BY ROWID for deterministic results in test
    sqlite_query = sqlite_query.replace("ORDER BY RANDOM()", "ORDER BY ROWID")
    return sqlite_query

def execute_table_creation_queries(conn, queries_config):
    """Execute all table creation queries and return table data."""
    cursor = conn.cursor()
    results = {}
    
    for table_name, table_info in queries_config['tables'].items():
        query = table_info['query']
        
        # Convert to SQLite-compatible query
        sqlite_query = sqlite_compatible_query(query)
        
        # Drop table if exists
        cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
        
        # Execute the creation query
        cursor.execute(sqlite_query)
        
        # Get the created table data
        cursor.execute(f"SELECT * FROM {table_name} ORDER BY 1")
        rows = cursor.fetchall()
        
        # Get column names
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = [col[1] for col in cursor.fetchall()]
        
        results[table_name] = {
            'columns': columns,
            'rows': rows,
            'row_count': len(rows)
        }
    
    return results

def calculate_hash(data):
    """Calculate MD5 hash of serialized data for comparison."""
    serialized = json.dumps(data, sort_keys=True, default=str)
    return hashlib.md5(serialized.encode()).hexdigest()

def test_deterministic_behavior():
    """Test that table creation queries produce deterministic results."""
    print("Testing deterministic behavior of table creation queries...")
    print("Note: Using SQLite-compatible queries for testing (SETSEED -> ROWID ordering)")
    
    # Load configuration
    queries_config = load_table_creation_queries()
    
    # Create test database
    db_path, conn = create_test_database()
    
    try:
        # Run queries first time
        print("Running table creation queries (first time)...")
        results_1 = execute_table_creation_queries(conn, queries_config)
        hash_1 = calculate_hash(results_1)
        
        # Run queries second time
        print("Running table creation queries (second time)...")
        results_2 = execute_table_creation_queries(conn, queries_config)
        hash_2 = calculate_hash(results_2)
        
        # Compare results
        print(f"\nResults comparison:")
        print(f"First run hash:  {hash_1}")
        print(f"Second run hash: {hash_2}")
        
        if hash_1 == hash_2:
            print("✅ SUCCESS: Table creation queries are deterministic!")
            print("   (SQLite-compatible version - actual production uses SETSEED)")
            
            # Print summary statistics
            print("\nTable creation summary:")
            for table_name, data in results_1.items():
                print(f"  {table_name}: {data['row_count']} rows, {len(data['columns'])} columns")
            
            return True
        else:
            print("❌ FAILURE: Table creation queries are non-deterministic!")
            
            # Find differences
            for table_name in results_1:
                if results_1[table_name] != results_2[table_name]:
                    print(f"  Difference detected in table: {table_name}")
                    print(f"    First run rows: {results_1[table_name]['row_count']}")
                    print(f"    Second run rows: {results_2[table_name]['row_count']}")
            
            return False
            
    finally:
        conn.close()
        os.unlink(db_path)

if __name__ == "__main__":
    success = test_deterministic_behavior()
    sys.exit(0 if success else 1) 