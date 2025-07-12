#!/usr/bin/env python3
"""
Table Creation Queries Validation Script

This script validates table creation query JSON files by:
1. Checking JSON schema structure and required fields
2. Validating SQL queries using the sql_helper
3. Providing preview results for each table creation query
4. Generating comprehensive validation reports

Usage:
    python validate_table_creation_queries.py --input table_creation_queries_jobs.json
    python validate_table_creation_queries.py --input table_creation_queries_jobs.json --database ../datasets/data_jobs.db
"""

import argparse
import json
import sys
import os
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
import traceback

# Add core directory to path for sql_helper import
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'core'))
from sql_helper import SQLHelper

class TableCreationValidator:
    """
    Validates table creation query JSON files for structure and SQL validity.
    """
    
    def __init__(self, input_file: str, database_path: str = None):
        """
        Initialize the validator.
        
        Args:
            input_file: Path to the JSON file to validate
            database_path: Path to the database file (optional)
        """
        self.input_file = Path(input_file)
        self.database_path = database_path
        self.sql_helper = None
        self.validation_results = {
            "schema_validation": {"passed": False, "errors": [], "warnings": []},
            "query_validation": {"passed": False, "errors": [], "warnings": []},
            "query_results": {}
        }
        
    def validate_all(self) -> Dict[str, Any]:
        """
        Run complete validation process.
        
        Returns:
            Dictionary containing all validation results
        """
        print("🔍 VALIDATING TABLE CREATION QUERIES")
        print("=" * 60)
        
        # Step 1: Load and validate JSON structure
        json_data = self._load_and_validate_json()
        if not json_data:
            return self.validation_results
        
        # Step 2: Validate schema structure
        self._validate_schema_structure(json_data)
        
        # Step 3: Initialize SQL helper if database provided
        if self.database_path:
            self._initialize_sql_helper()
        
        # Step 4: Validate SQL queries
        if self.sql_helper:
            self._validate_sql_queries(json_data)
        else:
            print("⚠️  Database not provided - skipping SQL query validation")
        
        # Step 5: Generate summary report
        self._generate_summary_report()
        
        # Step 6: Clean up test tables
        if self.sql_helper:
            self._cleanup_test_tables(json_data)
        
        return self.validation_results
    
    def _load_and_validate_json(self) -> Optional[Dict[str, Any]]:
        """Load and validate JSON file."""
        try:
            if not self.input_file.exists():
                error_msg = f"Input file does not exist: {self.input_file}"
                self.validation_results["schema_validation"]["errors"].append(error_msg)
                print(f"❌ {error_msg}")
                return None
            
            with open(self.input_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            print(f"✅ JSON file loaded successfully: {self.input_file}")
            return data
            
        except json.JSONDecodeError as e:
            error_msg = f"Invalid JSON format: {e}"
            self.validation_results["schema_validation"]["errors"].append(error_msg)
            print(f"❌ {error_msg}")
            return None
        except Exception as e:
            error_msg = f"Error loading JSON file: {e}"
            self.validation_results["schema_validation"]["errors"].append(error_msg)
            print(f"❌ {error_msg}")
            return None
    
    def _validate_schema_structure(self, data: Dict[str, Any]) -> None:
        """Validate the JSON schema structure."""
        print("\n📋 VALIDATING SCHEMA STRUCTURE")
        print("-" * 40)
        
        # Check top-level required fields
        required_top_level = ["metadata", "tables"]
        for field in required_top_level:
            if field not in data:
                error_msg = f"Missing required top-level field: {field}"
                self.validation_results["schema_validation"]["errors"].append(error_msg)
                print(f"❌ {error_msg}")
        
        # Validate metadata structure
        if "metadata" in data:
            self._validate_metadata(data["metadata"])
        
        # Validate tables structure
        if "tables" in data:
            self._validate_tables(data["tables"])
        
        # Check for optional sections
        optional_sections = ["educational_queries", "learning_progression"]
        for section in optional_sections:
            if section in data:
                print(f"✅ Optional section found: {section}")
            else:
                warning_msg = f"Optional section missing: {section}"
                self.validation_results["schema_validation"]["warnings"].append(warning_msg)
                print(f"⚠️  {warning_msg}")
        
        # Set schema validation status
        if not self.validation_results["schema_validation"]["errors"]:
            self.validation_results["schema_validation"]["passed"] = True
            print("✅ Schema structure validation passed")
        else:
            print("❌ Schema structure validation failed")
    
    def _validate_metadata(self, metadata: Dict[str, Any]) -> None:
        """Validate metadata structure."""
        required_metadata_fields = ["description", "target_week", "core_concepts", "dataset_source"]
        
        for field in required_metadata_fields:
            if field not in metadata:
                error_msg = f"Missing required metadata field: {field}"
                self.validation_results["schema_validation"]["errors"].append(error_msg)
                print(f"❌ {error_msg}")
        
        # Validate specific field types
        if "target_week" in metadata:
            if not isinstance(metadata["target_week"], int):
                error_msg = "target_week must be an integer"
                self.validation_results["schema_validation"]["errors"].append(error_msg)
                print(f"❌ {error_msg}")
        
        if "core_concepts" in metadata:
            if not isinstance(metadata["core_concepts"], list):
                error_msg = "core_concepts must be a list"
                self.validation_results["schema_validation"]["errors"].append(error_msg)
                print(f"❌ {error_msg}")
    
    def _validate_tables(self, tables: Dict[str, Any]) -> None:
        """Validate tables structure."""
        if not isinstance(tables, dict):
            error_msg = "tables must be a dictionary"
            self.validation_results["schema_validation"]["errors"].append(error_msg)
            print(f"❌ {error_msg}")
            return
        
        if not tables:
            error_msg = "tables dictionary is empty"
            self.validation_results["schema_validation"]["errors"].append(error_msg)
            print(f"❌ {error_msg}")
            return
        
        print(f"📊 Found {len(tables)} tables to validate")
        
        # Validate each table
        for table_name, table_config in tables.items():
            self._validate_single_table(table_name, table_config)
    
    def _validate_single_table(self, table_name: str, table_config: Dict[str, Any]) -> None:
        """Validate a single table configuration."""
        required_table_fields = ["description", "educational_purpose", "row_count_estimate", "query"]
        
        for field in required_table_fields:
            if field not in table_config:
                error_msg = f"Table '{table_name}' missing required field: {field}"
                self.validation_results["schema_validation"]["errors"].append(error_msg)
                print(f"❌ {error_msg}")
        
        # Validate field types
        if "row_count_estimate" in table_config:
            if not isinstance(table_config["row_count_estimate"], int):
                error_msg = f"Table '{table_name}' row_count_estimate must be an integer"
                self.validation_results["schema_validation"]["errors"].append(error_msg)
                print(f"❌ {error_msg}")
        
        if "query" in table_config:
            if not isinstance(table_config["query"], str):
                error_msg = f"Table '{table_name}' query must be a string"
                self.validation_results["schema_validation"]["errors"].append(error_msg)
                print(f"❌ {error_msg}")
            elif not table_config["query"].strip():
                error_msg = f"Table '{table_name}' query cannot be empty"
                self.validation_results["schema_validation"]["errors"].append(error_msg)
                print(f"❌ {error_msg}")
        
        print(f"  ✅ Table '{table_name}' structure valid")
    
    def _initialize_sql_helper(self) -> None:
        """Initialize SQL helper with database connection."""
        try:
            self.sql_helper = SQLHelper(self.database_path)
            print(f"✅ SQL Helper initialized with database: {self.database_path}")
        except Exception as e:
            error_msg = f"Failed to initialize SQL Helper: {e}"
            self.validation_results["query_validation"]["errors"].append(error_msg)
            print(f"❌ {error_msg}")
    
    def _validate_sql_queries(self, data: Dict[str, Any]) -> None:
        """Validate SQL queries using sql_helper."""
        print("\n🔍 VALIDATING SQL QUERIES")
        print("-" * 40)
        
        if "tables" not in data:
            return
        
        tables = data["tables"]
        successful_queries = 0
        
        for table_name, table_config in tables.items():
            if "query" not in table_config:
                continue
            
            print(f"\n📋 Testing table: {table_name}")
            print(f"   Description: {table_config.get('description', 'No description')}")
            print(f"   Expected rows: {table_config.get('row_count_estimate', 'Unknown')}")
            
            success = self._test_single_query(table_name, table_config["query"])
            if success:
                successful_queries += 1
        
        # Set query validation status
        total_queries = len(tables)
        if successful_queries == total_queries:
            self.validation_results["query_validation"]["passed"] = True
            print(f"\n✅ All {total_queries} queries validated successfully")
        else:
            print(f"\n❌ {successful_queries}/{total_queries} queries validated successfully")
    
    def _test_single_query(self, table_name: str, query: str) -> bool:
        """Test a single SQL query."""
        try:
            # Drop table if it exists (for testing purposes)
            drop_query = f"DROP TABLE IF EXISTS {table_name}"
            drop_result = self.sql_helper.execute_query(drop_query)
            if drop_result["status"] == "success":
                print(f"   🗑️  Dropped existing table: {table_name}")
            
            # Execute the query
            result = self.sql_helper.execute_query(query)
            
            if result["status"] == "success":
                # Store results
                self.validation_results["query_results"][table_name] = {
                    "status": "success",
                    "row_count": result["row_count"],
                    "columns": result["columns"],
                    "execution_time": result["execution_time"],
                    "sample_data": result["data"].head(5).to_dict('records') if result["data"] is not None else []
                }
                
                print(f"   ✅ Query executed successfully")
                print(f"   📊 Created {result['row_count']} rows, {len(result['columns'])} columns")
                print(f"   ⏱️  Execution time: {result['execution_time']}s")
                print(f"   📋 Columns: {', '.join(result['columns'])}")
                
                # Show sample data
                if result["data"] is not None and not result["data"].empty:
                    print(f"   📄 Sample data (first 5 rows):")
                    sample_data = result["data"].head(5)
                    for i, row in sample_data.iterrows():
                        print(f"      Row {i+1}: {dict(row)}")
                else:
                    print(f"   📭 No data returned")
                
                return True
                
            else:
                # Query failed
                error_msg = f"Query failed for table '{table_name}': {result['error']}"
                self.validation_results["query_validation"]["errors"].append(error_msg)
                
                self.validation_results["query_results"][table_name] = {
                    "status": "error",
                    "error": result["error"],
                    "error_type": result.get("error_type", "Unknown")
                }
                
                print(f"   ❌ Query failed: {result['error']}")
                if result.get("error_type"):
                    print(f"   🔍 Error type: {result['error_type']}")
                
                return False
                
        except Exception as e:
            error_msg = f"Exception testing query for table '{table_name}': {e}"
            self.validation_results["query_validation"]["errors"].append(error_msg)
            
            self.validation_results["query_results"][table_name] = {
                "status": "exception",
                "error": str(e),
                "traceback": traceback.format_exc()
            }
            
            print(f"   ❌ Exception: {e}")
            return False
    
    def _cleanup_test_tables(self, data: Dict[str, Any]) -> None:
        """Clean up test tables created during validation."""
        print("\n🧹 CLEANING UP TEST TABLES")
        print("-" * 40)
        
        if "tables" not in data:
            return
        
        tables = data["tables"]
        cleaned_count = 0
        
        for table_name in tables.keys():
            try:
                drop_query = f"DROP TABLE IF EXISTS {table_name}"
                result = self.sql_helper.execute_query(drop_query)
                if result["status"] == "success":
                    print(f"   🗑️  Cleaned up table: {table_name}")
                    cleaned_count += 1
                else:
                    print(f"   ⚠️  Could not clean up table: {table_name}")
            except Exception as e:
                print(f"   ❌ Error cleaning table {table_name}: {e}")
        
        print(f"✅ Cleaned up {cleaned_count}/{len(tables)} test tables")
    
    def _generate_summary_report(self) -> None:
        """Generate final validation summary report."""
        print("\n" + "=" * 60)
        print("📊 VALIDATION SUMMARY REPORT")
        print("=" * 60)
        
        # Schema validation summary
        schema_status = "✅ PASSED" if self.validation_results["schema_validation"]["passed"] else "❌ FAILED"
        print(f"Schema Validation: {schema_status}")
        
        schema_errors = len(self.validation_results["schema_validation"]["errors"])
        schema_warnings = len(self.validation_results["schema_validation"]["warnings"])
        print(f"  - Errors: {schema_errors}")
        print(f"  - Warnings: {schema_warnings}")
        
        # Query validation summary
        if self.sql_helper:
            query_status = "✅ PASSED" if self.validation_results["query_validation"]["passed"] else "❌ FAILED"
            print(f"Query Validation: {query_status}")
            
            query_errors = len(self.validation_results["query_validation"]["errors"])
            total_queries = len(self.validation_results["query_results"])
            successful_queries = sum(1 for r in self.validation_results["query_results"].values() if r["status"] == "success")
            
            print(f"  - Total queries: {total_queries}")
            print(f"  - Successful: {successful_queries}")
            print(f"  - Failed: {query_errors}")
        else:
            print("Query Validation: ⚠️  SKIPPED (no database provided)")
        
        # Overall status
        overall_passed = (
            self.validation_results["schema_validation"]["passed"] and
            (self.validation_results["query_validation"]["passed"] or not self.sql_helper)
        )
        
        overall_status = "✅ PASSED" if overall_passed else "❌ FAILED"
        print(f"\nOverall Status: {overall_status}")
        
        if not overall_passed:
            print("\n🔍 Issues found:")
            for error in self.validation_results["schema_validation"]["errors"]:
                print(f"  - Schema: {error}")
            for error in self.validation_results["query_validation"]["errors"]:
                print(f"  - Query: {error}")


def main():
    """Main function for command-line usage."""
    parser = argparse.ArgumentParser(
        description="Validate table creation queries JSON files"
    )
    parser.add_argument(
        "--input", 
        required=True, 
        help="Path to the JSON file to validate"
    )
    parser.add_argument(
        "--database", 
        help="Path to the database file for SQL validation (optional)"
    )
    
    args = parser.parse_args()
    
    # Default database path if not provided
    if not args.database:
        # Try to find database in common locations
        possible_paths = [
            "datasets/data_jobs.db",
            "../datasets/data_jobs.db",
            "../../datasets/data_jobs.db"
        ]
        
        for path in possible_paths:
            if Path(path).exists():
                args.database = path
                break
    
    # Create validator and run validation
    validator = TableCreationValidator(args.input, args.database)
    results = validator.validate_all()
    
    # Exit with appropriate code
    overall_passed = (
        results["schema_validation"]["passed"] and
        (results["query_validation"]["passed"] or not args.database)
    )
    
    sys.exit(0 if overall_passed else 1)


if __name__ == "__main__":
    main() 