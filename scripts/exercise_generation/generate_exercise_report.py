#!/usr/bin/env python3
"""
Exercise Report Generator

Tests all exercise solutions and generates a comprehensive markdown report with:
1. Exercise statements
2. SQL solutions
3. Top 20 results in markdown tables

Usage:
    python generate_exercise_report.py --exercise-key ../../exercises/week_4_key.json --dataset data_jobs --output week_4_report.md
"""

import json
import argparse
import time
from pathlib import Path
import sys
import pandas as pd

# Add the core directory to path to import sql_helper
sys.path.append(str(Path(__file__).parent.parent / "core"))
from sql_helper import SQLHelper

def load_exercise_key(file_path):
    """Load the exercise key JSON file"""
    with open(file_path, 'r') as f:
        return json.load(f)

def execute_solution(db_manager, solution, limit=20):
    """Execute a SQL solution and return results with specified limit"""
    # Modify the solution to include LIMIT if not already present
    solution_lines = solution.strip().split('\n')
    last_line = solution_lines[-1].strip()
    
    # Check if LIMIT is already present
    if 'LIMIT' not in last_line.upper():
        # Remove any existing semicolon and add our limit
        if last_line.endswith(';'):
            solution_lines[-1] = last_line[:-1]
        solution_lines.append(f'LIMIT {limit};')
    else:
        # Replace existing limit with our limit
        if 'LIMIT' in last_line.upper():
            # Find and replace the limit value
            import re
            solution_lines[-1] = re.sub(r'LIMIT\s+\d+', f'LIMIT {limit}', last_line, flags=re.IGNORECASE)
    
    modified_solution = '\n'.join(solution_lines)
    
    return db_manager.execute_query(modified_solution)

def format_dataframe_as_markdown_table(df, max_rows=20):
    """Convert pandas DataFrame to markdown table format"""
    if df is None or df.empty:
        return "No results returned."
    
    # Limit to max_rows
    display_df = df.head(max_rows)
    
    # Convert to markdown table
    markdown_lines = []
    
    # Header row
    headers = list(display_df.columns)
    markdown_lines.append('| ' + ' | '.join(headers) + ' |')
    
    # Separator row
    separators = ['---'] * len(headers)
    markdown_lines.append('| ' + ' | '.join(separators) + ' |')
    
    # Data rows
    for _, row in display_df.iterrows():
        row_values = []
        for col in headers:
            value = row[col]
            # Handle None/NaN values
            if pd.isna(value):
                row_values.append('NULL')
            elif isinstance(value, float):
                # Format floats to avoid scientific notation
                if value.is_integer():
                    row_values.append(str(int(value)))
                else:
                    row_values.append(f'{value:.2f}')
            else:
                # Escape pipe characters in the data
                str_value = str(value).replace('|', '\\|')
                row_values.append(str_value)
        
        markdown_lines.append('| ' + ' | '.join(row_values) + ' |')
    
    return '\n'.join(markdown_lines)

def generate_markdown_report(exercise_key, dataset):
    """Generate a comprehensive markdown report for all exercises"""
    
    # Initialize database manager
    db_path = Path(f"../../datasets/{dataset}.db")
    if not db_path.exists():
        raise FileNotFoundError(f"Database not found: {db_path}")
    
    db_manager = SQLHelper(str(db_path))
    
    # Start markdown content
    markdown_content = []
    
    # Header
    markdown_content.append(f"# {exercise_key['metadata']['title']}")
    markdown_content.append("")
    markdown_content.append(f"**Description:** {exercise_key['metadata']['description']}")
    markdown_content.append(f"**Database:** {exercise_key['metadata']['database']}")
    markdown_content.append(f"**Total Exercises:** {exercise_key['metadata']['total_exercises']}")
    markdown_content.append(f"**Focus Topics:** {', '.join(exercise_key['metadata']['focus_topics'])}")
    markdown_content.append("")
    markdown_content.append(f"*Report generated on: {time.strftime('%Y-%m-%d %H:%M:%S')}*")
    markdown_content.append("")
    markdown_content.append("---")
    markdown_content.append("")
    
    # Process each exercise
    for exercise in exercise_key["exercises"]:
        print(f"Processing Exercise {exercise['id']}: {exercise['title']}")
        
        # Exercise header
        markdown_content.append(f"## Exercise {exercise['id']}: {exercise['title']}")
        markdown_content.append("")
        
        # Difficulty and topics
        difficulty = exercise.get('difficulty', 'Not specified')
        topics = exercise.get('topics', [])
        educational_focus = exercise.get('educational_focus', '')
        
        markdown_content.append(f"**Difficulty:** {difficulty}")
        markdown_content.append(f"**Topics:** {', '.join(topics)}")
        if educational_focus:
            markdown_content.append(f"**Educational Focus:** {educational_focus}")
        markdown_content.append("")
        
        # Exercise statement
        markdown_content.append("### Problem Statement")
        markdown_content.append("")
        markdown_content.append(exercise['statement'])
        markdown_content.append("")
        
        # SQL solution
        markdown_content.append("### SQL Solution")
        markdown_content.append("")
        markdown_content.append("```sql")
        markdown_content.append(exercise['solution'])
        markdown_content.append("```")
        markdown_content.append("")
        
        # Execute solution
        markdown_content.append("### Results")
        markdown_content.append("")
        
        try:
            result = execute_solution(db_manager, exercise['solution'], limit=20)
            
            if result['status'] == 'success':
                markdown_content.append(f"✅ **Query executed successfully**")
                markdown_content.append(f"- **Execution time:** {result['execution_time']}s")
                markdown_content.append(f"- **Rows returned:** {result['row_count']}")
                markdown_content.append(f"- **Columns:** {', '.join(result['columns'])}")
                markdown_content.append("")
                
                # Results table
                if result['data'] is not None and not result['data'].empty:
                    markdown_content.append("#### Top 20 Results")
                    markdown_content.append("")
                    table_markdown = format_dataframe_as_markdown_table(result['data'], max_rows=20)
                    markdown_content.append(table_markdown)
                else:
                    markdown_content.append("*No data returned by the query.*")
            else:
                markdown_content.append(f"❌ **Query failed**")
                markdown_content.append(f"- **Error:** {result['error']}")
                
        except Exception as e:
            markdown_content.append(f"❌ **Execution error:** {str(e)}")
        
        markdown_content.append("")
        markdown_content.append("---")
        markdown_content.append("")
    
    # Close database connection
    db_manager.close()
    
    return '\n'.join(markdown_content)

def main():
    parser = argparse.ArgumentParser(description='Generate markdown report for exercise solutions')
    parser.add_argument('--exercise-key', type=str, required=True, help='Path to exercise key JSON file')
    parser.add_argument('--dataset', type=str, required=True, help='Dataset name (e.g., data_jobs)')
    parser.add_argument('--output', type=str, help='Output markdown file path (optional)')
    
    args = parser.parse_args()
    
    # Load exercise key
    exercise_key_path = Path(args.exercise_key)
    if not exercise_key_path.exists():
        print(f"❌ Exercise key not found: {exercise_key_path}")
        return
    
    print(f"📖 Loading exercise key: {exercise_key_path}")
    exercise_key = load_exercise_key(exercise_key_path)
    
    # Validate database exists
    db_path = Path(f"../../datasets/{args.dataset}.db")
    if not db_path.exists():
        print(f"❌ Database not found: {db_path}")
        return
    
    print(f"🗃️ Using database: {db_path}")
    print(f"📝 Generating report for {len(exercise_key['exercises'])} exercises...")
    print()
    
    # Generate markdown report
    try:
        markdown_content = generate_markdown_report(exercise_key, args.dataset)
        
        # Determine output file
        if args.output:
            output_path = Path(args.output)
        else:
            dataset_name = args.dataset  # Keep underscores
            week_num = exercise_key['metadata'].get('week', 'X')
            
            # Extract version from exercise key file name if present
            exercise_key_filename = Path(args.exercise_key).name
            version = ""
            if "_v" in exercise_key_filename:
                version_part = exercise_key_filename.split("_v")[-1].split(".")[0]
                version = f"_v{version_part}"
            
            # Use absolute path relative to project root, not current working directory
            project_root = Path(__file__).parent.parent.parent
            output_path = project_root / "reports" / f"week_{week_num}" / f"week_{week_num}_key_report_{dataset_name}{version}.md"
            
        # Create reports directory structure if it doesn't exist
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Write report
        with open(output_path, 'w') as f:
            f.write(markdown_content)
        
        print(f"✅ Report generated successfully!")
        print(f"📁 Output: {output_path}")
        print(f"📊 File size: {output_path.stat().st_size / 1024:.1f} KB")
        
    except Exception as e:
        print(f"❌ Error generating report: {str(e)}")

if __name__ == "__main__":
    main() 