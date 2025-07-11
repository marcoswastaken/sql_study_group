#!/usr/bin/env python3
"""
Generate data_schema_jobs.json with comprehensive database schema information for the jobs dataset.
Includes table creation queries showing how each table was derived from the original dataset.
"""

import json
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'core'))
from sql_helper import SQLHelper

def get_table_descriptions():
    """Get descriptions for tables based on the database schema."""
    return {
        'companies': 'Contains information about companies that post job listings',
        'locations': 'Geographic information for job locations including city and country',
        'platforms': 'Job posting platforms (LinkedIn, Indeed, etc.) where jobs are advertised',
        'jobs': 'Main table containing all job postings with details like title, salary, and requirements',
        'skills': 'Available skills that can be required for jobs, categorized by type',
        'job_skills': 'Junction table linking jobs to their required skills (many-to-many relationship)'
    }

def get_table_creation_queries():
    """Get the creation queries showing how each table was derived from the original dataset."""
    # Load queries from JSON file
    queries_file = os.path.join(os.path.dirname(__file__), 'table_creation_queries_jobs.json')
    with open(queries_file, 'r', encoding='utf-8') as f:
        queries_data = json.load(f)
    
    # Extract just the query strings for each table
    return {table: data['query'] for table, data in queries_data['queries'].items()}

def get_column_descriptions():
    """Get descriptions for important columns."""
    return {
        # Companies table
        'company_id': 'Unique identifier for each company',
        'company_name': 'Name of the company posting the job',
        
        # Locations table
        'location_id': 'Unique identifier for each location',
        'job_location': 'City or geographic area where the job is located',
        'job_country': 'Country where the job is located',
        
        # Platforms table
        'platform_id': 'Unique identifier for each job posting platform',
        'platform_name': 'Name of the platform (e.g., "via LinkedIn", "via Indeed")',
        
        # Jobs table
        'job_id': 'Unique identifier for each job posting',
        'job_title_short': 'Standardized job title category (e.g., "Data Scientist", "Data Engineer")',
        'job_title': 'Full job title as posted by the company',
        'job_schedule_type': 'Employment type (full-time, part-time, contract, etc.)',
        'job_work_from_home': 'Boolean indicating if remote work is available',
        'job_posted_date': 'Date and time when the job was posted',
        'job_no_degree_mention': 'Boolean indicating if the job posting mentions no degree requirement',
        'job_health_insurance': 'Boolean indicating if health insurance is mentioned as a benefit',
        'salary_rate': 'Rate type for salary (yearly, hourly, etc.)',
        'salary_year_avg': 'Average yearly salary in USD',
        'salary_hour_avg': 'Average hourly salary in USD',
        
        # Skills table
        'skill_id': 'Unique identifier for each skill',
        'skill_name': 'Name of the skill (e.g., "Python", "SQL", "Excel")',
        'skill_category': 'Category of the skill (programming, analyst_tools, cloud, etc.)',
        
        # Job_skills table
        # job_id and skill_id are foreign keys linking jobs to skills
    }

def get_table_info(helper):
    """Get comprehensive information about all tables."""
    tables_info = []
    
    # Get list of all tables
    tables_result = helper.execute_query("SHOW TABLES")
    if tables_result['status'] != 'success':
        print("❌ Failed to get table list")
        return []
    
    table_names = [row['name'] for row in tables_result['data'].to_dict('records')]
    table_descriptions = get_table_descriptions()
    column_descriptions = get_column_descriptions()
    creation_queries = get_table_creation_queries()
    
    for i, table_name in enumerate(table_names, 1):
        print(f"📋 Processing table {i}: {table_name}")
        
        # Get table structure
        describe_result = helper.execute_query(f"DESCRIBE {table_name}")
        if describe_result['status'] != 'success':
            print(f"  ❌ Failed to describe {table_name}")
            continue
        
        # Get sample data to better understand the table
        sample_result = helper.execute_query(f"SELECT * FROM {table_name} LIMIT 3")
        sample_data = []
        if sample_result['status'] == 'success' and not sample_result['data'].empty:
            sample_df = sample_result['data'].astype(str)
            sample_data = sample_df.to_dict('records')
        
        # Get row count
        count_result = helper.execute_query(f"SELECT COUNT(*) as row_count FROM {table_name}")
        row_count = 0
        if count_result['status'] == 'success':
            row_count = int(count_result['data'].iloc[0]['row_count'])
        
        # Process columns
        columns = []
        for col_info in describe_result['data'].to_dict('records'):
            col_name = col_info['column_name']
            col_type = col_info['column_type']
            is_nullable = col_info['null'] == 'YES'
            is_primary_key = col_info['key'] == 'PRI'
            
            # Get description if available
            description = column_descriptions.get(col_name, "")
            
            # Add foreign key information
            foreign_key_info = ""
            if col_name.endswith('_id') and not is_primary_key:
                if col_name == 'company_id':
                    foreign_key_info = "References companies.company_id"
                elif col_name == 'location_id':
                    foreign_key_info = "References locations.location_id"
                elif col_name == 'platform_id':
                    foreign_key_info = "References platforms.platform_id"
                elif col_name == 'job_id' and table_name == 'job_skills':
                    foreign_key_info = "References jobs.job_id"
                elif col_name == 'skill_id':
                    foreign_key_info = "References skills.skill_id"
            
            columns.append({
                'name': col_name,
                'type': col_type,
                'nullable': is_nullable,
                'primary_key': is_primary_key,
                'description': description,
                'foreign_key': foreign_key_info
            })
        
        table_info = {
            'id': i,
            'name': table_name,
            'description': table_descriptions.get(table_name, ""),
            'creation_query': creation_queries.get(table_name, ""),
            'row_count': row_count,
            'columns': columns,
            'sample_data': sample_data
        }
        
        tables_info.append(table_info)
    
    return tables_info

def generate_relationships():
    """Generate relationship information between tables."""
    return [
        {
            'type': 'one-to-many',
            'from_table': 'companies',
            'from_column': 'company_id',
            'to_table': 'jobs',
            'to_column': 'company_id',
            'description': 'One company can have many job postings'
        },
        {
            'type': 'one-to-many',
            'from_table': 'locations',
            'from_column': 'location_id',
            'to_table': 'jobs',
            'to_column': 'location_id',
            'description': 'One location can have many job postings'
        },
        {
            'type': 'one-to-many',
            'from_table': 'platforms',
            'from_column': 'platform_id',
            'to_table': 'jobs',
            'to_column': 'platform_id',
            'description': 'One platform can have many job postings'
        },
        {
            'type': 'many-to-many',
            'from_table': 'jobs',
            'from_column': 'job_id',
            'to_table': 'skills',
            'to_column': 'skill_id',
            'junction_table': 'job_skills',
            'description': 'Jobs can require multiple skills, and skills can be required by multiple jobs'
        }
    ]

def generate_data_jobs_schema():
    """Generate the complete data jobs schema JSON file."""
    print("🔧 Generating Data Jobs Schema...")
    
    # Initialize SQL helper with correct database path
    helper = SQLHelper('../../datasets/data_jobs.db')
    
    # Get table information
    tables_info = get_table_info(helper)
    
    # Close helper
    helper.close()
    
    if not tables_info:
        print("❌ No table information retrieved")
        return
    
    # Create comprehensive summary
    summary_data = {
        'metadata': {
            'database_name': 'data_jobs.db',
            'description': 'Normalized schema for real-world data analytics job postings dataset',
            'total_tables': len(tables_info),
            'total_records': int(sum(table['row_count'] for table in tables_info)),
            'source': 'Luke Barousse Data Jobs Dataset from HuggingFace',
            'original_dataset_size': 785741,
            'normalization_approach': 'Dimensional modeling with fact table (jobs) and dimension tables (companies, locations, platforms, skills)',
            'year': '2023',
            'creation_date': '2024',
            'use_cases': [
                'SQL practice exercises',
                'JOIN operations training', 
                'Database normalization examples',
                'Real-world data analysis',
                'Business intelligence tutorials'
            ]
        },
        'tables': tables_info,
        'relationships': generate_relationships(),
        'schema_notes': [
            'Database follows normalized design principles with dimensional modeling approach',
            'All dimension tables (companies, locations, platforms, skills) were extracted from the original dataset',
            'The jobs table serves as the central fact table with foreign key references',
            'Foreign key relationships ensure data integrity and enable efficient JOINs',
            'Junction table (job_skills) implements many-to-many relationship between jobs and skills',
            'Creation queries show the normalization process from raw data to structured schema',
            'Salary information is in USD where available',
            'Date format follows ISO 8601 standard (YYYY-MM-DD HH:MM:SS)',
            'Schema is optimized for educational SQL exercises and real-world analysis'
        ]
    }
    
    # Save to JSON file in schemas directory
    output_path = '../../schemas/data_schema_jobs.json'
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(summary_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n🎉 Generated {output_path}")
    print(f"📊 Summary:")
    print(f"  📋 Tables: {len(tables_info)}")
    print(f"  📈 Total Records: {int(sum(table['row_count'] for table in tables_info)):,}")
    print(f"  🔗 Relationships: {len(generate_relationships())}")
    
    # Print table overview
    print(f"\n📋 Table Overview:")
    for table in tables_info:
        print(f"  • {table['name']}: {int(table['row_count']):,} rows, {len(table['columns'])} columns")
    
    return summary_data

if __name__ == "__main__":
    schema_data = generate_data_jobs_schema()
    print("\n✨ Data jobs schema generated successfully!") 