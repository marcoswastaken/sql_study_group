"""
Data service for loading exercise data and table schemas for the SQL practice app.
"""

import json
import os
from typing import Dict, List, Any, Optional


class DataService:
    """Service for loading and managing exercise data and table schemas."""
    
    def __init__(self, base_path: str = None):
        """
        Initialize the data service.
        
        Args:
            base_path: Base path for the project. If None, uses current directory.
        """
        self.base_path = base_path or os.getcwd()
        self.exercises_data = None
        self.schema_data = None
        
    def load_exercises(self, week: int = 4) -> Dict[str, Any]:
        """
        Load exercise data for the specified week.
        
        Args:
            week: Week number to load exercises for
            
        Returns:
            Dictionary containing exercise data
        """
        if self.exercises_data is None:
            exercises_file = os.path.join(
                self.base_path, 
                f"exercises/week_{week}/week_{week}_key_v4.json"
            )
            
            if not os.path.exists(exercises_file):
                raise FileNotFoundError(f"Exercises file not found: {exercises_file}")
                
            with open(exercises_file, 'r') as f:
                self.exercises_data = json.load(f)
                
        return self.exercises_data
    
    def load_table_schema(self) -> Dict[str, Any]:
        """
        Load table schema information for the data dictionary.
        
        Returns:
            Dictionary containing table schema data
        """
        if self.schema_data is None:
            schema_file = os.path.join(
                self.base_path,
                "schemas/data_schema_data_jobs.json"
            )
            
            if not os.path.exists(schema_file):
                raise FileNotFoundError(f"Schema file not found: {schema_file}")
                
            with open(schema_file, 'r') as f:
                self.schema_data = json.load(f)
                
        return self.schema_data
    
    def get_exercise_list(self, week: int = 4) -> List[Dict[str, Any]]:
        """
        Get a list of exercises with basic information.
        
        Args:
            week: Week number to get exercises for
            
        Returns:
            List of exercise dictionaries with id, title, and difficulty
        """
        exercises = self.load_exercises(week)
        
        return [
            {
                "id": exercise["id"],
                "title": exercise["title"],
                "difficulty": exercise["difficulty"],
                "topics": exercise["topics"]
            }
            for exercise in exercises.get("exercises", [])
        ]
    
    def get_exercise_details(self, exercise_id: int, week: int = 4) -> Optional[Dict[str, Any]]:
        """
        Get detailed information for a specific exercise.
        
        Args:
            exercise_id: ID of the exercise to get details for
            week: Week number
            
        Returns:
            Exercise details or None if not found
        """
        exercises = self.load_exercises(week)
        
        for exercise in exercises.get("exercises", []):
            if exercise["id"] == exercise_id:
                return {
                    "id": exercise["id"],
                    "title": exercise["title"],
                    "statement": exercise["statement"],
                    "difficulty": exercise["difficulty"],
                    "topics": exercise["topics"],
                    "educational_focus": exercise.get("educational_focus", ""),
                    "solution": exercise.get("solution", ""),
                    "expected_result": exercise.get("result", {})
                }
        
        return None
    
    def get_table_info(self) -> List[Dict[str, Any]]:
        """
        Get simplified table information for the data dictionary.
        
        Returns:
            List of table information dictionaries
        """
        schema = self.load_table_schema()
        
        tables_info = []
        for table in schema.get("tables", []):
            table_info = {
                "name": table["name"],
                "description": table["description"],
                "row_count": table.get("row_count", 0),
                "columns": []
            }
            
            # Simplify column information for students
            for column in table.get("columns", []):
                column_info = {
                    "name": column["name"],
                    "type": column["type"],
                    "nullable": column.get("nullable", True),
                    "primary_key": column.get("primary_key", False),
                    "foreign_key": column.get("foreign_key", ""),
                    "description": column.get("description", "")
                }
                table_info["columns"].append(column_info)
            
            tables_info.append(table_info)
        
        return tables_info
    
    def get_database_path(self) -> str:
        """
        Get the path to the SQLite database file.
        
        Returns:
            Path to the database file
        """
        db_path = os.path.join(self.base_path, "datasets/data_jobs.db")
        if not os.path.exists(db_path):
            raise FileNotFoundError(f"Database file not found: {db_path}")
        return db_path 