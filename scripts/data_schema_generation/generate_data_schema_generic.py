#!/usr/bin/env python3
"""
Phase 2: Generic Data Schema Generation Script

Generates comprehensive data schema documentation by introspecting the database
and combining with existing JSON artifacts. Produces deterministic information
with strategic placeholders for agent enhancement.

Usage: python generate_data_schema_generic.py --dataset jobs
"""

import json
import sys
import os
import argparse
from pathlib import Path
from datetime import datetime

# Add core directory to path for sql_helper
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'core'))
from sql_helper import SQLHelper

def load_existing_artifacts(dataset_name):
    """Load existing JSON artifacts for context and enhancement."""
    artifacts = {}
    
    # Load table creation queries if available
    queries_file = Path(__file__).parent / f'table_creation_queries_{dataset_name}.json'
    if queries_file.exists():
        with open(queries_file, 'r', encoding='utf-8') as f:
            artifacts['table_queries'] = json.load(f)
    
    # Load initial exploration if available
    exploration_file = Path(__file__).parent / f'initial_exploration_{dataset_name}.json'
    if exploration_file.exists():
        with open(exploration_file, 'r', encoding='utf-8') as f:
            artifacts['exploration'] = json.load(f)
    
    return artifacts

def detect_foreign_keys(column_name, table_name, all_tables):
    """Detect foreign key relationships using naming conventions."""
    if not column_name.endswith('_id'):
        return ""
    
    # Skip primary keys
    if column_name == f"{table_name}_id":
        return ""
    
    # Look for referenced table based on naming convention
    potential_table = column_name.replace('_id', 's')  # e.g., company_id -> companies
    if potential_table in all_tables:
        return f"References {potential_table}.{column_name}"
    
    # Try singular form
    potential_table = column_name.replace('_id', '')  # e.g., company_id -> company
    if potential_table in all_tables:
        return f"References {potential_table}.{column_name}"
    
    return ""

def introspect_database(helper, artifacts):
    """Introspect database to get comprehensive table information."""
    print("🔍 Introspecting database structure...")
    
    # Get all tables
    tables_result = helper.execute_query("SHOW TABLES")
    if tables_result['status'] != 'success':
        print("❌ Failed to get table list")
        return []
    
    table_names = [row['name'] for row in tables_result['data'].to_dict('records')]
    print(f"📋 Found {len(table_names)} tables: {', '.join(table_names)}")
    
    tables_info = []
    creation_queries = {}
    
    # Extract creation queries from artifacts
    if 'table_queries' in artifacts:
        creation_queries = {name: data['query'] for name, data in artifacts['table_queries']['tables'].items()}
    
    for i, table_name in enumerate(table_names, 1):
        print(f"📊 Processing table {i}/{len(table_names)}: {table_name}")
        
        # Get table structure
        describe_result = helper.execute_query(f"DESCRIBE {table_name}")
        if describe_result['status'] != 'success':
            print(f"  ❌ Failed to describe {table_name}")
            continue
        
        # Get row count
        count_result = helper.execute_query(f"SELECT COUNT(*) as row_count FROM {table_name}")
        row_count = 0
        if count_result['status'] == 'success':
            row_count = int(count_result['data'].iloc[0]['row_count'])
        
        # Get sample data
        sample_result = helper.execute_query(f"SELECT * FROM {table_name} LIMIT 3")
        sample_data = []
        if sample_result['status'] == 'success' and not sample_result['data'].empty:
            sample_df = sample_result['data'].astype(str)
            sample_data = sample_df.to_dict('records')
        
        # Process columns
        columns = []
        for col_info in describe_result['data'].to_dict('records'):
            col_name = col_info['column_name']
            col_type = col_info['column_type']
            is_nullable = col_info['null'] == 'YES'
            is_primary_key = col_info['key'] == 'PRI'
            
            # Detect foreign keys
            foreign_key_info = detect_foreign_keys(col_name, table_name, table_names)
            
            columns.append({
                'name': col_name,
                'type': col_type,
                'nullable': is_nullable,
                'primary_key': is_primary_key,
                'foreign_key': foreign_key_info,
                'description': ""  # Placeholder for agent enhancement
            })
        
        table_info = {
            'id': i,
            'name': table_name,
            'description': "",  # Placeholder for agent enhancement
            'creation_query': creation_queries.get(table_name, ""),
            'row_count': row_count,
            'columns': columns,
            'sample_data': sample_data,
            'educational_purpose': ""  # Placeholder for agent enhancement
        }
        
        tables_info.append(table_info)
    
    return tables_info

def generate_relationships(tables_info):
    """Generate relationship information based on foreign key detection."""
    relationships = []
    
    for table in tables_info:
        for column in table['columns']:
            if column['foreign_key']:
                # Parse foreign key reference
                if 'References' in column['foreign_key']:
                    ref_parts = column['foreign_key'].replace('References ', '').split('.')
                    if len(ref_parts) == 2:
                        ref_table, ref_column = ref_parts
                        relationships.append({
                            'type': 'one-to-many',
                            'from_table': ref_table,
                            'from_column': ref_column,
                            'to_table': table['name'],
                            'to_column': column['name'],
                            'description': ""  # Placeholder for agent enhancement
                        })
    
    return relationships

def generate_metadata(dataset_name, tables_info, artifacts):
    """Generate metadata section with deterministic information."""
    total_records = sum(table['row_count'] for table in tables_info)
    
    metadata = {
        'database_name': f'data_{dataset_name}.db',
        'description': "",  # Placeholder for agent enhancement
        'total_tables': len(tables_info),
        'total_records': total_records,
        'source': "",  # Placeholder for agent enhancement
        'generation_date': datetime.now().strftime('%Y-%m-%d'),
        'use_cases': []  # Placeholder for agent enhancement
    }
    
    # Add educational metadata if available from table queries
    if 'table_queries' in artifacts and 'metadata' in artifacts['table_queries']:
        query_metadata = artifacts['table_queries']['metadata']
        metadata.update({
            'target_week': query_metadata.get('target_week', ''),
            'core_concepts': query_metadata.get('core_concepts', []),
            'educational_focus': query_metadata.get('educational_focus', ''),
            'complexity_level': query_metadata.get('complexity_level', '')
        })
    
    return metadata

def generate_schema_notes(tables_info):
    """Generate schema notes based on detected patterns."""
    notes = []
    
    # Count foreign keys
    fk_count = sum(1 for table in tables_info for col in table['columns'] if col['foreign_key'])
    if fk_count > 0:
        notes.append(f"Database contains {fk_count} foreign key relationships ensuring referential integrity")
    
    # Check for junction tables (tables with multiple foreign keys)
    junction_tables = []
    for table in tables_info:
        fk_cols = [col for col in table['columns'] if col['foreign_key']]
        if len(fk_cols) >= 2:
            junction_tables.append(table['name'])
    
    if junction_tables:
        notes.append(f"Junction tables detected: {', '.join(junction_tables)} - implementing many-to-many relationships")
    
    # Add placeholders for agent enhancement
    notes.extend([
        "",  # Placeholder for normalization notes
        "",  # Placeholder for business logic notes
        "",  # Placeholder for optimization notes
    ])
    
    return notes

def generate_agent_prompt(dataset_name, output_path, schema_data, artifacts):
    """Generate a comprehensive prompt for agent enhancement."""
    print("\n" + "="*80)
    print("🤖 AGENT ENHANCEMENT PROMPT")
    print("="*80)
    
    # Context Overview
    print(f"\n📋 PHASE 2 COMPLETE - Schema Generated for '{dataset_name}' Dataset")
    print(f"📄 File: {output_path}")
    print(f"📊 Structure: {schema_data['metadata']['total_tables']} tables, {schema_data['metadata']['total_records']:,} records")
    
    # Educational Context
    if 'table_queries' in artifacts:
        metadata = artifacts['table_queries'].get('metadata', {})
        print(f"\n🎓 EDUCATIONAL CONTEXT:")
        print(f"  • Target Week: {metadata.get('target_week', 'N/A')}")
        print(f"  • Core Concepts: {', '.join(metadata.get('core_concepts', []))}")
        print(f"  • Focus: {metadata.get('educational_focus', 'N/A')}")
        print(f"  • Level: {metadata.get('complexity_level', 'N/A')}")
    
    # What's Already Done
    print(f"\n✅ DETERMINISTIC GENERATION COMPLETE:")
    print(f"  • Database introspection (11 tables discovered)")
    print(f"  • Column types, constraints, and nullability")
    print(f"  • Foreign key relationships via naming conventions")
    print(f"  • Sample data (3 rows per table)")
    print(f"  • Creation queries from table_creation_queries_{dataset_name}.json")
    print(f"  • Educational metadata preserved")
    
    # What Needs Enhancement
    print(f"\n🎯 AGENT ENHANCEMENT NEEDED:")
    print(f"Your task is to enhance the following BLANK fields with intelligent, contextual content:")
    
    enhancement_fields = schema_data['agent_enhancement_needed']['fields_to_enhance']
    for i, field in enumerate(enhancement_fields, 1):
        print(f"  {i}. {field}")
    
    # Specific Instructions
    print(f"\n📝 SPECIFIC ENHANCEMENT INSTRUCTIONS:")
    print(f"")
    print(f"1. METADATA ENHANCEMENTS:")
    print(f"   • metadata.description: Write a comprehensive overview of the database")
    print(f"   • metadata.source: Identify the original data source")
    print(f"   • metadata.use_cases: List 3-5 educational use cases")
    print(f"")
    print(f"2. TABLE ENHANCEMENTS:")
    print(f"   • tables[].description: Business context for each table")
    print(f"   • tables[].educational_purpose: Learning objectives per table")
    print(f"")
    print(f"3. COLUMN ENHANCEMENTS:")
    print(f"   • tables[].columns[].description: Semantic meaning of each column")
    print(f"   • Focus on business context, not just technical details")
    print(f"")
    print(f"4. RELATIONSHIP ENHANCEMENTS:")
    print(f"   • relationships[].description: Explain the business relationship")
    print(f"")
    print(f"5. SCHEMA NOTES:")
    print(f"   • Fill in the 3 empty strings with insights about:")
    print(f"     - Normalization approach and design decisions")
    print(f"     - Business logic and domain modeling")
    print(f"     - Optimization and performance considerations")
    
    # Next Steps
    print(f"\n🚀 NEXT STEPS:")
    print(f"1. Open the generated schema file: {output_path}")
    print(f"2. Enhance ALL empty string fields (\"\") with meaningful content")
    print(f"3. Use the sample data and creation queries for context")
    print(f"4. Ensure descriptions are educational and business-focused")
    print(f"5. Maintain the educational objectives for Week {metadata.get('target_week', 'N/A')} SQL curriculum")
    
    print(f"\n💡 TIPS:")
    print(f"   • Use the sample_data arrays to understand content patterns")
    print(f"   • Reference the creation_query fields for business logic")
    print(f"   • Focus on educational value for JOIN practice")
    print(f"   • Make descriptions helpful for SQL learning, not just documentation")
    
    print(f"\n🎯 SUCCESS CRITERIA:")
    print(f"   • No empty string fields remain")
    print(f"   • All descriptions are educational and contextual")
    print(f"   • Schema serves as comprehensive learning resource")
    print(f"   • Ready for SQL curriculum Week {metadata.get('target_week', 'N/A')} exercises")
    
    print("\n" + "="*80)
    print("Ready for Agent Enhancement! 🚀")
    print("="*80)

def generate_data_schema(dataset_name):
    """Generate comprehensive data schema with deterministic information."""
    print(f"🔧 Generating data schema for dataset: {dataset_name}")
    
    # Load existing artifacts
    artifacts = load_existing_artifacts(dataset_name)
    print(f"📁 Loaded {len(artifacts)} artifact types")
    
    # Connect to database
    # Handle dataset naming: if dataset_name contains '/', extract just the name part
    # If it doesn't start with 'data_', prefix it
    if '/' in dataset_name:
        # Extract name from HuggingFace format (e.g., "lukebarousse/data_jobs" -> "data_jobs")
        db_name = dataset_name.split('/')[-1]
    else:
        db_name = dataset_name
    
    # Ensure db_name starts with 'data_' if it doesn't already
    if not db_name.startswith('data_'):
        db_name = f'data_{db_name}'
    
    db_path = f'../../datasets/{db_name}.db'
    if not os.path.exists(db_path):
        print(f"❌ Database not found: {db_path}")
        return False
    
    helper = SQLHelper(db_path)
    
    # Introspect database
    tables_info = introspect_database(helper, artifacts)
    
    # Close database connection
    helper.close()
    
    if not tables_info:
        print("❌ No table information retrieved")
        return False
    
    # Generate relationships
    relationships = generate_relationships(tables_info)
    
    # Generate metadata
    metadata = generate_metadata(dataset_name, tables_info, artifacts)
    
    # Generate schema notes
    schema_notes = generate_schema_notes(tables_info)
    
    # Create comprehensive schema
    schema_data = {
        'metadata': metadata,
        'tables': tables_info,
        'relationships': relationships,
        'schema_notes': schema_notes,
        'agent_enhancement_needed': {
            'description': "The following fields need agent enhancement",
            'fields_to_enhance': [
                'metadata.description',
                'metadata.source', 
                'metadata.use_cases',
                'tables[].description',
                'tables[].educational_purpose',
                'tables[].columns[].description',
                'relationships[].description',
                'schema_notes (empty strings)'
            ]
        }
    }
    
    # Save to schemas directory
    output_path = f'../../schemas/data_schema_{dataset_name}.json'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(schema_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n🎉 Generated schema: {output_path}")
    print(f"📊 Summary:")
    print(f"  📋 Tables: {len(tables_info)}")
    print(f"  📈 Total Records: {sum(table['row_count'] for table in tables_info):,}")
    print(f"  🔗 Relationships: {len(relationships)}")
    print(f"  📝 Needs Agent Enhancement: {len(schema_data['agent_enhancement_needed']['fields_to_enhance'])} field types")
    
    # Generate agent enhancement prompt
    generate_agent_prompt(dataset_name, output_path, schema_data, artifacts)
    
    return True

def main():
    parser = argparse.ArgumentParser(description='Generate comprehensive data schema documentation')
    parser.add_argument('--dataset', required=True, help='Dataset name (e.g., jobs, movies)')
    
    args = parser.parse_args()
    
    success = generate_data_schema(args.dataset)
    
    if success:
        print(f"\n✨ Schema generation completed for {args.dataset}!")
        print("🤖 Ready for agent enhancement of semantic fields")
        sys.exit(0)
    else:
        print(f"\n💥 Schema generation failed for {args.dataset}")
        sys.exit(1)

if __name__ == "__main__":
    main() 