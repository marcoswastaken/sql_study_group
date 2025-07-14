"""
SQL execution service for running student queries against the DuckDB database.
"""

import time
from typing import Any, Dict, List

import duckdb


class SQLService:
    """Service for executing SQL queries against the DuckDB database."""

    def __init__(self, db_path: str):
        """
        Initialize the SQL service.

        Args:
            db_path: Path to the DuckDB database file
        """
        self.db_path = db_path

    def execute_query(self, query: str, limit: int = 1000) -> Dict[str, Any]:
        """
        Execute a SQL query and return results with metadata.

        Args:
            query: SQL query to execute
            limit: Maximum number of rows to return

        Returns:
            Dictionary containing query results, metadata, and any errors
        """
        start_time = time.time()

        try:
            # Clean up the query
            query = query.strip()
            if not query:
                return {
                    "success": False,
                    "error": "Query is empty",
                    "data": [],
                    "columns": [],
                    "row_count": 0,
                    "execution_time": 0,
                }

            # Add LIMIT if not present and query is SELECT
            if self._is_select_query(query) and not self._has_limit(query):
                # Remove trailing semicolon if present before adding LIMIT
                if query.rstrip().endswith(";"):
                    query = query.rstrip()[:-1]
                query = f"{query} LIMIT {limit}"

            # Execute the query
            with duckdb.connect(self.db_path) as conn:
                result = conn.execute(query).fetchall()

                # Get column names from the query description
                columns = (
                    [desc[0] for desc in conn.description] if conn.description else []
                )

                # Convert results to list of dictionaries
                data = []
                if result and columns:
                    for row in result:
                        data.append(dict(zip(columns, row)))

                execution_time = time.time() - start_time

                return {
                    "success": True,
                    "error": None,
                    "data": data,
                    "columns": columns,
                    "row_count": len(data),
                    "execution_time": round(execution_time, 4),
                }

        except Exception as e:
            execution_time = time.time() - start_time
            return {
                "success": False,
                "error": str(e),
                "data": [],
                "columns": [],
                "row_count": 0,
                "execution_time": round(execution_time, 4),
            }

    def get_table_info(self) -> List[Dict[str, Any]]:
        """
        Get information about all tables in the database.

        Returns:
            List of table information dictionaries
        """
        try:
            with duckdb.connect(self.db_path) as conn:
                # Get all table names
                tables_result = conn.execute("SHOW TABLES").fetchall()
                tables = [table[0] for table in tables_result]

                table_info = []
                for table_name in tables:
                    # Get table schema
                    desc_result = conn.execute(f"DESCRIBE {table_name}").fetchall()

                    # Get row count
                    count_result = conn.execute(
                        f"SELECT COUNT(*) FROM {table_name}"
                    ).fetchone()
                    row_count = count_result[0] if count_result else 0

                    column_info = []
                    for col in desc_result:
                        column_info.append(
                            {
                                "name": col[0],
                                "type": col[1],
                                "nullable": col[2] == "YES",
                                "primary_key": False,  # DuckDB doesn't easily expose PK info
                            }
                        )

                    table_info.append(
                        {
                            "name": table_name,
                            "row_count": row_count,
                            "columns": column_info,
                        }
                    )

                return table_info

        except Exception as e:
            return [{"error": str(e)}]

    def get_sample_data(self, table_name: str, limit: int = 5) -> Dict[str, Any]:
        """
        Get sample data from a table.

        Args:
            table_name: Name of the table to sample
            limit: Number of rows to return

        Returns:
            Dictionary containing sample data
        """
        query = f"SELECT * FROM {table_name} LIMIT {limit}"
        return self.execute_query(query)

    def validate_query(self, query: str) -> Dict[str, Any]:
        """
        Validate a SQL query without executing it.

        Args:
            query: SQL query to validate

        Returns:
            Dictionary containing validation results
        """
        try:
            with duckdb.connect(self.db_path) as conn:
                # Use EXPLAIN to validate without executing
                conn.execute(f"EXPLAIN {query}")
                return {"valid": True, "error": None}
        except Exception as e:
            return {"valid": False, "error": str(e)}

    def _is_select_query(self, query: str) -> bool:
        """Check if query is a SELECT statement."""
        return query.upper().strip().startswith("SELECT")

    def _has_limit(self, query: str) -> bool:
        """Check if query already has a LIMIT clause."""
        return "LIMIT" in query.upper()

    def get_table_schema(self, table_name: str) -> Dict[str, Any]:
        """
        Get detailed schema information for a specific table.

        Args:
            table_name: Name of the table

        Returns:
            Dictionary containing table schema information
        """
        try:
            with duckdb.connect(self.db_path) as conn:
                # Get table schema
                desc_result = conn.execute(f"DESCRIBE {table_name}").fetchall()

                column_info = []
                for col in desc_result:
                    column_info.append(
                        {
                            "name": col[0],
                            "type": col[1],
                            "nullable": col[2] == "YES",
                            "default": col[3] if len(col) > 3 else None,
                            "primary_key": False,  # DuckDB doesn't easily expose PK info
                        }
                    )

                return {
                    "name": table_name,
                    "columns": column_info,
                    "foreign_keys": [],  # DuckDB doesn't store FK metadata easily
                    "indexes": [],  # DuckDB doesn't expose index info easily
                }

        except Exception as e:
            return {"error": str(e)}
