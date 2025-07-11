import duckdb
import pandas as pd
from typing import Union, Dict, Any, Optional
import traceback
from pathlib import Path
import json

class SQLHelper:
    """
    A helper class for executing SQL queries and returning formatted results.
    Designed for educational use with built-in safety and formatting features.
    """
    
    def __init__(self, db_path: str = "datasets/data_jobs.db"):
        """
        Initialize the SQL helper with a database connection.
        
        Args:
            db_path: Path to the DuckDB database file
        """
        self.db_path = Path(db_path)
        self.conn = None
        self._connect()
        
    def _connect(self):
        """Establish connection to the database."""
        try:
            if not self.db_path.exists():
                raise FileNotFoundError(f"Database file not found: {self.db_path}")
            
            self.conn = duckdb.connect(str(self.db_path))
            print(f"✅ Connected to database: {self.db_path}")
            
        except Exception as e:
            print(f"❌ Failed to connect to database: {e}")
            raise
    
    def execute_query(self, query: str, exercise_number: Optional[int] = None) -> Dict[str, Any]:
        """
        Execute a SQL query and return formatted results.
        
        Args:
            query: SQL query string
            exercise_number: Optional exercise number for context
            
        Returns:
            Dictionary containing status, data, and metadata
        """
        result = {
            "status": "success",
            "exercise_number": exercise_number,
            "query": query.strip(),
            "data": None,
            "error": None,
            "row_count": 0,
            "columns": [],
            "execution_time": None
        }
        
        try:
            # Clean and validate query
            clean_query = self._clean_query(query)
            if not clean_query:
                result["status"] = "error"
                result["error"] = "Empty or invalid query"
                return result
            
            # Execute query with timing
            import time
            start_time = time.time()
            
            df = pd.read_sql(clean_query, self.conn)
            
            end_time = time.time()
            result["execution_time"] = round(end_time - start_time, 3)
            
            # Format results
            result["data"] = df
            result["row_count"] = len(df)
            result["columns"] = df.columns.tolist()
            
            # Add summary for large results
            if len(df) > 100:
                result["summary"] = f"Query returned {len(df)} rows (showing first 100)"
            
        except Exception as e:
            result["status"] = "error"
            result["error"] = str(e)
            result["error_type"] = type(e).__name__
            result["traceback"] = traceback.format_exc()
            
        return result
    
    def _clean_query(self, query: str) -> str:
        """Clean and validate SQL query."""
        if not query or not isinstance(query, str):
            return ""
        
        # Remove leading/trailing whitespace
        query = query.strip()
        
        # Remove common notebook artifacts
        query = query.replace('%%sql', '').strip()
        
        # Basic validation - must have some SQL keywords
        query_lower = query.lower()
        sql_keywords = ['select', 'insert', 'update', 'delete', 'create', 'drop', 'alter', 'show', 'describe']
        
        if not any(keyword in query_lower for keyword in sql_keywords):
            return ""
        
        return query
    
    def display_result(self, result: Dict[str, Any], max_rows: int = 100) -> None:
        """
        Display query results in a formatted way.
        
        Args:
            result: Result dictionary from execute_query
            max_rows: Maximum number of rows to display
        """
        print("=" * 60)
        
        if result["exercise_number"]:
            print(f"🎯 Exercise {result['exercise_number']}")
        
        print(f"📝 Query: {result['query'][:100]}{'...' if len(result['query']) > 100 else ''}")
        
        if result["status"] == "error":
            print(f"❌ Error: {result['error']}")
            if result.get("error_type"):
                print(f"   Type: {result['error_type']}")
            return
        
        print(f"✅ Success! ({result['execution_time']}s)")
        print(f"📊 Rows: {result['row_count']}, Columns: {len(result['columns'])}")
        
        if result["data"] is not None and not result["data"].empty:
            print(f"📋 Columns: {', '.join(result['columns'])}")
            print()
            
            # Display data
            display_df = result["data"].head(max_rows)
            print(display_df.to_string(index=False))
            
            if len(result["data"]) > max_rows:
                print(f"... and {len(result['data']) - max_rows} more rows")
        else:
            print("📭 No data returned")
        
        print("=" * 60)
    
    def run_exercise(self, query: str, exercise_number: int, max_rows: int = 100) -> Dict[str, Any]:
        """
        Execute a query for a specific exercise and display results.
        
        Args:
            query: SQL query string
            exercise_number: Exercise number
            max_rows: Maximum rows to display
            
        Returns:
            Result dictionary
        """
        result = self.execute_query(query, exercise_number)
        self.display_result(result, max_rows)
        return result
    
    def get_table_info(self, table_name: str = None) -> None:
        """Display information about database tables."""
        try:
            if table_name:
                # Show specific table info
                info_query = f"DESCRIBE {table_name}"
                result = self.execute_query(info_query)
                print(f"📋 Table: {table_name}")
                self.display_result(result)
            else:
                # Show all tables
                tables_query = "SHOW TABLES"
                result = self.execute_query(tables_query)
                print("📋 Available Tables:")
                self.display_result(result)
                
        except Exception as e:
            print(f"❌ Error getting table info: {e}")
    
    def get_sample_data(self, table_name: str, limit: int = 5) -> None:
        """Show sample data from a table."""
        try:
            sample_query = f"SELECT * FROM {table_name} LIMIT {limit}"
            result = self.execute_query(sample_query)
            print(f"📊 Sample data from {table_name}:")
            self.display_result(result)
        except Exception as e:
            print(f"❌ Error getting sample data: {e}")
    
    def close(self):
        """Close the database connection."""
        if self.conn:
            self.conn.close()
            print("🔒 Database connection closed")


def create_sql_helper(db_path: str = "datasets/data_jobs.db") -> SQLHelper:
    """
    Convenience function to create a SQLHelper instance.
    
    Args:
        db_path: Path to the database file
        
    Returns:
        SQLHelper instance
    """
    return SQLHelper(db_path)


# Example usage functions for students
def run_sql(query: str, exercise_number: int = None, max_rows: int = 100) -> Dict[str, Any]:
    """
    Quick function to run SQL queries with formatted output.
    
    Args:
        query: SQL query string
        exercise_number: Optional exercise number
        max_rows: Maximum rows to display
        
    Returns:
        Result dictionary
    """
    helper = create_sql_helper()
    try:
        if exercise_number:
            return helper.run_exercise(query, exercise_number, max_rows)
        else:
            result = helper.execute_query(query)
            helper.display_result(result, max_rows)
            return result
    finally:
        helper.close()


def show_tables():
    """Show all available tables in the database."""
    helper = create_sql_helper()
    try:
        helper.get_table_info()
    finally:
        helper.close()


def describe_table(table_name: str):
    """Show structure of a specific table."""
    helper = create_sql_helper()
    try:
        helper.get_table_info(table_name)
    finally:
        helper.close()


def sample_data(table_name: str, limit: int = 5):
    """Show sample data from a table."""
    helper = create_sql_helper()
    try:
        helper.get_sample_data(table_name, limit)
    finally:
        helper.close()


if __name__ == "__main__":
    # Example usage
    print("🧪 Testing SQL Helper...")
    
    # Test basic functionality
    helper = create_sql_helper()
    
    # Show tables
    print("\n1. Available tables:")
    helper.get_table_info()
    
    # Sample query
    print("\n2. Sample query:")
    sample_query = "SELECT company_name, job_title, salary_year_avg FROM jobs j JOIN companies c ON j.company_id = c.company_id LIMIT 5"
    helper.run_exercise(sample_query, 1)
    
    helper.close()
    
    print("\n✅ SQL Helper ready for use!") 