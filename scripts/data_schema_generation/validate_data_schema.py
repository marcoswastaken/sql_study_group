#!/usr/bin/env python3
"""
Data Schema Validation Script

Validates the enhanced data schema JSON file to ensure:
1. Valid JSON structure
2. Required fields are present
3. No empty string fields remain
4. Educational context is preserved
5. Relationships are properly defined

Usage: python validate_data_schema.py --dataset data_jobs
"""

import json
import sys
import os
import argparse
from pathlib import Path

def validate_json_structure(file_path):
    """Validate that the file contains valid JSON."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print("✅ JSON structure valid")
        return data
    except json.JSONDecodeError as e:
        print(f"❌ JSON syntax error: {e}")
        return None
    except FileNotFoundError:
        print(f"❌ File not found: {file_path}")
        return None

def validate_metadata(metadata):
    """Validate metadata section completeness."""
    print("\n📋 Validating metadata section...")
    
    required_fields = [
        'database_name', 'description', 'total_tables', 'total_records',
        'source', 'generation_date', 'use_cases', 'target_week', 
        'core_concepts', 'educational_focus', 'complexity_level'
    ]
    
    missing_fields = []
    empty_fields = []
    
    for field in required_fields:
        if field not in metadata:
            missing_fields.append(field)
        elif metadata[field] == "" or metadata[field] == []:
            empty_fields.append(field)
    
    if missing_fields:
        print(f"❌ Missing metadata fields: {', '.join(missing_fields)}")
        return False
    
    if empty_fields:
        print(f"❌ Empty metadata fields: {', '.join(empty_fields)}")
        return False
    
    # Validate specific field types
    if not isinstance(metadata['use_cases'], list) or len(metadata['use_cases']) == 0:
        print("❌ use_cases must be a non-empty list")
        return False
    
    if not isinstance(metadata['core_concepts'], list) or len(metadata['core_concepts']) == 0:
        print("❌ core_concepts must be a non-empty list")
        return False
    
    print("✅ Metadata section valid")
    return True

def validate_table_structure(table, table_index):
    """Validate individual table structure."""
    required_fields = [
        'id', 'name', 'description', 'creation_query', 'row_count',
        'columns', 'sample_data', 'educational_purpose'
    ]
    
    missing_fields = []
    empty_fields = []
    
    for field in required_fields:
        if field not in table:
            missing_fields.append(field)
        elif field in ['description', 'educational_purpose'] and table[field] == "":
            empty_fields.append(field)
    
    if missing_fields:
        print(f"❌ Table {table_index} missing fields: {', '.join(missing_fields)}")
        return False
    
    if empty_fields:
        print(f"❌ Table {table_index} ({table.get('name', 'unknown')}) empty fields: {', '.join(empty_fields)}")
        return False
    
    # Validate columns
    if not isinstance(table['columns'], list) or len(table['columns']) == 0:
        print(f"❌ Table {table_index} must have non-empty columns list")
        return False
    
    for col_index, column in enumerate(table['columns']):
        if 'description' in column and column['description'] == "":
            print(f"❌ Table {table_index} column {col_index} ({column.get('name', 'unknown')}) has empty description")
            return False
    
    return True

def validate_tables_section(tables):
    """Validate all tables in the tables section."""
    print("\n📊 Validating tables section...")
    
    if not isinstance(tables, list) or len(tables) == 0:
        print("❌ Tables must be a non-empty list")
        return False
    
    for index, table in enumerate(tables):
        if not validate_table_structure(table, index + 1):
            return False
    
    print(f"✅ All {len(tables)} tables valid")
    return True

def validate_relationships(relationships):
    """Validate relationships section."""
    print("\n🔗 Validating relationships section...")
    
    if not isinstance(relationships, list) or len(relationships) == 0:
        print("❌ Relationships must be a non-empty list")
        return False
    
    required_fields = ['type', 'from_table', 'from_column', 'to_table', 'to_column', 'description']
    
    for index, relationship in enumerate(relationships):
        missing_fields = []
        empty_fields = []
        
        for field in required_fields:
            if field not in relationship:
                missing_fields.append(field)
            elif field == 'description' and relationship[field] == "":
                empty_fields.append(field)
        
        if missing_fields:
            print(f"❌ Relationship {index + 1} missing fields: {', '.join(missing_fields)}")
            return False
        
        if empty_fields:
            print(f"❌ Relationship {index + 1} empty fields: {', '.join(empty_fields)}")
            return False
    
    print(f"✅ All {len(relationships)} relationships valid")
    return True

def validate_schema_notes(schema_notes):
    """Validate schema notes section."""
    print("\n📝 Validating schema notes section...")
    
    if not isinstance(schema_notes, list) or len(schema_notes) == 0:
        print("❌ Schema notes must be a non-empty list")
        return False
    
    empty_count = sum(1 for note in schema_notes if note == "")
    if empty_count > 0:
        print(f"❌ Schema notes contains {empty_count} empty strings")
        return False
    
    print(f"✅ All {len(schema_notes)} schema notes valid")
    return True

def validate_educational_context(data):
    """Validate that educational context is preserved."""
    print("\n🎓 Validating educational context...")
    
    # Check metadata educational fields
    metadata = data.get('metadata', {})
    if metadata.get('target_week') != 4:
        print("❌ Target week should be 4 for this dataset")
        return False
    
    if 'JOIN' not in str(metadata.get('core_concepts', [])):
        print("❌ Core concepts should include JOIN operations")
        return False
    
    # Check that tables have educational purposes
    tables = data.get('tables', [])
    tables_without_purpose = [
        table['name'] for table in tables 
        if not table.get('educational_purpose') or table['educational_purpose'] == ""
    ]
    
    if tables_without_purpose:
        print(f"❌ Tables without educational purpose: {', '.join(tables_without_purpose)}")
        return False
    
    print("✅ Educational context preserved")
    return True

def count_enhancement_completion(data):
    """Count and report enhancement completion statistics."""
    print("\n📈 Enhancement completion statistics...")
    
    # Count total fields that were enhanced
    total_enhanced = 0
    
    # Metadata enhancements
    metadata = data.get('metadata', {})
    if metadata.get('description') and metadata['description'] != "":
        total_enhanced += 1
    if metadata.get('source') and metadata['source'] != "":
        total_enhanced += 1
    if metadata.get('use_cases') and len(metadata['use_cases']) > 0:
        total_enhanced += 1
    
    # Table enhancements
    tables = data.get('tables', [])
    for table in tables:
        if table.get('description') and table['description'] != "":
            total_enhanced += 1
        if table.get('educational_purpose') and table['educational_purpose'] != "":
            total_enhanced += 1
        
        # Column descriptions
        for column in table.get('columns', []):
            if column.get('description') and column['description'] != "":
                total_enhanced += 1
    
    # Relationship enhancements
    relationships = data.get('relationships', [])
    for relationship in relationships:
        if relationship.get('description') and relationship['description'] != "":
            total_enhanced += 1
    
    # Schema notes
    schema_notes = data.get('schema_notes', [])
    non_empty_notes = len([note for note in schema_notes if note != ""])
    
    print(f"📊 Total enhanced fields: {total_enhanced}")
    print(f"📊 Tables with descriptions: {len([t for t in tables if t.get('description')])}")
    print(f"📊 Tables with educational purposes: {len([t for t in tables if t.get('educational_purpose')])}")
    print(f"📊 Relationships with descriptions: {len([r for r in relationships if r.get('description')])}")
    print(f"📊 Schema notes completed: {non_empty_notes}/{len(schema_notes)}")
    
    return True

def validate_data_schema(dataset_name):
    """Main validation function."""
    print(f"🔍 Validating data schema for dataset: {dataset_name}")
    
    # Construct file path
    schema_file = f'../../schemas/data_schema_{dataset_name}.json'
    
    # Load and validate JSON structure
    data = validate_json_structure(schema_file)
    if not data:
        return False
    
    # Validate each section
    validations = [
        validate_metadata(data.get('metadata', {})),
        validate_tables_section(data.get('tables', [])),
        validate_relationships(data.get('relationships', [])),
        validate_schema_notes(data.get('schema_notes', [])),
        validate_educational_context(data),
        count_enhancement_completion(data)
    ]
    
    if all(validations):
        print(f"\n🎉 Schema validation PASSED for {dataset_name}!")
        print(f"📄 File: {schema_file}")
        print(f"📊 Structure: {data['metadata']['total_tables']} tables, {data['metadata']['total_records']:,} records")
        print("✅ Ready for next step: Generate Exercises and Solutions")
        return True
    else:
        print(f"\n💥 Schema validation FAILED for {dataset_name}")
        print("❌ Please fix the issues before proceeding")
        return False

def main():
    parser = argparse.ArgumentParser(description='Validate enhanced data schema JSON file')
    parser.add_argument('--dataset', required=True, help='Dataset name (e.g., data_jobs)')
    
    args = parser.parse_args()
    
    success = validate_data_schema(args.dataset)
    
    if success:
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main() 