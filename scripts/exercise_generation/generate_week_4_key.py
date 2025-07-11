#!/usr/bin/env python3
"""
Generate week_4_key.json with all exercises, solutions, and verified results.
"""

import json
import re
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'core'))
from sql_helper import SQLHelper

def extract_exercises_from_solutions():
    """Extract exercises and solutions from the solutions markdown file."""
    exercises = []
    
    # Read the solutions file
    with open('solutions/week_4_practice_solutions.md', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split by exercise numbers (looking for **1. through **15.)
    exercise_pattern = r'\*\*(\d+)\.\s*(.+?)\*\*\n(.+?)(?=\*\*Solution:\*\*|$)'
    solution_pattern = r'\*\*Solution:\*\*\n```sql\n(.*?)\n```'
    
    # Find all exercises
    exercise_matches = re.finditer(exercise_pattern, content, re.DOTALL)
    
    for match in exercise_matches:
        exercise_id = int(match.group(1))
        title = match.group(2).strip()
        description = match.group(3).strip()
        
        # Find the corresponding solution
        # Look for the solution after this exercise
        start_pos = match.end()
        remaining_content = content[start_pos:]
        
        solution_match = re.search(solution_pattern, remaining_content, re.DOTALL)
        
        if solution_match:
            solution_query = solution_match.group(1).strip()
            
            exercises.append({
                'id': exercise_id,
                'title': title,
                'statement': description,
                'solution': solution_query
            })
    
    return exercises

def manual_exercises():
    """Manually define exercises since regex parsing is complex for this format."""
    exercises = [
        {
            'id': 1,
            'title': 'Company Job Listings',
            'statement': 'Find all job titles and company names for Data Scientist positions. Show only companies that currently have job postings.',
            'solution': '''SELECT c.company_name, j.job_title, j.job_posted_date
FROM companies AS c
INNER JOIN jobs AS j ON c.company_id = j.company_id
WHERE j.job_title_short = 'Data Scientist'
ORDER BY j.job_posted_date DESC;'''
        },
        {
            'id': 2,
            'title': 'Jobs by Location',
            'statement': 'List all job titles with their corresponding countries and cities. Only include jobs that have location information.',
            'solution': '''SELECT j.job_title_short, l.job_location, l.job_country
FROM jobs AS j
INNER JOIN locations AS l ON j.location_id = l.location_id
ORDER BY l.job_country, l.job_location;'''
        },
        {
            'id': 3,
            'title': 'Platform Analytics',
            'statement': 'Show which platforms (job_via) are posting the most Data Engineer jobs. Include platform name and job count.',
            'solution': '''SELECT p.platform_name, COUNT(j.job_id) AS job_count
FROM platforms AS p
INNER JOIN jobs AS j ON p.platform_id = j.platform_id
WHERE j.job_title_short = 'Data Engineer'
GROUP BY p.platform_name
ORDER BY job_count DESC;'''
        },
        {
            'id': 4,
            'title': 'All Companies with Job Counts',
            'statement': 'List all companies and count how many current job postings they have. Include companies that might not have any current postings (show 0 for them).',
            'solution': '''SELECT c.company_name, COUNT(j.job_id) AS job_count
FROM companies AS c
LEFT JOIN jobs AS j ON c.company_id = j.company_id
GROUP BY c.company_name
ORDER BY job_count DESC;'''
        },
        {
            'id': 5,
            'title': 'Remote Work Analysis',
            'statement': 'Show all job titles and whether they offer remote work options. Include all jobs, even those where remote work information is not specified.',
            'solution': '''SELECT j.job_title_short, 
       j.job_work_from_home,
       COUNT(*) AS total_jobs
FROM jobs AS j
GROUP BY j.job_title_short, j.job_work_from_home
ORDER BY j.job_title_short, j.job_work_from_home;'''
        },
        {
            'id': 6,
            'title': 'Skills in Demand',
            'statement': 'Find the top 10 most requested skills across all Data Analyst positions. Join jobs, companies, and skills tables.',
            'solution': '''SELECT s.skill_name, s.skill_category, COUNT(js.job_id) AS demand_count
FROM skills AS s
INNER JOIN job_skills AS js ON s.skill_id = js.skill_id
INNER JOIN jobs AS j ON js.job_id = j.job_id
WHERE j.job_title_short = 'Data Analyst'
GROUP BY s.skill_name, s.skill_category
ORDER BY demand_count DESC
LIMIT 10;'''
        },
        {
            'id': 7,
            'title': 'High-Paying Companies',
            'statement': 'List companies offering Data Engineer positions with above-average salaries (>$100,000). Include company name, average salary, and job count.',
            'solution': '''SELECT c.company_name, 
       AVG(j.salary_year_avg) AS avg_salary,
       COUNT(j.job_id) AS job_count
FROM companies AS c
INNER JOIN jobs AS j ON c.company_id = j.company_id
WHERE j.job_title_short = 'Data Engineer' 
  AND j.salary_year_avg > 100000
GROUP BY c.company_name
ORDER BY avg_salary DESC;'''
        },
        {
            'id': 8,
            'title': 'Geographic Salary Analysis',
            'statement': 'Find the average salary for Data Scientist roles by country. Only include countries with at least 5 job postings.',
            'solution': '''SELECT l.job_country, 
       AVG(j.salary_year_avg) AS avg_salary,
       COUNT(j.job_id) AS job_count
FROM locations AS l
INNER JOIN jobs AS j ON l.location_id = j.location_id
WHERE j.job_title_short = 'Data Scientist'
  AND j.salary_year_avg IS NOT NULL
GROUP BY l.job_country
HAVING COUNT(j.job_id) >= 5
ORDER BY avg_salary DESC;'''
        },
        {
            'id': 9,
            'title': 'Tech Stack Analysis',
            'statement': 'For each company hiring Data Engineers, show the most common skill category they require (programming, cloud, analyst_tools, etc.).',
            'solution': '''WITH skill_counts AS (
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
ORDER BY skill_count DESC;'''
        },
        {
            'id': 10,
            'title': 'Platform Performance',
            'statement': 'Find platforms that post jobs from companies offering above-average salaries ($90,000+). Include platform name, number of high-paying companies, and average salary of jobs posted.',
            'solution': '''SELECT p.platform_name,
       COUNT(DISTINCT c.company_id) AS high_paying_companies,
       AVG(j.salary_year_avg) AS avg_salary
FROM platforms AS p
INNER JOIN jobs AS j ON p.platform_id = j.platform_id
INNER JOIN companies AS c ON j.company_id = c.company_id
WHERE j.salary_year_avg >= 90000
GROUP BY p.platform_name
ORDER BY avg_salary DESC;'''
        },
        {
            'id': 11,
            'title': 'Multi-Skill Requirements',
            'statement': 'Find Data Scientist jobs that require both Python and SQL skills. Show company name, job title, and salary.',
            'solution': '''SELECT c.company_name, j.job_title, j.salary_year_avg
FROM companies AS c
INNER JOIN jobs AS j ON c.company_id = j.company_id
INNER JOIN job_skills AS js1 ON j.job_id = js1.job_id
INNER JOIN skills AS s1 ON js1.skill_id = s1.skill_id
INNER JOIN job_skills AS js2 ON j.job_id = js2.job_id
INNER JOIN skills AS s2 ON js2.skill_id = s2.skill_id
WHERE j.job_title_short = 'Data Scientist'
  AND s1.skill_name = 'Python'
  AND s2.skill_name = 'SQL'
  AND j.salary_year_avg IS NOT NULL
ORDER BY j.salary_year_avg DESC;'''
        },
        {
            'id': 12,
            'title': 'Remote vs On-site Salary Gap',
            'statement': 'Compare average salaries for remote vs on-site Data Engineer positions by company. Only include companies with both types of positions.',
            'solution': '''WITH salary_comparison AS (
    SELECT c.company_name,
           AVG(CASE WHEN j.job_work_from_home = TRUE THEN j.salary_year_avg END) AS remote_avg_salary,
           AVG(CASE WHEN j.job_work_from_home = FALSE THEN j.salary_year_avg END) AS onsite_avg_salary
    FROM companies AS c
    INNER JOIN jobs AS j ON c.company_id = j.company_id
    WHERE j.job_title_short = 'Data Engineer'
      AND j.salary_year_avg IS NOT NULL
    GROUP BY c.company_name
    HAVING COUNT(CASE WHEN j.job_work_from_home = TRUE THEN 1 END) > 0
       AND COUNT(CASE WHEN j.job_work_from_home = FALSE THEN 1 END) > 0
)
SELECT company_name,
       remote_avg_salary,
       onsite_avg_salary,
       (remote_avg_salary - onsite_avg_salary) AS salary_difference
FROM salary_comparison
WHERE remote_avg_salary IS NOT NULL AND onsite_avg_salary IS NOT NULL
ORDER BY salary_difference DESC;'''
        },
        {
            'id': 13,
            'title': 'Skill Correlation Analysis',
            'statement': 'Find pairs of skills that frequently appear together in Data Analyst job postings. Show skill combinations that appear in at least 10 jobs together.',
            'solution': '''SELECT s1.skill_name AS skill1_name,
       s2.skill_name AS skill2_name,
       COUNT(DISTINCT js1.job_id) AS co_occurrence_count
FROM job_skills AS js1
INNER JOIN job_skills AS js2 ON js1.job_id = js2.job_id AND js1.skill_id < js2.skill_id
INNER JOIN skills AS s1 ON js1.skill_id = s1.skill_id
INNER JOIN skills AS s2 ON js2.skill_id = s2.skill_id
INNER JOIN jobs AS j ON js1.job_id = j.job_id
WHERE j.job_title_short = 'Data Analyst'
GROUP BY s1.skill_name, s2.skill_name
HAVING COUNT(DISTINCT js1.job_id) >= 10
ORDER BY co_occurrence_count DESC;'''
        },
        {
            'id': 14,
            'title': 'Seasonal Hiring Patterns',
            'statement': 'Analyze hiring patterns by showing the number of Data Engineer jobs posted by each platform per month in 2023.',
            'solution': '''SELECT p.platform_name,
       EXTRACT(MONTH FROM j.job_posted_date) AS month,
       COUNT(j.job_id) AS job_count
FROM platforms AS p
INNER JOIN jobs AS j ON p.platform_id = j.platform_id
WHERE j.job_title_short = 'Data Engineer'
  AND EXTRACT(YEAR FROM j.job_posted_date) = 2023
GROUP BY p.platform_name, EXTRACT(MONTH FROM j.job_posted_date)
ORDER BY p.platform_name, month;'''
        },
        {
            'id': 15,
            'title': 'Complete Market Analysis',
            'statement': 'Create a comprehensive report showing: company name, location, total jobs posted, average salary, most required skill, and primary posting platform. Only include companies with 5+ job postings.',
            'solution': '''WITH company_stats AS (
    SELECT c.company_name,
           l.job_location,
           COUNT(j.job_id) AS total_jobs,
           AVG(j.salary_year_avg) AS avg_salary
    FROM companies AS c
    INNER JOIN jobs AS j ON c.company_id = j.company_id
    INNER JOIN locations AS l ON j.location_id = l.location_id
    WHERE j.salary_year_avg IS NOT NULL
    GROUP BY c.company_name, l.job_location
    HAVING COUNT(j.job_id) >= 5
),
top_skills AS (
    SELECT c.company_name,
           s.skill_name,
           ROW_NUMBER() OVER (PARTITION BY c.company_name ORDER BY COUNT(s.skill_id) DESC) AS skill_rank
    FROM companies AS c
    INNER JOIN jobs AS j ON c.company_id = j.company_id
    INNER JOIN job_skills AS js ON j.job_id = js.job_id
    INNER JOIN skills AS s ON js.skill_id = s.skill_id
    GROUP BY c.company_name, s.skill_name
),
main_platforms AS (
    SELECT c.company_name,
           p.platform_name,
           ROW_NUMBER() OVER (PARTITION BY c.company_name ORDER BY COUNT(j.job_id) DESC) AS platform_rank
    FROM companies AS c
    INNER JOIN jobs AS j ON c.company_id = j.company_id
    INNER JOIN platforms AS p ON j.platform_id = p.platform_id
    GROUP BY c.company_name, p.platform_name
)
SELECT cs.company_name,
       cs.job_location,
       cs.total_jobs,
       ROUND(cs.avg_salary, 2) AS avg_salary,
       ts.skill_name AS top_skill,
       mp.platform_name AS main_platform
FROM company_stats AS cs
LEFT JOIN top_skills AS ts ON cs.company_name = ts.company_name AND ts.skill_rank = 1
LEFT JOIN main_platforms AS mp ON cs.company_name = mp.company_name AND mp.platform_rank = 1
ORDER BY cs.total_jobs DESC;'''
        }
    ]
    
    return exercises

def test_exercise_with_helper(exercise, helper):
    """Test an exercise with the SQL helper and return result info."""
    try:
        result = helper.execute_query(exercise['solution'], exercise['id'])
        
        if result['status'] == 'success':
            # Get sample results (first 3 rows)
            sample_results = []
            if result['data'] is not None and not result['data'].empty:
                sample_df = result['data'].head(3)
                # Convert datetime objects to strings for JSON serialization
                sample_df = sample_df.astype(str)
                sample_results = sample_df.to_dict('records')
            
            return {
                'working': True,
                'execution_time': result['execution_time'],
                'row_count': result['row_count'],
                'columns': result['columns'],
                'sample_results': sample_results,
                'error': None
            }
        else:
            return {
                'working': False,
                'execution_time': None,
                'row_count': 0,
                'columns': [],
                'sample_results': [],
                'error': result['error']
            }
    except Exception as e:
        return {
            'working': False,
            'execution_time': None,
            'row_count': 0,
            'columns': [],
            'sample_results': [],
            'error': str(e)
        }

def generate_week_4_key():
    """Generate the complete week 4 key JSON file."""
    print("🔧 Generating Week 4 Practice Key...")
    
    # Get exercises
    exercises = manual_exercises()
    print(f"📋 Found {len(exercises)} exercises")
    
    # Initialize SQL helper
    helper = SQLHelper('../../datasets/data_jobs.db')
    
    # Test each exercise
    key_data = {
        'metadata': {
            'title': 'Week 4 Practice - Data Jobs Dataset',
            'description': 'JOIN operations on real-world data analytics job postings',
            'total_exercises': len(exercises),
            'database': 'data_jobs.db',
            'total_records': 785741
        },
        'exercises': []
    }
    
    for exercise in exercises:
        print(f"\n🧪 Testing Exercise {exercise['id']}: {exercise['title']}")
        
        test_result = test_exercise_with_helper(exercise, helper)
        
        exercise_data = {
            'id': exercise['id'],
            'title': exercise['title'],
            'statement': exercise['statement'],
            'solution': exercise['solution'],
            'result': test_result
        }
        
        key_data['exercises'].append(exercise_data)
        
        if test_result['working']:
            print(f"  ✅ Working - {test_result['row_count']} rows in {test_result['execution_time']}s")
        else:
            print(f"  ❌ Error: {test_result['error']}")
    
    # Close helper
    helper.close()
    
    # Save to JSON file
    with open('../../exercises/week_4_key.json', 'w', encoding='utf-8') as f:
        json.dump(key_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n🎉 Generated week_4_key.json with {len(exercises)} exercises")
    print(f"📊 Summary:")
    working_count = sum(1 for ex in key_data['exercises'] if ex['result']['working'])
    print(f"  ✅ Working: {working_count}/{len(exercises)}")
    print(f"  ❌ Failed: {len(exercises) - working_count}/{len(exercises)}")
    
    return key_data

if __name__ == "__main__":
    key_data = generate_week_4_key()
    print("\n✨ Week 4 key file generated successfully!") 