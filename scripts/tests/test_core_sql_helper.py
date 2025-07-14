#!/usr/bin/env python3
"""
Comprehensive test script for SQL helper function.
Tests actual queries from week 4 practice solutions to ensure everything works correctly.
"""

import traceback

from scripts.core.sql_helper import SQLHelper


def test_query(helper, query_name, query, expected_min_rows=0, expected_columns=None):
    """Test a single query and report results."""
    print(f"\n{'='*80}")
    print(f"🧪 Testing: {query_name}")
    print(f"{'='*80}")

    try:
        result = helper.execute_query(query)

        if result["status"] == "success":
            print(f"✅ Query executed successfully in {result['execution_time']}s")
            print(
                f"📊 Returned {result['row_count']} rows, {len(result['columns'])} columns"
            )
            print(f"📋 Columns: {', '.join(result['columns'])}")

            # Check expectations
            if result["row_count"] >= expected_min_rows:
                print(f"✅ Row count check passed (>= {expected_min_rows})")
            else:
                print(
                    f"⚠️  Row count lower than expected (got {result['row_count']}, expected >= {expected_min_rows})"
                )

            if expected_columns and set(expected_columns).issubset(
                set(result["columns"])
            ):
                print("✅ Column check passed")
            elif expected_columns:
                print(
                    f"⚠️  Missing expected columns: {set(expected_columns) - set(result['columns'])}"
                )

            # Show sample data
            if result["data"] is not None and not result["data"].empty:
                print("\n📋 Sample Results (first 3 rows):")
                print(result["data"].head(3).to_string(index=False))

        else:
            print(f"❌ Query failed: {result['error']}")
            print(f"   Error type: {result.get('error_type', 'Unknown')}")

    except Exception as e:
        print(f"❌ Test failed with exception: {e}")
        traceback.print_exc()


def main():
    """Run comprehensive tests on SQL helper function."""
    print("🧪 COMPREHENSIVE SQL HELPER TESTING")
    print("=" * 80)

    # Initialize helper
    try:
        helper = SQLHelper("datasets/data_jobs.db")
        print("✅ SQL Helper initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize SQL Helper: {e}")
        return

    # Test 1: Basic schema exploration
    print("\n🔍 SCHEMA EXPLORATION TESTS")

    test_query(
        helper,
        "Show Tables",
        "SHOW TABLES",
        expected_min_rows=5,
        expected_columns=["name"],
    )

    test_query(
        helper,
        "Describe Jobs Table",
        "DESCRIBE jobs",
        expected_min_rows=10,
        expected_columns=["column_name", "column_type"],
    )

    # Test 2: Basic JOIN queries from solutions
    print("\n🔗 BASIC JOIN TESTS")

    test_query(
        helper,
        "Solution 1: Data Scientist Jobs",
        """
        SELECT c.company_name, j.job_title, j.job_posted_date
        FROM companies AS c
        INNER JOIN jobs AS j ON c.company_id = j.company_id
        WHERE j.job_title_short = 'Data Scientist'
        ORDER BY j.job_posted_date DESC
        LIMIT 10
        """,
        expected_min_rows=1,
        expected_columns=["company_name", "job_title", "job_posted_date"],
    )

    test_query(
        helper,
        "Solution 2: Jobs by Location",
        """
        SELECT j.job_title_short, l.job_location, l.job_country
        FROM jobs AS j
        INNER JOIN locations AS l ON j.location_id = l.location_id
        ORDER BY l.job_country, l.job_location
        LIMIT 10
        """,
        expected_min_rows=5,
        expected_columns=["job_title_short", "job_location", "job_country"],
    )

    test_query(
        helper,
        "Solution 3: Platform Analytics",
        """
        SELECT p.platform_name, COUNT(j.job_id) AS job_count
        FROM platforms AS p
        INNER JOIN jobs AS j ON p.platform_id = j.platform_id
        WHERE j.job_title_short = 'Data Engineer'
        GROUP BY p.platform_name
        ORDER BY job_count DESC
        """,
        expected_min_rows=1,
        expected_columns=["platform_name", "job_count"],
    )

    # Test 3: LEFT JOIN queries
    print("\n⬅️ LEFT JOIN TESTS")

    test_query(
        helper,
        "Solution 4: All Companies with Job Counts",
        """
        SELECT c.company_name, COUNT(j.job_id) AS job_count
        FROM companies AS c
        LEFT JOIN jobs AS j ON c.company_id = j.company_id
        GROUP BY c.company_name
        ORDER BY job_count DESC
        LIMIT 10
        """,
        expected_min_rows=10,
        expected_columns=["company_name", "job_count"],
    )

    # Test 4: Advanced multi-table JOINs
    print("\n🔗 ADVANCED JOIN TESTS")

    test_query(
        helper,
        "Solution 6: Skills in Demand",
        """
        SELECT s.skill_name, s.skill_category, COUNT(js.job_id) AS demand_count
        FROM skills AS s
        INNER JOIN job_skills AS js ON s.skill_id = js.skill_id
        INNER JOIN jobs AS j ON js.job_id = j.job_id
        WHERE j.job_title_short = 'Data Analyst'
        GROUP BY s.skill_name, s.skill_category
        ORDER BY demand_count DESC
        LIMIT 10
        """,
        expected_min_rows=5,
        expected_columns=["skill_name", "skill_category", "demand_count"],
    )

    test_query(
        helper,
        "Solution 7: High-Paying Companies",
        """
        SELECT c.company_name,
               AVG(j.salary_year_avg) AS avg_salary,
               COUNT(j.job_id) AS job_count
        FROM companies AS c
        INNER JOIN jobs AS j ON c.company_id = j.company_id
        WHERE j.job_title_short = 'Data Engineer'
          AND j.salary_year_avg > 100000
        GROUP BY c.company_name
        ORDER BY avg_salary DESC
        LIMIT 10
        """,
        expected_min_rows=1,
        expected_columns=["company_name", "avg_salary", "job_count"],
    )

    test_query(
        helper,
        "Solution 8: Geographic Salary Analysis",
        """
        SELECT l.job_country,
               AVG(j.salary_year_avg) AS avg_salary,
               COUNT(j.job_id) AS job_count
        FROM locations AS l
        INNER JOIN jobs AS j ON l.location_id = j.location_id
        WHERE j.job_title_short = 'Data Scientist'
          AND j.salary_year_avg IS NOT NULL
        GROUP BY l.job_country
        HAVING COUNT(j.job_id) >= 5
        ORDER BY avg_salary DESC
        """,
        expected_min_rows=1,
        expected_columns=["job_country", "avg_salary", "job_count"],
    )

    # Test 5: Complex queries with CTEs
    print("\n🧩 COMPLEX QUERY TESTS")

    test_query(
        helper,
        "Solution 9: Tech Stack Analysis (CTE)",
        """
        WITH skill_counts AS (
            SELECT c.company_name,
                   s.skill_category,
                   COUNT(s.skill_id) AS category_count,
                   ROW_NUMBER() OVER (PARTITION BY c.company_name ORDER BY COUNT(s.skill_id) DESC) AS rn
            FROM companies AS c
            INNER JOIN jobs AS j ON c.company_id = j.company_id
            INNER JOIN job_skills AS js ON j.job_id = js.job_id
            INNER JOIN skills AS s ON js.skill_id = s.skill_id
            WHERE j.job_title_short = 'Data Engineer'
            GROUP BY c.company_name, s.skill_category
        )
        SELECT company_name, skill_category AS most_common_skill_category, category_count AS skill_count
        FROM skill_counts
        WHERE rn = 1
        ORDER BY skill_count DESC
        LIMIT 10
        """,
        expected_min_rows=1,
        expected_columns=["company_name", "most_common_skill_category", "skill_count"],
    )

    # Test 6: Error handling
    print("\n❌ ERROR HANDLING TESTS")

    test_query(
        helper,
        "Invalid Column Name",
        """
        SELECT invalid_column_name
        FROM jobs
        LIMIT 5
        """,
        expected_min_rows=0,
    )

    test_query(
        helper,
        "Invalid Table Name",
        """
        SELECT *
        FROM nonexistent_table
        LIMIT 5
        """,
        expected_min_rows=0,
    )

    test_query(
        helper,
        "SQL Syntax Error",
        """
        SELECT *
        FROM jobs
        WHERE
        """,
        expected_min_rows=0,
    )

    # Test 7: Performance with large results
    print("\n🚀 PERFORMANCE TESTS")

    test_query(
        helper,
        "Large Result Set",
        """
        SELECT job_title_short, COUNT(*) as count
        FROM jobs
        GROUP BY job_title_short
        ORDER BY count DESC
        """,
        expected_min_rows=5,
        expected_columns=["job_title_short", "count"],
    )

    # Test 8: Data validation
    print("\n✅ DATA VALIDATION TESTS")

    test_query(
        helper,
        "Record Count Validation",
        """
        SELECT COUNT(*) as total_jobs
        FROM jobs
        """,
        expected_min_rows=1,
        expected_columns=["total_jobs"],
    )

    test_query(
        helper,
        "Foreign Key Integrity",
        """
        SELECT
            (SELECT COUNT(*) FROM jobs WHERE company_id NOT IN (SELECT company_id FROM companies)) as orphaned_jobs,
            (SELECT COUNT(*) FROM jobs WHERE location_id NOT IN (SELECT location_id FROM locations)) as orphaned_locations,
            (SELECT COUNT(*) FROM jobs WHERE platform_id NOT IN (SELECT platform_id FROM platforms)) as orphaned_platforms
        """,
        expected_min_rows=1,
        expected_columns=["orphaned_jobs", "orphaned_locations", "orphaned_platforms"],
    )

    # Close connection
    helper.close()

    print("\n" + "=" * 80)
    print("🎉 COMPREHENSIVE TESTING COMPLETE!")
    print("=" * 80)
    print("\nIf all tests passed, the SQL helper function is ready for use!")


if __name__ == "__main__":
    main()
