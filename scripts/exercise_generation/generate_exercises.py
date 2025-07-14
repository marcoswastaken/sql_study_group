#!/usr/bin/env python3
"""
Generic Exercise Generation Script

Generates SQL exercises based on:
- Week topics from syllabus schema
- Table structure from data schema
- Educational requirements for progressive difficulty

Usage:
    python generate_exercises.py --week 4 --dataset data_jobs
"""

import argparse
import json
from datetime import datetime
from pathlib import Path


def load_syllabus_schema():
    """Load syllabus schema to get week-specific topics"""
    syllabus_path = Path("../asset_generation/syllabus_schema.json")
    with open(syllabus_path) as f:
        return json.load(f)


def load_data_schema(dataset):
    """Load data schema to understand table structure"""
    schema_path = Path(f"../../schemas/data_schema_{dataset}.json")
    with open(schema_path) as f:
        return json.load(f)


def get_week_info(syllabus, week_num):
    """Extract information for specific week"""
    for week in syllabus["weeks"]:
        if week["number"] == week_num:
            return week
    return None


def generate_week_4_exercises(schema_info, week_info):
    """Generate Week 4 specific exercises focusing on JOIN operations"""

    exercises = []

    # Exercise 1: Basic INNER JOIN - Companies and Job Postings
    exercises.append(
        {
            "id": 1,
            "title": "Company Job Postings",
            "statement": "Find all Data Scientist job postings along with company names. Show the job title, company name, and posted date. Use INNER JOIN to only show jobs that have company information.",
            "solution": """SELECT jp.job_title, c.company_name, jp.job_posted_date
FROM job_postings AS jp
INNER JOIN companies AS c ON jp.company_name = c.company_name
WHERE jp.job_title_short = 'Data Scientist'
ORDER BY jp.job_posted_date DESC
LIMIT 10;""",
            "topics": ["INNER JOIN", "Table aliases", "WHERE clause", "ORDER BY"],
            "difficulty": "Easy",
            "educational_focus": "Basic INNER JOIN syntax with table aliases",
        }
    )

    # Exercise 2: LEFT JOIN - All companies with job counts
    exercises.append(
        {
            "id": 2,
            "title": "All Companies with Job Counts",
            "statement": "List all companies and count how many job postings they have. Include companies even if they don't have any job postings in the job_postings table (show 0 for them). Use LEFT JOIN to ensure all companies are included.",
            "solution": """SELECT c.company_name, COUNT(jp.job_id) AS job_count
FROM companies AS c
LEFT JOIN job_postings AS jp ON c.company_name = jp.company_name
GROUP BY c.company_name
ORDER BY job_count DESC
LIMIT 20;""",
            "topics": ["LEFT JOIN", "COUNT", "GROUP BY", "Table aliases"],
            "difficulty": "Medium",
            "educational_focus": "LEFT JOIN to include all records from left table, handling NULLs",
        }
    )

    # Exercise 3: Platform Analysis with INNER JOIN
    exercises.append(
        {
            "id": 3,
            "title": "Platform Job Distribution",
            "statement": "Show which job platforms are posting the most Data Engineer jobs. Include platform name and job count. Use INNER JOIN to connect job postings with platforms.",
            "solution": """SELECT jpl.platform_name, COUNT(jp.job_id) AS job_count
FROM job_platforms AS jpl
INNER JOIN job_postings AS jp ON jpl.platform_name = jp.job_via
WHERE jp.job_title_short = 'Data Engineer'
GROUP BY jpl.platform_name
ORDER BY job_count DESC
LIMIT 10;""",
            "topics": ["INNER JOIN", "COUNT", "GROUP BY", "WHERE clause"],
            "difficulty": "Medium",
            "educational_focus": "INNER JOIN with aggregation and filtering",
        }
    )

    # Exercise 4: Geographic Analysis with LEFT JOIN
    exercises.append(
        {
            "id": 4,
            "title": "Jobs by Location",
            "statement": "List all job postings with their location details. Show job title, location, and country. Use LEFT JOIN to include jobs even if location information is missing.",
            "solution": """SELECT jp.job_title_short, jp.job_location, l.job_country
FROM job_postings AS jp
LEFT JOIN locations AS l ON jp.job_location = l.job_location
WHERE jp.job_title_short IN ('Data Scientist', 'Data Engineer', 'Data Analyst')
ORDER BY l.job_country, jp.job_location
LIMIT 15;""",
            "topics": ["LEFT JOIN", "WHERE IN", "ORDER BY", "Table aliases"],
            "difficulty": "Medium",
            "educational_focus": "LEFT JOIN with multiple column sorting and filtering",
        }
    )

    # Exercise 5: Salary Range Analysis with conditional JOIN
    exercises.append(
        {
            "id": 5,
            "title": "Salary Range Classification",
            "statement": "Classify Data Scientist jobs by salary ranges. Show job title, salary, and experience level. Use a conditional JOIN to match salaries with appropriate ranges.",
            "solution": """SELECT jp.job_title, jp.salary_year_avg, sr.range_name, sr.experience_level
FROM job_postings AS jp
INNER JOIN salary_ranges AS sr ON jp.salary_year_avg BETWEEN sr.min_salary AND sr.max_salary
WHERE jp.job_title_short = 'Data Scientist'
  AND jp.salary_year_avg IS NOT NULL
ORDER BY jp.salary_year_avg DESC
LIMIT 10;""",
            "topics": ["INNER JOIN", "BETWEEN", "IS NOT NULL", "Table aliases"],
            "difficulty": "Hard",
            "educational_focus": "Conditional JOIN using BETWEEN clause",
        }
    )

    # Exercise 6: Multiple JOINs
    exercises.append(
        {
            "id": 6,
            "title": "Comprehensive Job Analysis",
            "statement": "Create a comprehensive report showing job title, company name, location, country, and platform for Data Analyst positions. Use multiple JOINs to combine information from different tables.",
            "solution": """SELECT jp.job_title, c.company_name, jp.job_location, l.job_country, jp.job_via
FROM job_postings AS jp
INNER JOIN companies AS c ON jp.company_name = c.company_name
LEFT JOIN locations AS l ON jp.job_location = l.job_location
WHERE jp.job_title_short = 'Data Analyst'
  AND jp.job_location IS NOT NULL
ORDER BY l.job_country, jp.job_location
LIMIT 12;""",
            "topics": ["Multiple JOINs", "INNER JOIN", "LEFT JOIN", "WHERE clause"],
            "difficulty": "Hard",
            "educational_focus": "Combining multiple JOIN types in a single query",
        }
    )

    # Exercise 7: Foreign Key Relationships
    exercises.append(
        {
            "id": 7,
            "title": "Platform Performance Analysis",
            "statement": "Compare platform performance by showing platform name, total jobs posted, and average jobs per platform. Use PRIMARY KEY and FOREIGN KEY concepts through JOINs.",
            "solution": """SELECT jpl.platform_name, jpl.jobs_posted, COUNT(jp.job_id) AS actual_jobs
FROM job_platforms AS jpl
LEFT JOIN job_postings AS jp ON jpl.platform_name = jp.job_via
GROUP BY jpl.platform_name, jpl.jobs_posted
HAVING COUNT(jp.job_id) > 100
ORDER BY actual_jobs DESC
LIMIT 15;""",
            "topics": ["LEFT JOIN", "GROUP BY", "HAVING", "COUNT"],
            "difficulty": "Hard",
            "educational_focus": "Understanding primary/foreign key relationships through JOINs",
        }
    )

    # Exercise 8: Remote Work Analysis
    exercises.append(
        {
            "id": 8,
            "title": "Remote Work by Company",
            "statement": "Analyze remote work opportunities by company. Show company name, total jobs, and count of remote jobs. Include companies even if they don't offer remote work.",
            "solution": """SELECT c.company_name,
       COUNT(jp.job_id) AS total_jobs,
       COUNT(CASE WHEN jp.job_work_from_home = 'True' THEN 1 END) AS remote_jobs
FROM companies AS c
LEFT JOIN job_postings AS jp ON c.company_name = jp.company_name
GROUP BY c.company_name
HAVING COUNT(jp.job_id) > 5
ORDER BY remote_jobs DESC
LIMIT 10;""",
            "topics": ["LEFT JOIN", "COUNT", "CASE WHEN", "GROUP BY", "HAVING"],
            "difficulty": "Hard",
            "educational_focus": "LEFT JOIN with conditional aggregation",
        }
    )

    return exercises


def generate_exercise_key(dataset, week_num, exercises):
    """Generate the complete exercise key structure"""
    return {
        "metadata": {
            "title": f"Week {week_num} Practice - {dataset.replace('_', ' ').title()} Dataset",
            "description": "JOIN operations on real-world data job postings",
            "week": week_num,
            "total_exercises": len(exercises),
            "database": f"{dataset}.db",
            "focus_topics": [
                "INNER JOIN",
                "LEFT JOIN",
                "Table aliases",
                "Primary/Foreign keys",
            ],
            "generated_date": datetime.now().isoformat(),
            "difficulty_levels": ["Easy", "Medium", "Hard"],
        },
        "exercises": exercises,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Generate SQL exercises for a specific week"
    )
    parser.add_argument("--week", type=int, required=True, help="Week number (e.g., 4)")
    parser.add_argument(
        "--dataset", type=str, required=True, help="Dataset name (e.g., data_jobs)"
    )
    parser.add_argument("--output", type=str, help="Output file path (optional)")

    args = parser.parse_args()

    # Load schemas
    syllabus = load_syllabus_schema()
    schema_info = load_data_schema(args.dataset)

    # Get week information
    week_info = get_week_info(syllabus, args.week)
    if not week_info:
        print(f"❌ Week {args.week} not found in syllabus")
        return

    print(f"📚 Generating exercises for Week {args.week}: {week_info['title']}")
    print(f"🎯 Core concepts: {', '.join(week_info['core_concepts'])}")

    # Generate exercises based on week
    if args.week == 4:
        exercises = generate_week_4_exercises(schema_info, week_info)
    else:
        print(f"❌ Exercise generation not implemented for Week {args.week}")
        return

    # Generate complete exercise key
    exercise_key = generate_exercise_key(args.dataset, args.week, exercises)

    # Output file
    if args.output:
        output_path = Path(args.output)
    else:
        output_path = Path(f"../../exercises/week_{args.week}_key.json")

    # Write to file
    with open(output_path, "w") as f:
        json.dump(exercise_key, f, indent=2)

    print(f"✅ Generated {len(exercises)} exercises")
    print(f"📁 Output: {output_path}")
    print(
        f"🎯 Topics covered: {', '.join({topic for ex in exercises for topic in ex['topics']})}"
    )


if __name__ == "__main__":
    main()
