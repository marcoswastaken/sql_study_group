# Week 4 Practice - Alternate (Data Jobs Dataset)

## Dataset Overview

**Dataset:** [Data Jobs Dataset](https://huggingface.co/datasets/lukebarousse/data_jobs)

This dataset contains 785,741 real-world data analytics job postings from 2023, collected by Luke Barousse. You'll be working as a data analyst helping a recruiting company understand the job market landscape using SQL JOIN operations.

**Normalized Database Schema:**

For this exercise, imagine the flat dataset has been normalized into the following related tables:

```sql
CREATE TABLE companies (
    company_id INTEGER PRIMARY KEY,
    company_name VARCHAR(255)
);

CREATE TABLE locations (
    location_id INTEGER PRIMARY KEY,
    job_location VARCHAR(255),
    job_country VARCHAR(100)
);

CREATE TABLE platforms (
    platform_id INTEGER PRIMARY KEY,
    platform_name VARCHAR(255)  -- job_via field
);

CREATE TABLE jobs (
    job_id INTEGER PRIMARY KEY,
    company_id INTEGER,
    location_id INTEGER,
    platform_id INTEGER,
    job_title_short VARCHAR(100),
    job_title VARCHAR(255),
    job_schedule_type VARCHAR(50),
    job_work_from_home BOOLEAN,
    job_posted_date TIMESTAMP,
    job_no_degree_mention BOOLEAN,
    job_health_insurance BOOLEAN,
    salary_rate VARCHAR(20),
    salary_year_avg DECIMAL(10,2),
    salary_hour_avg DECIMAL(8,2),
    FOREIGN KEY (company_id) REFERENCES companies(company_id),
    FOREIGN KEY (location_id) REFERENCES locations(location_id),
    FOREIGN KEY (platform_id) REFERENCES platforms(platform_id)
);

CREATE TABLE skills (
    skill_id INTEGER PRIMARY KEY,
    skill_name VARCHAR(100),
    skill_category VARCHAR(50)  -- programming, cloud, analyst_tools, etc.
);

CREATE TABLE job_skills (
    job_id INTEGER,
    skill_id INTEGER,
    PRIMARY KEY (job_id, skill_id),
    FOREIGN KEY (job_id) REFERENCES jobs(job_id),
    FOREIGN KEY (skill_id) REFERENCES skills(skill_id)
);
```

## Practice Questions

### Basic INNER JOIN Questions

**1. Company Job Listings**
Find all job titles and company names for Data Scientist positions. Show only companies that currently have job postings.

**Expected Output Columns:** company_name, job_title, job_posted_date

**2. Jobs by Location**
List all job titles with their corresponding countries and cities. Only include jobs that have location information.

**Expected Output Columns:** job_title_short, job_location, job_country

**3. Platform Analytics**
Show which platforms (job_via) are posting the most Data Engineer jobs. Include platform name and job count.

**Expected Output Columns:** platform_name, job_count

### LEFT JOIN Questions

**4. All Companies with Job Counts**
List all companies and count how many current job postings they have. Include companies that might not have any current postings (show 0 for them).

**Expected Output Columns:** company_name, job_count

**5. Remote Work Analysis**
Show all job titles and whether they offer remote work options. Include all jobs, even those where remote work information is not specified.

**Expected Output Columns:** job_title_short, job_work_from_home, total_jobs

### Advanced JOIN Questions

**6. Skills in Demand**
Find the top 10 most requested skills across all Data Analyst positions. Join jobs, companies, and skills tables.

**Expected Output Columns:** skill_name, skill_category, demand_count

**7. High-Paying Companies**
List companies offering Data Engineer positions with above-average salaries (>$100,000). Include company name, average salary, and job count.

**Expected Output Columns:** company_name, avg_salary, job_count

**8. Geographic Salary Analysis**
Find the average salary for Data Scientist roles by country. Only include countries with at least 5 job postings.

**Expected Output Columns:** job_country, avg_salary, job_count

### Complex JOIN Questions

**9. Tech Stack Analysis**
For each company hiring Data Engineers, show the most common skill category they require (programming, cloud, analyst_tools, etc.).

**Expected Output Columns:** company_name, most_common_skill_category, skill_count

**10. Platform Performance**
Find platforms that post jobs from companies offering above-average salaries ($90,000+). Include platform name, number of high-paying companies, and average salary of jobs posted.

**Expected Output Columns:** platform_name, high_paying_companies, avg_salary

### Challenge Questions

**11. Multi-Skill Requirements**
Find Data Scientist jobs that require both Python and SQL skills. Show company name, job title, and salary.

**Expected Output Columns:** company_name, job_title, salary_year_avg

**12. Remote vs On-site Salary Gap**
Compare average salaries for remote vs on-site Data Engineer positions by company. Only include companies with both types of positions.

**Expected Output Columns:** company_name, remote_avg_salary, onsite_avg_salary, salary_difference

**13. Skill Correlation Analysis**
Find pairs of skills that frequently appear together in Data Analyst job postings. Show skill combinations that appear in at least 10 jobs together.

**Expected Output Columns:** skill1_name, skill2_name, co_occurrence_count

**14. Seasonal Hiring Patterns**
Analyze hiring patterns by showing the number of Data Engineer jobs posted by each platform per month in 2023.

**Expected Output Columns:** platform_name, month, job_count

**15. Complete Market Analysis**
Create a comprehensive report showing: company name, location, total jobs posted, average salary, most required skill, and primary posting platform. Only include companies with 5+ job postings.

**Expected Output Columns:** company_name, job_location, total_jobs, avg_salary, top_skill, main_platform

## Learning Objectives

By completing these exercises, you should be able to:

- Join job market data across multiple related tables
- Analyze salary trends and geographic patterns
- Understand skill demand in the tech job market
- Combine JOINs with aggregation for business insights
- Handle NULL values in real-world recruiting data
- Use complex multi-table JOINs for comprehensive analysis

## Tips for Success

1. **Think Like a Recruiter:** Consider what insights would be valuable for hiring decisions
2. **Handle NULLs Carefully:** Salary and skill data may have missing values
3. **Use Meaningful Aliases:** job_postings AS jp, companies AS c, etc.
4. **Consider Data Quality:** Real-world data may have inconsistencies
5. **Focus on Business Value:** Each query should answer a practical recruiting question

## Real-World Context

This dataset represents actual job market conditions for data roles in 2023. The skills, salaries, and geographic distributions reflect real hiring patterns that you might encounter in your career. Understanding how to analyze this type of data is directly applicable to:

- **Job Seekers:** Understanding market demand and salary expectations
- **Recruiters:** Identifying talent gaps and competitive salary ranges
- **Companies:** Benchmarking compensation and optimizing job postings
- **Career Counselors:** Providing data-driven advice to students
