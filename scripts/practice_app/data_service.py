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
        self.current_dataset = None
        
    def load_exercises(self, week: int = 4) -> Dict[str, Any]:
        """
        Load exercise data for the specified week, automatically finding the latest version.
        
        Args:
            week: Week number to load exercises for
            
        Returns:
            Dictionary containing exercise data
        """
        if self.exercises_data is None:
            exercises_file = self._find_latest_exercise_file(week)
            
            if not os.path.exists(exercises_file):
                raise FileNotFoundError(f"Exercises file not found: {exercises_file}")
                
            with open(exercises_file, 'r') as f:
                self.exercises_data = json.load(f)
            
            # Extract dataset name from exercise metadata
            self.current_dataset = self._extract_dataset_name(self.exercises_data)
                
        return self.exercises_data
    
    def _find_latest_exercise_file(self, week: int) -> str:
        """
        Find the latest version of exercise file for the given week.
        
        Args:
            week: Week number
            
        Returns:
            Path to the latest exercise file
        """
        import glob
        import re
        
        # Look for all exercise files for this week
        pattern = os.path.join(self.base_path, f"exercises/week_{week}/week_{week}_key_v*.json")
        files = glob.glob(pattern)
        
        if not files:
            # Fallback to non-versioned file
            fallback = os.path.join(self.base_path, f"exercises/week_{week}_key.json")
            if os.path.exists(fallback):
                return fallback
            raise FileNotFoundError(f"No exercise files found for week {week}")
        
        # Extract version numbers and find the highest
        def extract_version(filename):
            match = re.search(r'_v(\d+)\.json$', filename)
            return int(match.group(1)) if match else 0
        
        # Sort by version number and return the latest
        latest_file = max(files, key=extract_version)
        return latest_file
    
    def _extract_dataset_name(self, exercises_data: Dict[str, Any]) -> str:
        """
        Extract dataset name from exercise metadata.
        
        Args:
            exercises_data: Exercise data dictionary
            
        Returns:
            Dataset name (e.g., "data_jobs")
        """
        database_file = exercises_data.get("metadata", {}).get("database", "data_jobs.db")
        # Remove .db extension to get dataset name
        dataset_name = database_file.replace(".db", "")
        return dataset_name
    
    def load_table_schema(self) -> Dict[str, Any]:
        """
        Load table schema information for the data dictionary.
        Auto-detects the correct schema based on the current dataset.
        
        Returns:
            Dictionary containing table schema data
        """
        if self.schema_data is None:
            # Ensure we have dataset info by loading exercises first
            if self.current_dataset is None:
                self.load_exercises()
            
            schema_file = os.path.join(
                self.base_path,
                f"schemas/data_schema_{self.current_dataset}.json"
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
        Get the path to the database file.
        Auto-detects the correct database based on the current dataset.
        
        Returns:
            Path to the database file
        """
        # Ensure we have dataset info by loading exercises first
        if self.current_dataset is None:
            self.load_exercises()
            
        db_path = os.path.join(self.base_path, f"datasets/{self.current_dataset}.db")
        if not os.path.exists(db_path):
            raise FileNotFoundError(f"Database file not found: {db_path}")
        return db_path
    
    def get_current_dataset(self) -> str:
        """
        Get the name of the current dataset.
        
        Returns:
            Current dataset name
        """
        if self.current_dataset is None:
            self.load_exercises()
        return self.current_dataset 