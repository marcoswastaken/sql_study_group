#!/usr/bin/env python3
"""
Tests for the dataset exploration script.

These tests verify that the dataset explorer works correctly with:
- Real HuggingFace datasets
- Mock datasets with different characteristics
- Edge cases and error conditions
- JSON output validity and completeness
"""

import json
import os
import sys
import tempfile
import unittest
from unittest.mock import patch

import numpy as np
import pandas as pd

from scripts.core.explore_dataset import DatasetExplorer


class TestDatasetExplorer(unittest.TestCase):
    """Test cases for the DatasetExplorer class."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Clean up test fixtures."""
        import shutil

        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def create_mock_dataset(self, data_dict: dict) -> pd.DataFrame:
        """Create a mock dataset for testing."""
        return pd.DataFrame(data_dict)

    def test_simple_dataset_analysis(self):
        """Test analysis of a simple dataset with various column types."""
        # Create mock dataset
        mock_data = {
            "id": range(1, 101),
            "category": ["A", "B", "C"] * 33 + ["A"],
            "value": np.random.normal(100, 15, 100),
            "date": pd.date_range("2023-01-01", periods=100),
            "text": [f"item_{i}" for i in range(100)],
            "flag": [True, False] * 50,
        }

        explorer = DatasetExplorer("test/dataset")
        explorer.df = self.create_mock_dataset(mock_data)

        # Run analysis
        results = explorer.analyze_dataset()

        # Verify structure
        self.assertIn("metadata", results)
        self.assertIn("columns", results)
        self.assertIn("data_quality", results)
        self.assertIn("relationships", results)
        self.assertIn("educational_assessment", results)

        # Verify metadata
        metadata = results["metadata"]
        self.assertEqual(metadata["total_records"], 100)
        self.assertEqual(metadata["total_columns"], 6)
        self.assertEqual(metadata["dataset_name"], "dataset")

        # Verify column analysis
        columns = results["columns"]
        self.assertEqual(len(columns), 6)

        # Check specific column types
        column_names = [col["name"] for col in columns]
        self.assertIn("id", column_names)
        self.assertIn("category", column_names)
        self.assertIn("value", column_names)

        # Verify data quality metrics
        data_quality = results["data_quality"]
        self.assertIn("completeness_score", data_quality)
        self.assertIn("duplicate_records", data_quality)
        self.assertGreaterEqual(data_quality["completeness_score"], 0)
        self.assertLessEqual(data_quality["completeness_score"], 100)

    def test_column_type_classification(self):
        """Test column type classification for different data types."""
        mock_data = {
            "integer_col": [1, 2, 3, 4, 5] * 20,  # 100 items
            "float_col": [1.1, 2.2, 3.3, 4.4, 5.5] * 20,  # 100 items
            "categorical_col": ["A", "A", "B", "B", "C"]
            * 20,  # 100 items, 3 unique (3% unique)
            "text_col": [
                f"unique_text_{i}" for i in range(100)
            ],  # 100 unique items (100% unique)
            "datetime_col": pd.date_range("2023-01-01", periods=100),  # 100 items
            "boolean_col": [True, False, True, False, True] * 20,  # 100 items
        }

        explorer = DatasetExplorer("test/types")
        explorer.df = self.create_mock_dataset(mock_data)

        results = explorer.analyze_dataset()
        columns = {col["name"]: col for col in results["columns"]}

        # Test type classifications
        self.assertEqual(columns["integer_col"]["pandas_type"], "numeric")
        self.assertEqual(columns["float_col"]["pandas_type"], "numeric")
        self.assertEqual(columns["categorical_col"]["pandas_type"], "categorical")
        self.assertEqual(columns["text_col"]["pandas_type"], "text")
        self.assertEqual(columns["datetime_col"]["pandas_type"], "datetime")
        self.assertEqual(columns["boolean_col"]["pandas_type"], "boolean")

    def test_potential_id_field_detection(self):
        """Test detection of potential ID fields."""
        mock_data = {
            "sequential_id": range(1, 101),  # Should be detected as ID
            "random_unique": np.random.choice(
                range(1000, 2000), 100, replace=False
            ),  # Should be detected as ID
            "non_unique": [1, 2, 3] * 33 + [1],  # Should NOT be detected as ID
            "negative_nums": range(
                -50, 50
            ),  # Should NOT be detected as ID (has negatives)
        }

        explorer = DatasetExplorer("test/ids")
        explorer.df = self.create_mock_dataset(mock_data)

        results = explorer.analyze_dataset()
        columns = {col["name"]: col for col in results["columns"]}

        # Test ID field detection
        self.assertTrue(columns["sequential_id"].get("potential_id_field", False))
        self.assertTrue(columns["random_unique"].get("potential_id_field", False))
        self.assertFalse(columns["non_unique"].get("potential_id_field", False))
        self.assertFalse(columns["negative_nums"].get("potential_id_field", False))

    def test_foreign_key_detection(self):
        """Test detection of potential foreign key fields."""
        # Create dataset with foreign key-like column
        company_names = [
            "Company_A",
            "Company_B",
            "Company_C",
            "Company_D",
            "Company_E",
        ]
        mock_data = {
            "id": range(1, 1001),
            "company": np.random.choice(company_names, 1000),  # Should be FK candidate
            "unique_field": [f"unique_{i}" for i in range(1000)],  # Should NOT be FK
            "too_few_categories": ["X", "Y"]
            * 500,  # Should NOT be FK (too few categories)
        }

        explorer = DatasetExplorer("test/fks")
        explorer.df = self.create_mock_dataset(mock_data)

        results = explorer.analyze_dataset()
        columns = {col["name"]: col for col in results["columns"]}

        # Test FK detection
        self.assertTrue(columns["company"].get("potential_foreign_key", False))
        self.assertFalse(columns["unique_field"].get("potential_foreign_key", False))
        self.assertFalse(
            columns["too_few_categories"].get("potential_foreign_key", False)
        )

    def test_data_quality_analysis(self):
        """Test data quality metrics calculation."""
        # Create dataset with known quality issues
        mock_data = {
            "perfect_col": range(100),
            "half_null_col": [i if i % 2 == 0 else None for i in range(100)],
            "mostly_null_col": [i if i < 10 else None for i in range(100)],
            "duplicate_values": [1, 2, 3] * 33 + [1],
        }

        # Add duplicate rows
        df = self.create_mock_dataset(mock_data)
        df_with_dupes = pd.concat([df, df.head(10)], ignore_index=True)

        explorer = DatasetExplorer("test/quality")
        explorer.df = df_with_dupes

        results = explorer.analyze_dataset()
        data_quality = results["data_quality"]

        # Test quality metrics
        self.assertEqual(data_quality["duplicate_records"], 10)
        self.assertLess(
            data_quality["completeness_score"], 100
        )  # Should be less than 100% due to nulls
        self.assertIn("High null rates", " ".join(data_quality["potential_issues"]))

    def test_educational_assessment(self):
        """Test educational value assessment."""
        # Create dataset with good characteristics for SQL learning
        mock_data = {
            "id": range(1, 1001),
            "category1": np.random.choice(["A", "B", "C"], 1000),
            "category2": np.random.choice(["X", "Y", "Z"], 1000),
            "category3": np.random.choice(["P", "Q", "R"], 1000),
            "numeric1": np.random.normal(100, 15, 1000),
            "numeric2": np.random.randint(1, 100, 1000),
            "date_col": pd.date_range("2023-01-01", periods=1000),
            "text_col": [f"text_{i}" for i in range(1000)],
        }

        explorer = DatasetExplorer("test/educational")
        explorer.df = self.create_mock_dataset(mock_data)

        results = explorer.analyze_dataset()
        assessment = results["educational_assessment"]

        # Test assessment components
        self.assertIn("sql_suitability_score", assessment)
        self.assertIn("complexity_level", assessment)
        self.assertIn("recommended_topics", assessment)
        self.assertIn("column_type_distribution", assessment)

        # Should score well due to multiple categoricals, numerics, and good size
        self.assertGreaterEqual(assessment["sql_suitability_score"], 7.0)

        # Should recommend JOIN operations due to multiple categorical columns
        self.assertIn("INNER JOIN", assessment["recommended_topics"])

    def test_normalization_opportunities(self):
        """Test detection of normalization opportunities."""
        # Create dataset with clear normalization opportunities
        companies = ["Apple", "Google", "Microsoft"] * 100
        locations = ["NYC", "SF", "Seattle"] * 100

        mock_data = {
            "id": range(1, 301),
            "company": companies,
            "location": locations,
            "salary": np.random.randint(50000, 150000, 300),
            "employee_name": [f"Employee_{i}" for i in range(300)],
        }

        explorer = DatasetExplorer("test/normalization")
        explorer.df = self.create_mock_dataset(mock_data)

        results = explorer.analyze_dataset()
        relationships = results["relationships"]

        # Should detect normalization opportunities
        self.assertGreater(len(relationships["normalization_opportunities"]), 0)

        # Should suggest tables for categorical columns
        suggested_tables = [
            opp["suggested_table"]
            for opp in relationships["normalization_opportunities"]
        ]
        self.assertTrue(any("company" in table for table in suggested_tables))

    def test_empty_dataset_handling(self):
        """Test handling of empty datasets."""
        explorer = DatasetExplorer("test/empty")
        explorer.df = pd.DataFrame()

        # Should handle empty dataset gracefully
        with self.assertRaises(ValueError):
            explorer.analyze_dataset()

    def test_single_column_dataset(self):
        """Test handling of single-column datasets."""
        mock_data = {"single_col": range(100)}

        explorer = DatasetExplorer("test/single")
        explorer.df = self.create_mock_dataset(mock_data)

        results = explorer.analyze_dataset()

        # Should complete analysis but indicate limitations
        self.assertEqual(len(results["columns"]), 1)
        assessment = results["educational_assessment"]
        self.assertIn(
            "Few columns limit complexity", " ".join(assessment["limitations"])
        )

    def test_all_null_column(self):
        """Test handling of columns with all null values."""
        mock_data = {"normal_col": range(100), "all_null_col": [None] * 100}

        explorer = DatasetExplorer("test/nulls")
        explorer.df = self.create_mock_dataset(mock_data)

        results = explorer.analyze_dataset()
        columns = {col["name"]: col for col in results["columns"]}

        # Should handle all-null column
        self.assertEqual(columns["all_null_col"]["null_percentage"], 100.0)
        self.assertEqual(
            columns["all_null_col"]["sample_values"], ["(all null values)"]
        )

    def test_json_output_validity(self):
        """Test that the output JSON is valid and complete."""
        mock_data = {
            "id": range(50),
            "category": ["A", "B"] * 25,
            "value": np.random.normal(100, 15, 50),
        }

        explorer = DatasetExplorer("test/json")
        explorer.df = self.create_mock_dataset(mock_data)

        results = explorer.analyze_dataset()

        # Test JSON serialization
        output_path = os.path.join(self.temp_dir, "test_output.json")
        success = explorer.save_analysis(output_path)
        self.assertTrue(success)

        # Verify file was created and is valid JSON
        self.assertTrue(os.path.exists(output_path))

        with open(output_path) as f:
            loaded_results = json.load(f)

        # Verify structure is preserved
        self.assertEqual(loaded_results.keys(), results.keys())
        self.assertEqual(loaded_results["metadata"]["total_records"], 50)

    def test_sample_values_extraction(self):
        """Test sample value extraction for different column types."""
        mock_data = {
            "short_categories": ["A", "B", "C"] * 34,  # Few unique values (102 items)
            "many_categories": [
                f"cat_{i}" for i in range(102)
            ],  # Many unique values (102 items)
            "long_text": [
                "This is a very long text that should be truncated because it exceeds the limit"
            ]
            * 102,  # 102 items
        }

        explorer = DatasetExplorer("test/samples")
        explorer.df = self.create_mock_dataset(mock_data)

        results = explorer.analyze_dataset()
        columns = {col["name"]: col for col in results["columns"]}

        # Should include all values for short categories
        self.assertEqual(len(columns["short_categories"]["sample_values"]), 3)

        # Should limit samples for many categories
        self.assertLessEqual(len(columns["many_categories"]["sample_values"]), 5)

        # Should truncate long text
        for sample in columns["long_text"]["sample_values"]:
            self.assertLessEqual(len(sample), 53)  # 50 chars + "..."

    @patch("core.explore_dataset.load_dataset")
    def test_dataset_loading_error(self, mock_load_dataset):
        """Test error handling when dataset loading fails."""
        mock_load_dataset.side_effect = Exception("Dataset not found")

        explorer = DatasetExplorer("nonexistent/dataset")
        success = explorer.load_dataset()

        self.assertFalse(success)
        self.assertIsNone(explorer.df)


class TestDatasetExplorerIntegration(unittest.TestCase):
    """Integration tests with real datasets (if available)."""

    def test_with_small_real_dataset(self):
        """Test with a small real dataset if available."""
        # This test only runs if we can access a real dataset
        try:
            explorer = DatasetExplorer("lukebarousse/data_jobs")

            # Try to load a small sample
            success = explorer.load_dataset()

            if success and explorer.df is not None:
                # Limit to first 1000 rows for speed
                explorer.df = explorer.df.head(1000)

                results = explorer.analyze_dataset()

                # Basic validation of real dataset analysis
                self.assertIn("metadata", results)
                self.assertGreater(results["metadata"]["total_records"], 0)
                self.assertGreater(results["metadata"]["total_columns"], 0)

                # Should work with real data structure
                self.assertIn("educational_assessment", results)
                self.assertIsInstance(
                    results["educational_assessment"]["sql_suitability_score"],
                    (int, float),
                )

                print("✅ Real dataset test passed:")
                print(f"   Records: {results['metadata']['total_records']:,}")
                print(f"   Columns: {results['metadata']['total_columns']}")
                print(
                    f"   SQL Score: {results['educational_assessment']['sql_suitability_score']}/10"
                )

        except Exception as e:
            self.skipTest(f"Real dataset test skipped: {e}")


def run_comprehensive_tests():
    """Run all tests and provide summary."""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add test cases
    suite.addTests(loader.loadTestsFromTestCase(TestDatasetExplorer))
    suite.addTests(loader.loadTestsFromTestCase(TestDatasetExplorerIntegration))

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Print summary
    print(f"\n{'='*60}")
    print("🧪 TEST SUMMARY")
    print(f"{'='*60}")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")

    if result.failures:
        print("\n❌ FAILURES:")
        for test, traceback in result.failures:
            print(f"  {test}: {traceback}")

    if result.errors:
        print("\n❌ ERRORS:")
        for test, traceback in result.errors:
            print(f"  {test}: {traceback}")

    if result.wasSuccessful():
        print("\n✅ All tests passed!")
        return True
    else:
        print("\n❌ Some tests failed!")
        return False


if __name__ == "__main__":
    success = run_comprehensive_tests()
    sys.exit(0 if success else 1)
