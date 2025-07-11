# Week 4 Practice Solutions - Alternate (Data Jobs Dataset)

## Dataset Overview

**Dataset:** [Data Jobs Dataset](https://huggingface.co/datasets/lukebarousse/data_jobs)

This dataset contains 785,741 real-world data analytics job postings from 2023, collected by Luke Barousse. You'll be working as a data analyst helping a recruiting company understand the job market landscape using SQL JOIN operations.

**Normalized Database Schema:**

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

## Practice Questions with Solutions

### Basic INNER JOIN Questions

**1. Company Job Listings**
Find all job titles and company names for Data Scientist positions. Show only companies that currently have job postings.

**Solution:**
```sql
SELECT c.company_name, j.job_title, j.job_posted_date
FROM companies AS c
INNER JOIN jobs AS j ON c.company_id = j.company_id
WHERE j.job_title_short = 'Data Scientist'
ORDER BY j.job_posted_date DESC;
```

**Explanation:** INNER JOIN ensures we only get companies that actually have job postings, filtered for Data Scientist roles.

---

**2. Jobs by Location**
List all job titles with their corresponding countries and cities. Only include jobs that have location information.

**Solution:**
```sql
SELECT j.job_title_short, l.job_location, l.job_country
FROM jobs AS j
INNER JOIN locations AS l ON j.location_id = l.location_id
ORDER BY l.job_country, l.job_location;
```

**Explanation:** INNER JOIN excludes any jobs without location data, giving us only jobs with complete location information.

---

**3. Platform Analytics**
Show which platforms (job_via) are posting the most Data Engineer jobs. Include platform name and job count.

**Solution:**
```sql
SELECT p.platform_name, COUNT(j.job_id) AS job_count
FROM platforms AS p
INNER JOIN jobs AS j ON p.platform_id = j.platform_id
WHERE j.job_title_short = 'Data Engineer'
GROUP BY p.platform_name
ORDER BY job_count DESC;
```

**Explanation:** Groups by platform and counts Data Engineer positions, showing which platforms are most active for this role.

---

### LEFT JOIN Questions

**4. All Companies with Job Counts**
List all companies and count how many current job postings they have. Include companies that might not have any current postings (show 0 for them).

**Solution:**
```sql
SELECT c.company_name, COUNT(j.job_id) AS job_count
FROM companies AS c
LEFT JOIN jobs AS j ON c.company_id = j.company_id
GROUP BY c.company_name
ORDER BY job_count DESC;
```

**Explanation:** LEFT JOIN includes all companies, even those without current postings. COUNT(j.job_id) returns 0 for companies with no jobs.

---

**5. Remote Work Analysis**
Show all job titles and whether they offer remote work options. Include all jobs, even those where remote work information is not specified.

**Solution:**
```sql
SELECT j.job_title_short, 
       j.job_work_from_home,
       COUNT(*) AS total_jobs
FROM jobs AS j
GROUP BY j.job_title_short, j.job_work_from_home
ORDER BY j.job_title_short, j.job_work_from_home;
```

**Explanation:** Groups by job title and remote work status to show the distribution of remote vs on-site opportunities.

---

### Advanced JOIN Questions

**6. Skills in Demand**
Find the top 10 most requested skills across all Data Analyst positions. Join jobs, companies, and skills tables.

**Solution:**
```sql
SELECT s.skill_name, s.skill_category, COUNT(js.job_id) AS demand_count
FROM skills AS s
INNER JOIN job_skills AS js ON s.skill_id = js.skill_id
INNER JOIN jobs AS j ON js.job_id = j.job_id
WHERE j.job_title_short = 'Data Analyst'
GROUP BY s.skill_name, s.skill_category
ORDER BY demand_count DESC
LIMIT 10;
```

**Explanation:** Three-table JOIN connecting skills → job_skills → jobs, filtering for Data Analyst positions.

---

**7. High-Paying Companies**
List companies offering Data Engineer positions with above-average salaries (>$100,000). Include company name, average salary, and job count.

**Solution:**
```sql
SELECT c.company_name, 
       AVG(j.salary_year_avg) AS avg_salary,
       COUNT(j.job_id) AS job_count
FROM companies AS c
INNER JOIN jobs AS j ON c.company_id = j.company_id
WHERE j.job_title_short = 'Data Engineer' 
  AND j.salary_year_avg > 100000
GROUP BY c.company_name
ORDER BY avg_salary DESC;
```

**Explanation:** Filters for high-paying positions first, then aggregates by company to show competitive employers.

---

**8. Geographic Salary Analysis**
Find the average salary for Data Scientist roles by country. Only include countries with at least 5 job postings.

**Solution:**
```sql
SELECT l.job_country, 
       AVG(j.salary_year_avg) AS avg_salary,
       COUNT(j.job_id) AS job_count
FROM locations AS l
INNER JOIN jobs AS j ON l.location_id = j.location_id
WHERE j.job_title_short = 'Data Scientist'
  AND j.salary_year_avg IS NOT NULL
GROUP BY l.job_country
HAVING COUNT(j.job_id) >= 5
ORDER BY avg_salary DESC;
```

**Explanation:** Groups by country with HAVING clause to ensure statistical significance (5+ jobs per country).

---

### Complex JOIN Questions

**9. Tech Stack Analysis**
For each company hiring Data Engineers, show the most common skill category they require (programming, cloud, analyst_tools, etc.).

**Solution:**
```sql
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
ORDER BY skill_count DESC;
```

**Explanation:** Uses CTE with window function to find the most common skill category per company.

---

**10. Platform Performance**
Find platforms that post jobs from companies offering above-average salaries ($90,000+). Include platform name, number of high-paying companies, and average salary of jobs posted.

**Solution:**
```sql
SELECT p.platform_name,
       COUNT(DISTINCT c.company_id) AS high_paying_companies,
       AVG(j.salary_year_avg) AS avg_salary
FROM platforms AS p
INNER JOIN jobs AS j ON p.platform_id = j.platform_id
INNER JOIN companies AS c ON j.company_id = c.company_id
WHERE j.salary_year_avg >= 90000
GROUP BY p.platform_name
ORDER BY avg_salary DESC;
```

**Explanation:** Multi-table JOIN focusing on high-salary jobs, showing which platforms attract premium employers.

---

### Challenge Questions

**11. Multi-Skill Requirements**
Find Data Scientist jobs that require both Python and SQL skills. Show company name, job title, and salary.

**Solution:**
```sql
SELECT c.company_name, j.job_title, j.salary_year_avg
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
ORDER BY j.salary_year_avg DESC;
```

**Explanation:** Self-joins on job_skills and skills tables to find jobs requiring both specific skills.

---

**12. Remote vs On-site Salary Gap**
Compare average salaries for remote vs on-site Data Engineer positions by company. Only include companies with both types of positions.

**Solution:**
```sql
WITH salary_comparison AS (
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
ORDER BY salary_difference DESC;
```

**Explanation:** Uses conditional aggregation and HAVING to ensure companies have both remote and on-site positions.

---

**13. Skill Correlation Analysis**
Find pairs of skills that frequently appear together in Data Analyst job postings. Show skill combinations that appear in at least 10 jobs together.

**Solution:**
```sql
SELECT s1.skill_name AS skill1_name,
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
ORDER BY co_occurrence_count DESC;
```

**Explanation:** Self-join on job_skills to find skill pairs, with condition to avoid duplicate pairs and ensure minimum frequency.

---

**14. Seasonal Hiring Patterns**
Analyze hiring patterns by showing the number of Data Engineer jobs posted by each platform per month in 2023.

**Solution:**
```sql
SELECT p.platform_name,
       EXTRACT(MONTH FROM j.job_posted_date) AS month,
       COUNT(j.job_id) AS job_count
FROM platforms AS p
INNER JOIN jobs AS j ON p.platform_id = j.platform_id
WHERE j.job_title_short = 'Data Engineer'
  AND EXTRACT(YEAR FROM j.job_posted_date) = 2023
GROUP BY p.platform_name, EXTRACT(MONTH FROM j.job_posted_date)
ORDER BY p.platform_name, month;
```

**Explanation:** Uses date functions to extract month and year, showing seasonal patterns in hiring activity.

---

**15. Complete Market Analysis**
Create a comprehensive report showing: company name, location, total jobs posted, average salary, most required skill, and primary posting platform. Only include companies with 5+ job postings.

**Solution:**
```sql
WITH company_stats AS (
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
ORDER BY cs.total_jobs DESC;
```

**Explanation:** Complex query using multiple CTEs to gather company statistics, most common skills, and primary platforms.

---

## Key Learning Points

### Real-World Applications:
- **Salary Benchmarking:** Understanding market rates for negotiation
- **Skill Gap Analysis:** Identifying what skills to develop
- **Geographic Insights:** Finding best locations for career growth
- **Platform Strategy:** Knowing where to post/search for jobs

### Advanced SQL Techniques Demonstrated:
1. **Complex JOINs:** Multi-table relationships for comprehensive analysis
2. **Conditional Aggregation:** Using CASE statements with aggregate functions
3. **Window Functions:** ROW_NUMBER() for ranking and top-N analysis
4. **CTEs:** Breaking complex queries into readable components
5. **Self-Joins:** Finding relationships within the same table

### Business Intelligence Patterns:
- Market trend analysis through temporal data
- Competitive analysis through salary and benefit comparisons
- Demand forecasting through skill requirement patterns
- Platform performance evaluation for recruiting strategy 