#!/usr/bin/env python3
"""
Dataset Exploration Script for SQL Curriculum Development

This script analyzes HuggingFace datasets to assess their suitability for SQL exercises
and provides comprehensive metadata for curriculum planning.

Usage:
    python scripts/core/explore_dataset.py --dataset lukebarousse/data_jobs --output initial_exploration_jobs.json
"""

import argparse
import json
import pandas as pd
import numpy as np
from datasets import load_dataset
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
import sys
import warnings
import os
import duckdb
import random

# Suppress warnings for cleaner output
warnings.filterwarnings('ignore')

class DatasetExplorer:
    """
    Comprehensive dataset exploration for SQL curriculum development.
    
    Analyzes HuggingFace datasets to determine:
    - Basic dataset characteristics
    - Column-level analysis and data types
    - Data quality metrics
    - Potential relationships and normalization opportunities
    - Educational suitability for SQL exercises
    """
    
    def __init__(self, dataset_name: str, split: str = "train", sample_size: int = 1000):
        """
        Initialize the dataset explorer.
        
        Args:
            dataset_name: HuggingFace dataset identifier (e.g., "lukebarousse/data_jobs")
            split: Dataset split to analyze (default: "train")
            sample_size: Number of sample values to extract per column
        """
        self.dataset_name = dataset_name
        self.split = split
        self.sample_size = sample_size
        self.df = None
        self.analysis_results = {}
    
    def load_dataset(self) -> bool:
        """
        Load the dataset from HuggingFace and convert to pandas DataFrame.
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            print(f"📥 Loading dataset: {self.dataset_name} (split: {self.split})")
            ds = load_dataset(self.dataset_name, split=self.split)
            self.df = ds.to_pandas()
            print(f"✅ Loaded {len(self.df):,} records with {len(self.df.columns)} columns")
            return True
        except Exception as e:
            print(f"❌ Failed to load dataset: {e}")
            return False
    
    def analyze_dataset(self) -> Dict[str, Any]:
        """
        Perform comprehensive dataset analysis.
        
        Returns:
            dict: Complete analysis results
        """
        if self.df is None:
            raise ValueError("Dataset not loaded. Call load_dataset() first.")
        
        if self.df.empty:
            raise ValueError("Dataset is empty - cannot perform analysis on empty dataset.")
        
        print("🔍 Analyzing dataset characteristics...")
        
        # Perform all analysis components
        metadata = self._analyze_metadata()
        columns = self._analyze_columns()
        data_quality = self._analyze_data_quality()
        relationships = self._detect_relationships()
        educational_assessment = self._assess_educational_value()
        
        self.analysis_results = {
            "metadata": metadata,
            "columns": columns,
            "data_quality": data_quality,
            "relationships": relationships,
            "educational_assessment": educational_assessment
        }
        
        return self.analysis_results
    
    def _analyze_metadata(self) -> Dict[str, Any]:
        """Analyze basic dataset metadata."""
        memory_usage_mb = self.df.memory_usage(deep=True).sum() / (1024 * 1024)
        
        return {
            "dataset_name": self.dataset_name.split('/')[-1],
            "hf_source": self.dataset_name,
            "split": self.split,
            "total_records": len(self.df),
            "total_columns": len(self.df.columns),
            "memory_usage_mb": round(memory_usage_mb, 2),
            "analysis_date": datetime.now().isoformat(),
            "column_names": list(self.df.columns)
        }
    
    def _analyze_columns(self) -> List[Dict[str, Any]]:
        """Perform detailed analysis of each column."""
        columns_analysis = []
        
        for col in self.df.columns:
            print(f"  📊 Analyzing column: {col}")
            
            col_data = self.df[col]
            analysis = {
                "name": col,
                "data_type": str(col_data.dtype),
                "pandas_type": self._classify_pandas_type(col_data),
                "null_count": int(col_data.isnull().sum()),
                "null_percentage": round((col_data.isnull().sum() / len(col_data)) * 100, 2),
                "unique_count": int(col_data.nunique()),
                "unique_percentage": round((col_data.nunique() / len(col_data)) * 100, 2),
                "sample_values": self._get_sample_values(col_data),
                "statistics": self._get_column_statistics(col_data)
            }
            
            # Add type-specific analysis
            if analysis["pandas_type"] in ["numeric", "datetime"]:
                analysis.update(self._analyze_numeric_column(col_data))
            elif analysis["pandas_type"] == "categorical":
                analysis.update(self._analyze_categorical_column(col_data))
            
            columns_analysis.append(analysis)
        
        return columns_analysis
    
    def _classify_pandas_type(self, series: pd.Series) -> str:
        """Classify pandas column into educational categories."""
        # Check boolean first since it might also be detected as numeric
        if pd.api.types.is_bool_dtype(series):
            return "boolean"
        elif series.dtype == 'bool' or set(series.dropna().unique()).issubset({True, False, 1, 0}):
            # Additional check for boolean-like data
            return "boolean"
        elif pd.api.types.is_datetime64_any_dtype(series):
            return "datetime"
        elif pd.api.types.is_numeric_dtype(series):
            return "numeric"
        elif series.dtype == 'object':
            # Check if it's categorical (low cardinality)
            unique_ratio = series.nunique() / len(series)
            if unique_ratio < 0.1:  # Less than 10% unique values
                return "categorical"
            else:
                return "text"
        else:
            return "other"
    
    def _get_sample_values(self, series: pd.Series, max_samples: int = 5) -> List[str]:
        """Get representative sample values from a column."""
        # Remove nulls and get unique values
        non_null_values = series.dropna().unique()
        
        if len(non_null_values) == 0:
            return ["(all null values)"]
        
        # Sample values (prefer most common ones for categorical data)
        if len(non_null_values) <= max_samples:
            samples = non_null_values
        else:
            # For categorical data, get most frequent values
            if self._classify_pandas_type(series) == "categorical":
                samples = series.value_counts().head(max_samples).index.tolist()
            else:
                # For other types, get random sample
                samples = np.random.choice(non_null_values, max_samples, replace=False)
        
        # Convert to strings and handle long values
        return [str(val)[:50] + "..." if len(str(val)) > 50 else str(val) for val in samples]
    
    def _get_column_statistics(self, series: pd.Series) -> Dict[str, Any]:
        """Get basic statistics for a column."""
        stats = {
            "count": int(series.count()),
            "memory_usage_mb": round(series.memory_usage(deep=True) / (1024 * 1024), 3)
        }
        
        if pd.api.types.is_numeric_dtype(series):
            stats.update({
                "mean": float(series.mean()) if not series.empty else None,
                "std": float(series.std()) if not series.empty else None,
                "min": float(series.min()) if not series.empty else None,
                "max": float(series.max()) if not series.empty else None,
                "median": float(series.median()) if not series.empty else None
            })
        
        return stats
    
    def _analyze_numeric_column(self, series: pd.Series) -> Dict[str, Any]:
        """Additional analysis for numeric columns."""
        # Only analyze if it's actually numeric (not datetime)
        if not pd.api.types.is_numeric_dtype(series):
            return {"potential_id_field": False}
            
        return {
            "is_integer": pd.api.types.is_integer_dtype(series),
            "has_negatives": bool((series < 0).any()) if not series.empty else False,
            "has_zeros": bool((series == 0).any()) if not series.empty else False,
            "potential_id_field": self._is_potential_id_field(series)
        }
    
    def _analyze_categorical_column(self, series: pd.Series) -> Dict[str, Any]:
        """Additional analysis for categorical columns."""
        value_counts = series.value_counts()
        
        return {
            "top_values": value_counts.head(10).to_dict(),
            "category_count": len(value_counts),
            "potential_foreign_key": self._is_potential_foreign_key(series)
        }
    
    def _is_potential_id_field(self, series: pd.Series) -> bool:
        """Determine if a numeric column could be an ID field."""
        if not pd.api.types.is_numeric_dtype(series):
            return False
        
        if series.empty:
            return False
        
        # Check for ID-like characteristics
        unique_ratio = series.nunique() / len(series)
        is_sequential = False
        has_no_negatives = (series.min() >= 0)
        
        if pd.api.types.is_integer_dtype(series):
            sorted_values = series.dropna().sort_values()
            if len(sorted_values) > 1:
                # Check if values are roughly sequential
                diffs = sorted_values.diff().dropna()
                is_sequential = (diffs == 1).mean() > 0.8
        
        return unique_ratio > 0.9 and has_no_negatives and (is_sequential or unique_ratio > 0.98)
    
    def _is_potential_foreign_key(self, series: pd.Series) -> bool:
        """Determine if a categorical column could be a foreign key."""
        if series.empty:
            return False
            
        unique_ratio = series.nunique() / len(series)
        unique_count = series.nunique()
        
        # Potential FK if it has moderate cardinality (not too unique, not too few values)
        # Adjusted thresholds to be more permissive for testing
        return 0.001 < unique_ratio < 0.5 and unique_count >= 3
    
    def _analyze_data_quality(self) -> Dict[str, Any]:
        """Analyze overall data quality metrics."""
        # Count duplicate rows
        duplicate_count = self.df.duplicated().sum()
        
        # Calculate completeness score (average non-null percentage across columns)
        completeness_scores = []
        for col in self.df.columns:
            completeness = (1 - self.df[col].isnull().mean()) * 100
            completeness_scores.append(completeness)
        
        avg_completeness = np.mean(completeness_scores)
        
        # Identify potential issues
        issues = []
        
        # Check for columns with high null rates
        high_null_cols = [col for col in self.df.columns 
                         if self.df[col].isnull().mean() > 0.5]
        if high_null_cols:
            issues.append(f"High null rates in columns: {', '.join(high_null_cols)}")
        
        # Check for duplicate records
        if duplicate_count > 0:
            issues.append(f"Found {duplicate_count} duplicate records")
        
        # Check for columns with single values
        single_value_cols = [col for col in self.df.columns 
                           if self.df[col].nunique() <= 1]
        if single_value_cols:
            issues.append(f"Columns with single/no values: {', '.join(single_value_cols)}")
        
        return {
            "total_records": len(self.df),
            "duplicate_records": int(duplicate_count),
            "duplicate_percentage": round((duplicate_count / len(self.df)) * 100, 2),
            "completeness_score": round(avg_completeness, 2),
            "completeness_by_column": {col: round(score, 2) 
                                     for col, score in zip(self.df.columns, completeness_scores)},
            "potential_issues": issues
        }
    
    def _detect_relationships(self) -> Dict[str, Any]:
        """Detect potential relationships between columns."""
        potential_relationships = []
        normalization_opportunities = []
        
        # Find potential primary keys
        potential_pks = []
        for col in self.df.columns:
            col_data = self.df[col]
            if self._is_potential_id_field(col_data):
                potential_pks.append(col)
        
        # Find potential foreign key relationships
        categorical_cols = [col for col in self.df.columns 
                          if self._classify_pandas_type(self.df[col]) == "categorical"]
        
        for col in categorical_cols:
            if self._is_potential_foreign_key(self.df[col]):
                normalization_opportunities.append({
                    "column": col,
                    "suggested_table": f"{col.lower().replace('_', '')}_table",
                    "unique_values": int(self.df[col].nunique()),
                    "foreign_key_potential": "high"
                })
        
        return {
            "potential_primary_keys": potential_pks,
            "normalization_opportunities": normalization_opportunities,
            "total_categorical_columns": len(categorical_cols),
            "suggested_fact_table": "main_table"
        }
    
    def _assess_educational_value(self) -> Dict[str, Any]:
        """Assess the dataset's educational value for SQL learning."""
        # Count different column types
        type_counts = {}
        for col in self.df.columns:
            col_type = self._classify_pandas_type(self.df[col])
            type_counts[col_type] = type_counts.get(col_type, 0) + 1
        
        # Calculate suitability score (0-10)
        score = 5.0  # Base score
        
        # Add points for good characteristics
        if len(self.df) > 1000:  # Sufficient data size
            score += 1.0
        if type_counts.get("categorical", 0) >= 3:  # Multiple categorical columns for JOINs
            score += 1.5
        if type_counts.get("numeric", 0) >= 2:  # Numeric columns for aggregation
            score += 1.0
        if type_counts.get("datetime", 0) >= 1:  # Time-based analysis
            score += 0.5
        if self.analysis_results.get("data_quality", {}).get("completeness_score", 0) > 80:
            score += 1.0
        
        # Subtract points for issues
        if len(self.df) < 100:  # Too small
            score -= 2.0
        if self.analysis_results.get("data_quality", {}).get("completeness_score", 0) < 60:
            score -= 1.0
        
        score = max(0, min(10, score))  # Clamp to 0-10 range
        
        # Determine complexity level
        if len(self.df.columns) < 5:
            complexity = "beginner"
        elif len(self.df.columns) < 15:
            complexity = "intermediate"
        else:
            complexity = "advanced"
        
        # Recommend topics based on data characteristics
        recommended_topics = []
        if type_counts.get("categorical", 0) >= 2:
            recommended_topics.extend(["INNER JOIN", "LEFT JOIN", "GROUP BY"])
        if type_counts.get("numeric", 0) >= 1:
            recommended_topics.extend(["Aggregation functions", "Mathematical operations"])
        if type_counts.get("datetime", 0) >= 1:
            recommended_topics.extend(["Date functions", "Time-based analysis"])
        if len(self.analysis_results.get("relationships", {}).get("normalization_opportunities", [])) > 0:
            recommended_topics.append("Database normalization")
        
        return {
            "sql_suitability_score": round(score, 1),
            "complexity_level": complexity,
            "recommended_topics": recommended_topics,
            "column_type_distribution": type_counts,
            "strengths": self._identify_strengths(),
            "limitations": self._identify_limitations()
        }
    
    def _identify_strengths(self) -> List[str]:
        """Identify dataset strengths for SQL education."""
        strengths = []
        
        if len(self.df) > 10000:
            strengths.append("Large dataset size enables realistic query performance analysis")
        
        categorical_count = sum(1 for col in self.df.columns 
                              if self._classify_pandas_type(self.df[col]) == "categorical")
        if categorical_count >= 3:
            strengths.append("Multiple categorical columns enable complex JOIN exercises")
        
        if self.analysis_results.get("data_quality", {}).get("completeness_score", 0) > 85:
            strengths.append("High data quality with minimal missing values")
        
        if len(self.analysis_results.get("relationships", {}).get("normalization_opportunities", [])) > 2:
            strengths.append("Good normalization opportunities for database design practice")
        
        return strengths
    
    def _identify_limitations(self) -> List[str]:
        """Identify dataset limitations for SQL education."""
        limitations = []
        
        if len(self.df) < 1000:
            limitations.append("Small dataset size may not demonstrate query performance concepts")
        
        if self.analysis_results.get("data_quality", {}).get("completeness_score", 0) < 70:
            limitations.append("High missing data rates may complicate analysis")
        
        categorical_count = sum(1 for col in self.df.columns 
                              if self._classify_pandas_type(self.df[col]) == "categorical")
        if categorical_count < 2:
            limitations.append("Limited categorical columns reduce JOIN exercise opportunities")
        
        if len(self.df.columns) < 5:
            limitations.append("Few columns limit complexity of exercises")
        
        return limitations
    
    def save_analysis(self, output_path: str) -> bool:
        """
        Save analysis results to JSON file.
        
        Args:
            output_path: Path to save the analysis JSON
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Ensure results exist
            if not self.analysis_results:
                raise ValueError("No analysis results to save. Run analyze_dataset() first.")
            
            # Create output directory if needed
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            
            # Save with proper formatting
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(self.analysis_results, f, indent=2, ensure_ascii=False, default=str)
            
            print(f"💾 Analysis saved to: {output_path}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to save analysis: {e}")
            return False

    def create_database(self, database_path: str) -> bool:
        """
        Create a generic database from the dataset (dataset agnostic).
        
        Args:
            database_path: Path where to create the database
            
        Returns:
            bool: True if successful, False otherwise
        """
        if self.df is None:
            print("❌ Dataset not loaded. Cannot create database.")
            return False
        
        try:
            print(f"🗄️  Creating generic database: {database_path}")
            
            # Create directory if needed
            os.makedirs(os.path.dirname(database_path), exist_ok=True)
            
            # Connect to database
            conn = duckdb.connect(database_path)
            
            # Create a generic table name based on dataset
            dataset_name = self.dataset_name.split('/')[-1]
            table_name = dataset_name.replace('-', '_')
            
            # Drop existing table to ensure clean creation
            conn.execute(f"DROP TABLE IF EXISTS {table_name}")
            
            # Create a single table with all the raw data
            # This is dataset agnostic - works with any dataset structure
            conn.register('df_temp', self.df)
            conn.execute(f"CREATE TABLE {table_name} AS SELECT * FROM df_temp")
            
            # Get row count for summary
            result = conn.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()
            row_count = result[0] if result else 0
            
            conn.close()
            
            # Print summary
            print(f"📊 Database Summary:")
            print(f"   Table: {table_name}")
            print(f"   Records: {row_count:,}")
            print(f"   Columns: {len(self.df.columns):,}")
            
            print(f"✅ Database created successfully: {database_path}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to create database: {e}")
            return False


def main():
    """Main function for command-line usage."""
    parser = argparse.ArgumentParser(
        description="Explore HuggingFace datasets for SQL curriculum development"
    )
    parser.add_argument(
        "--dataset", 
        required=True, 
        help="HuggingFace dataset identifier (e.g., 'lukebarousse/data_jobs')"
    )
    parser.add_argument(
        "--split", 
        default="train", 
        help="Dataset split to analyze (default: 'train')"
    )
    parser.add_argument(
        "--output", 
        help="Output JSON file path (default: initial_exploration_<dataset_name>.json in project's scripts/data_schema_generation/)"
    )
    parser.add_argument(
        "--sample-size", 
        type=int, 
        default=1000, 
        help="Number of sample values per column (default: 1000)"
    )
    parser.add_argument(
        "--create-database", 
        action="store_true", 
        help="Create generic database from the dataset (dataset agnostic)"
    )
    
    args = parser.parse_args()
    
    # Set default output path if not provided
    if not args.output:
        dataset_name = args.dataset.split('/')[-1]
        # Always use absolute path relative to project root, not current working directory
        project_root = Path(__file__).parent.parent.parent
        args.output = str(project_root / "scripts" / "data_schema_generation" / f"initial_exploration_{dataset_name}.json")
    
    # Create explorer and run analysis
    explorer = DatasetExplorer(args.dataset, args.split, args.sample_size)
    
    # Load dataset
    if not explorer.load_dataset():
        sys.exit(1)
    
    # Run analysis
    try:
        results = explorer.analyze_dataset()
        print(f"\n📋 Analysis Summary:")
        print(f"   Dataset: {results['metadata']['dataset_name']}")
        print(f"   Records: {results['metadata']['total_records']:,}")
        print(f"   Columns: {results['metadata']['total_columns']}")
        print(f"   SQL Suitability: {results['educational_assessment']['sql_suitability_score']}/10")
        print(f"   Complexity: {results['educational_assessment']['complexity_level']}")
        print(f"   Data Quality: {results['data_quality']['completeness_score']:.1f}%")
        
    except Exception as e:
        print(f"❌ Analysis failed: {e}")
        sys.exit(1)
    
    # Save results
    if not explorer.save_analysis(args.output):
        sys.exit(1)
    
    # Create database if requested
    if args.create_database:
        dataset_name = args.dataset.split('/')[-1]
        db_path = f"../../datasets/{dataset_name}.db"
        if not explorer.create_database(db_path):
            sys.exit(1)
    
    print(f"\n✅ Dataset exploration completed successfully!")


if __name__ == "__main__":
    main() 