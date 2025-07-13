# Week 4 Practice - Data Jobs Dataset (Enhanced)

**Description:** JOIN operations demonstrating how combining tables reveals insights not available in individual tables
**Database:** data_jobs.db
**Total Exercises:** 8
**Focus Topics:** INNER JOIN, LEFT JOIN, Table aliases, Cross-table analysis, Data relationships

*Report generated on: 2025-07-12 12:36:41*

---

## Exercise 1: Company Size Impact on Remote Work

**Difficulty:** Medium
**Topics:** INNER JOIN, GROUP BY, CASE WHEN, Percentage calculation, Cross-table analysis
**Educational Focus:** Shows how joining reveals correlation between company hiring volume and remote work policies - insights not available in either table alone

### Problem Statement

Analyze how company hiring activity correlates with remote work policies. Show company name, total jobs posted by the company, and percentage of jobs that are remote. This requires combining company hiring volume (from companies table) with remote work data (from job_postings table). Only include companies with 10+ jobs posted.

### SQL Solution

```sql
SELECT c.company_name, 
       c.total_jobs AS company_total_jobs,
       COUNT(jp.job_id) AS jobs_in_dataset,
       ROUND(COUNT(CASE WHEN jp.job_work_from_home = 'True' THEN 1 END) * 100.0 / COUNT(jp.job_id), 2) AS remote_job_percentage
FROM companies AS c
INNER JOIN job_postings AS jp ON c.company_name = jp.company_name
WHERE c.total_jobs >= 10
GROUP BY c.company_name, c.total_jobs
ORDER BY remote_job_percentage DESC
LIMIT 15;
```

### Results

✅ **Query executed successfully**
- **Execution time:** 0.085s
- **Rows returned:** 20
- **Columns:** company_name, company_total_jobs, jobs_in_dataset, remote_job_percentage

#### Top 20 Results

| company_name | company_total_jobs | jobs_in_dataset | remote_job_percentage |
| --- | --- | --- | --- |
| Infogain | 103 | 1 | 100 |
| Boehringer Ingelheim | 138 | 1 | 100 |
| US Tech Solutions | 156 | 1 | 100 |
| Navy Federal Credit Union | 312 | 1 | 100 |
| Braintrust | 231 | 2 | 100 |
| Wipro | 390 | 1 | 100 |
| BAIRESDEV | 101 | 1 | 100 |
| Nagarro | 113 | 2 | 100 |
| Collabera | 205 | 1 | 100 |
| Amgen | 113 | 1 | 100 |
| Splunk | 337 | 1 | 100 |
| Xpertise Recruitment | 100 | 1 | 100 |
| Lawrence Harvey | 225 | 1 | 100 |
| EPAM Anywhere | 337 | 4 | 100 |
| Listopro | 1984 | 2 | 100 |
| OESON | 105 | 3 | 100 |
| Kpler | 99 | 1 | 100 |
| Upwork | 1415 | 4 | 75 |
| EPAM Systems | 1133 | 8 | 75 |
| Crossover | 361 | 27 | 74.07 |

---

## Exercise 2: Geographic Job Market Density vs Platform Usage

**Difficulty:** Medium
**Topics:** INNER JOIN, GROUP BY, HAVING, Market analysis, Geographic correlation
**Educational Focus:** Demonstrates how joins reveal relationships between geographic job density and platform effectiveness - combining location market data with platform usage patterns

### Problem Statement

Identify which job platforms are most effective in high-density job markets. Show location, job market density (from locations table), most popular platform in that location, and platform's job count. This combines geographic market data with platform preference data.

### SQL Solution

```sql
SELECT l.job_location,
       l.job_country,
       l.job_count AS market_density,
       jp.job_via AS most_popular_platform,
       COUNT(jp.job_id) AS platform_jobs_in_location
FROM locations AS l
INNER JOIN job_postings AS jp ON l.job_location = jp.job_location
WHERE l.job_count > 500
GROUP BY l.job_location, l.job_country, l.job_count, jp.job_via
HAVING COUNT(jp.job_id) > 20
ORDER BY l.job_count DESC, platform_jobs_in_location DESC
LIMIT 20;
```

### Results

✅ **Query executed successfully**
- **Execution time:** 0.003s
- **Rows returned:** 20
- **Columns:** job_location, job_country, market_density, most_popular_platform, platform_jobs_in_location

#### Top 20 Results

| job_location | job_country | market_density | most_popular_platform | platform_jobs_in_location |
| --- | --- | --- | --- | --- |
| Singapore | Singapore | 23415 | via LinkedIn | 49 |
| Singapore | Singapore | 23415 | via BeBee Singapore | 28 |
| Singapore | Singapore | 23415 | via Recruit.net | 24 |
| Anywhere | United States | 23021 | via LinkedIn | 273 |
| Anywhere | United States | 23021 | via Recruit.net | 103 |
| Anywhere | United States | 23021 | via Indeed | 56 |
| Paris, France | France | 12311 | via BeBee | 80 |
| Paris, France | France | 12311 | via Indeed | 45 |
| Paris, France | France | 12311 | via LinkedIn | 23 |
| Bengaluru, Karnataka, India | India | 11474 | via LinkedIn | 54 |
| London, UK | United Kingdom | 10564 | via Recruit.net | 34 |
| London, UK | United Kingdom | 10564 | via LinkedIn | 24 |
| Madrid, Spain | Spain | 9787 | via BeBee | 34 |
| Madrid, Spain | Spain | 9787 | via Recruit.net | 22 |
| New York, NY | United States | 7891 | via LinkedIn | 40 |
| Lisbon, Portugal | Portugal | 7171 | via Empregos Trabajo.org | 24 |
| Atlanta, GA | United States | 6994 | via LinkedIn | 32 |
| Hyderabad, Telangana, India | India | 6841 | via LinkedIn | 28 |
| Dublin, Ireland | Ireland | 6559 | via Trabajo.org | 53 |
| Dublin, Ireland | Ireland | 6559 | via BeBee Ireland | 30 |

---

## Exercise 3: Platform Reach vs Company Diversity

**Difficulty:** Medium
**Topics:** INNER JOIN, COUNT DISTINCT, GROUP BY, HAVING, Business model analysis
**Educational Focus:** Shows how joins reveal platform business models - combining platform capacity with employer diversity metrics that require data from both tables

### Problem Statement

Analyze which platforms attract the most diverse range of employers. Show platform name, platform's total capacity (from job_platforms table), number of unique companies using the platform, and average jobs per company. This reveals platform business models and employer diversity.

### SQL Solution

```sql
SELECT jpl.platform_name,
       jpl.jobs_posted AS platform_capacity,
       COUNT(DISTINCT jp.company_name) AS unique_companies,
       COUNT(jp.job_id) AS actual_jobs_posted,
       ROUND(COUNT(jp.job_id) * 1.0 / COUNT(DISTINCT jp.company_name), 2) AS avg_jobs_per_company
FROM job_platforms AS jpl
INNER JOIN job_postings AS jp ON jpl.platform_name = jp.job_via
GROUP BY jpl.platform_name, jpl.jobs_posted
HAVING COUNT(DISTINCT jp.company_name) > 50
ORDER BY unique_companies DESC
LIMIT 12;
```

### Results

✅ **Query executed successfully**
- **Execution time:** 0.004s
- **Rows returned:** 16
- **Columns:** platform_name, platform_capacity, unique_companies, actual_jobs_posted, avg_jobs_per_company

#### Top 20 Results

| platform_name | platform_capacity | unique_companies | actual_jobs_posted | avg_jobs_per_company |
| --- | --- | --- | --- | --- |
| via LinkedIn | 186679 | 1079 | 1952 | 1.81 |
| via Trabajo.org | 61562 | 911 | 1308 | 1.44 |
| via BeBee | 103507 | 593 | 708 | 1.19 |
| via Recruit.net | 23646 | 565 | 779 | 1.38 |
| via Indeed | 42756 | 335 | 450 | 1.34 |
| via Jobrapido.com | 6202 | 283 | 384 | 1.36 |
| via Talent.com | 4242 | 212 | 258 | 1.22 |
| via CareerBuilder | 1331 | 125 | 221 | 1.77 |
| via Jooble | 3711 | 92 | 113 | 1.23 |
| via Snagajob | 9355 | 87 | 148 | 1.70 |
| via Big Country Jobs | 1350 | 86 | 118 | 1.37 |
| via ZipRecruiter | 15533 | 76 | 99 | 1.30 |
| via My ArkLaMiss Jobs | 3151 | 63 | 76 | 1.21 |
| via BeBee Nederland | 3384 | 59 | 64 | 1.08 |
| via Adzuna | 5238 | 56 | 71 | 1.27 |
| via BeBee Deutschland | 1637 | 51 | 57 | 1.12 |

---

## Exercise 4: International Salary Benchmarking

**Difficulty:** Hard
**Topics:** Multiple JOINs, INNER JOIN, BETWEEN, AVG function, International comparison
**Educational Focus:** Demonstrates complex multi-table joins that combine geographic, salary, and classification data to enable international salary benchmarking

### Problem Statement

Compare salary expectations across countries by experience level. Show country, experience level classification (from salary_ranges table), number of jobs in that category, and average salary. This requires joining geographic, salary, and classification data.

### SQL Solution

```sql
SELECT l.job_country,
       sr.experience_level,
       sr.range_name,
       COUNT(jp.job_id) AS jobs_in_category,
       ROUND(AVG(jp.salary_year_avg), 0) AS avg_salary
FROM job_postings AS jp
INNER JOIN locations AS l ON jp.job_location = l.job_location
INNER JOIN salary_ranges AS sr ON jp.salary_year_avg BETWEEN sr.min_salary AND sr.max_salary
WHERE jp.salary_year_avg IS NOT NULL
GROUP BY l.job_country, sr.experience_level, sr.range_name, sr.min_salary
HAVING COUNT(jp.job_id) >= 10
ORDER BY l.job_country, sr.min_salary
LIMIT 20;
```

### Results

✅ **Query executed successfully**
- **Execution time:** 0.002s
- **Rows returned:** 4
- **Columns:** job_country, experience_level, range_name, jobs_in_category, avg_salary

#### Top 20 Results

| job_country | experience_level | range_name | jobs_in_category | avg_salary |
| --- | --- | --- | --- | --- |
| Sudan | Senior | Senior Level | 24 | 123511 |
| United States | Mid | Mid Level | 22 | 85524 |
| United States | Senior | Senior Level | 50 | 123261 |
| United States | Executive | Executive | 37 | 187180 |

---

## Exercise 5: Skills Requirements vs Company Hiring Patterns

**Difficulty:** Medium
**Topics:** INNER JOIN, CASE WHEN, Percentage calculation, GROUP BY, Skills analysis
**Educational Focus:** Shows how joins reveal company hiring strategies by combining hiring volume data with job requirements - insights about company culture and standards

### Problem Statement

Identify companies that consistently hire for high-skill positions. Show company name, company's total hiring activity (from companies table), percentage of jobs requiring no degree, and percentage offering health insurance. This correlates company hiring volume with skill requirements.

### SQL Solution

```sql
SELECT c.company_name,
       c.total_jobs AS company_hiring_volume,
       COUNT(jp.job_id) AS jobs_in_sample,
       ROUND(COUNT(CASE WHEN jp.job_no_degree_mention = 'True' THEN 1 END) * 100.0 / COUNT(jp.job_id), 2) AS pct_no_degree_required,
       ROUND(COUNT(CASE WHEN jp.job_health_insurance = 'True' THEN 1 END) * 100.0 / COUNT(jp.job_id), 2) AS pct_health_insurance
FROM companies AS c
INNER JOIN job_postings AS jp ON c.company_name = jp.company_name
WHERE c.total_jobs >= 20
GROUP BY c.company_name, c.total_jobs
ORDER BY pct_health_insurance DESC, pct_no_degree_required DESC
LIMIT 15;
```

### Results

✅ **Query executed successfully**
- **Execution time:** 0.003s
- **Rows returned:** 20
- **Columns:** company_name, company_hiring_volume, jobs_in_sample, pct_no_degree_required, pct_health_insurance

#### Top 20 Results

| company_name | company_hiring_volume | jobs_in_sample | pct_no_degree_required | pct_health_insurance |
| --- | --- | --- | --- | --- |
| Jefferson Frank | 184 | 1 | 100 | 100 |
| Lumen | 147 | 2 | 50 | 100 |
| Zurich Insurance Company Ltd. | 95 | 2 | 0 | 100 |
| IDR, Inc. | 90 | 1 | 0 | 100 |
| Superior HealthPlan | 112 | 1 | 0 | 100 |
| SoFi | 102 | 3 | 0 | 100 |
| EDWARD JONES | 130 | 9 | 0 | 100 |
| JPMorgan Chase | 124 | 1 | 0 | 100 |
| Dell | 82 | 1 | 0 | 100 |
| Technology Partners | 89 | 1 | 0 | 100 |
| Ryder System | 85 | 1 | 0 | 100 |
| Splunk | 337 | 1 | 0 | 100 |
| Johns Hopkins University | 153 | 2 | 0 | 100 |
| Cox Communications | 225 | 1 | 0 | 100 |
| Electronic Arts | 165 | 1 | 0 | 100 |
| Professional Diversity Network | 133 | 2 | 0 | 100 |
| Fiserv | 123 | 1 | 0 | 100 |
| FullStack Labs | 341 | 2 | 0 | 100 |
| Forfeiture Support Associates | 84 | 2 | 0 | 100 |
| World Wide Technology | 164 | 1 | 0 | 100 |

---

## Exercise 6: Location Premium Analysis

**Difficulty:** Hard
**Topics:** Multiple JOINs, HAVING with conditions, AVG function, Premium analysis, Market comparison
**Educational Focus:** Complex join combining location market data, salary ranges, and actual salaries to identify premium markets - requires all three tables for the analysis

### Problem Statement

Identify locations where companies pay premium salaries relative to experience level expectations. Show location, country, market size (from locations table), experience level, expected salary range, and actual average salary. Find locations where actual salaries exceed range maximums.

### SQL Solution

```sql
SELECT l.job_location,
       l.job_country,
       l.job_count AS market_size,
       sr.experience_level,
       sr.min_salary AS expected_min,
       sr.max_salary AS expected_max,
       ROUND(AVG(jp.salary_year_avg), 0) AS actual_avg_salary,
       ROUND(AVG(jp.salary_year_avg) - sr.max_salary, 0) AS premium_over_range
FROM job_postings AS jp
INNER JOIN locations AS l ON jp.job_location = l.job_location
INNER JOIN salary_ranges AS sr ON jp.salary_year_avg BETWEEN sr.min_salary AND sr.max_salary
WHERE jp.salary_year_avg IS NOT NULL
GROUP BY l.job_location, l.job_country, l.job_count, sr.experience_level, sr.min_salary, sr.max_salary
HAVING COUNT(jp.job_id) >= 5 AND AVG(jp.salary_year_avg) > sr.max_salary
ORDER BY premium_over_range DESC
LIMIT 15;
```

### Results

✅ **Query executed successfully**
- **Execution time:** 0.003s
- **Rows returned:** 0
- **Columns:** job_location, job_country, market_size, experience_level, expected_min, expected_max, actual_avg_salary, premium_over_range

*No data returned by the query.*

---

## Exercise 7: Platform Efficiency vs Geographic Reach

**Difficulty:** Hard
**Topics:** Mixed JOINs, INNER JOIN, LEFT JOIN, Efficiency analysis, Geographic reach
**Educational Focus:** Demonstrates combining INNER and LEFT JOINs to analyze platform efficiency and geographic reach - requires data from all three tables

### Problem Statement

Analyze platform efficiency by comparing their declared capacity with actual performance across different markets. Show platform name, declared capacity (from job_platforms table), number of countries reached, average jobs per country, and capacity utilization rate.

### SQL Solution

```sql
SELECT jpl.platform_name,
       jpl.jobs_posted AS declared_capacity,
       COUNT(DISTINCT l.job_country) AS countries_reached,
       COUNT(jp.job_id) AS actual_jobs,
       ROUND(COUNT(jp.job_id) * 1.0 / COUNT(DISTINCT l.job_country), 2) AS avg_jobs_per_country,
       ROUND(COUNT(jp.job_id) * 100.0 / jpl.jobs_posted, 2) AS capacity_utilization_pct
FROM job_platforms AS jpl
INNER JOIN job_postings AS jp ON jpl.platform_name = jp.job_via
LEFT JOIN locations AS l ON jp.job_location = l.job_location
GROUP BY jpl.platform_name, jpl.jobs_posted
HAVING COUNT(jp.job_id) > 100
ORDER BY capacity_utilization_pct DESC
LIMIT 15;
```

### Results

✅ **Query executed successfully**
- **Execution time:** 0.005s
- **Rows returned:** 19
- **Columns:** platform_name, declared_capacity, countries_reached, actual_jobs, avg_jobs_per_country, capacity_utilization_pct

#### Top 20 Results

| platform_name | declared_capacity | countries_reached | actual_jobs | avg_jobs_per_country | capacity_utilization_pct |
| --- | --- | --- | --- | --- | --- |
| via CareerBuilder | 1331 | 39 | 628 | 16.10 | 47.18 |
| via EMPREGO | 993 | 40 | 284 | 7.10 | 28.60 |
| via AngelList | 800 | 38 | 196 | 5.16 | 24.50 |
| via Recruit.net | 23646 | 47 | 4615 | 98.19 | 19.52 |
| via Totaljobs | 1042 | 38 | 119 | 3.13 | 11.42 |
| via Jooble | 3711 | 41 | 421 | 10.27 | 11.34 |
| via Snagajob | 9355 | 38 | 866 | 22.79 | 9.26 |
| via Big Country Jobs | 1350 | 7 | 121 | 17.29 | 8.96 |
| via HelloWork | 1346 | 38 | 115 | 3.03 | 8.54 |
| via Upwork | 1357 | 38 | 114 | 3 | 8.40 |
| via LinkedIn | 186679 | 53 | 12222 | 230.60 | 6.55 |
| via Talent.com | 4242 | 13 | 275 | 21.15 | 6.48 |
| via Jobrapido.com | 6202 | 19 | 384 | 20.21 | 6.19 |
| via Indeed | 42756 | 44 | 2544 | 57.82 | 5.95 |
| via Linkedin | 2547 | 39 | 142 | 3.64 | 5.58 |
| via ZipRecruiter | 15533 | 38 | 705 | 18.55 | 4.54 |
| via Dice | 4493 | 38 | 158 | 4.16 | 3.52 |
| via Trabajo.org | 61562 | 43 | 1344 | 31.26 | 2.18 |
| via BeBee | 103507 | 19 | 742 | 39.05 | 0.72 |

---

## Exercise 8: Missing Data Impact Analysis

**Difficulty:** Medium
**Topics:** LEFT JOIN, Data quality analysis, NULL handling, CASE WHEN, Missing data patterns
**Educational Focus:** Shows how LEFT JOIN reveals data quality issues by combining company hiring volume with actual data completeness - demonstrates the value of preserving all records

### Problem Statement

Identify potential data quality issues by finding companies with significant hiring activity but missing job details. Show company name, total jobs (from companies table), jobs in our sample, jobs missing salary info, jobs missing location info, and data completeness percentage.

### SQL Solution

```sql
SELECT c.company_name,
       c.total_jobs AS total_company_jobs,
       COUNT(jp.job_id) AS jobs_in_sample,
       COUNT(CASE WHEN jp.salary_year_avg IS NULL THEN 1 END) AS jobs_missing_salary,
       COUNT(CASE WHEN jp.job_location IS NULL THEN 1 END) AS jobs_missing_location,
       ROUND((COUNT(jp.job_id) - COUNT(CASE WHEN jp.salary_year_avg IS NULL OR jp.job_location IS NULL THEN 1 END)) * 100.0 / COUNT(jp.job_id), 2) AS data_completeness_pct
FROM companies AS c
LEFT JOIN job_postings AS jp ON c.company_name = jp.company_name
WHERE c.total_jobs >= 50
GROUP BY c.company_name, c.total_jobs
ORDER BY data_completeness_pct ASC
LIMIT 15;
```

### Results

✅ **Query executed successfully**
- **Execution time:** 0.003s
- **Rows returned:** 20
- **Columns:** company_name, total_company_jobs, jobs_in_sample, jobs_missing_salary, jobs_missing_location, data_completeness_pct

#### Top 20 Results

| company_name | total_company_jobs | jobs_in_sample | jobs_missing_salary | jobs_missing_location | data_completeness_pct |
| --- | --- | --- | --- | --- | --- |
| Globant | 318 | 0 | 1 | 1 | -inf |
| Alstom | 159 | 0 | 1 | 1 | -inf |
| Russell Tobin | 113 | 0 | 1 | 1 | -inf |
| Energy Jobline | 141 | 0 | 1 | 1 | -inf |
| Old Mutual South Africa | 106 | 0 | 1 | 1 | -inf |
| Canonical | 188 | 0 | 1 | 1 | -inf |
| AECOM | 205 | 0 | 1 | 1 | -inf |
| System Soft Technologies | 83 | 0 | 1 | 1 | -inf |
| HCA Healthcare | 113 | 0 | 1 | 1 | -inf |
| amazon | 141 | 0 | 1 | 1 | -inf |
| Atlassian | 252 | 0 | 1 | 1 | -inf |
| HUK-COBURG Versicherungsgruppe | 94 | 0 | 1 | 1 | -inf |
| AUTODOC | 98 | 0 | 1 | 1 | -inf |
| CVS Pharmacy | 129 | 0 | 1 | 1 | -inf |
| The Hartford | 163 | 0 | 1 | 1 | -inf |
| Kforce Technology | 305 | 0 | 1 | 1 | -inf |
| Medtronic | 179 | 0 | 1 | 1 | -inf |
| Citizens | 246 | 0 | 1 | 1 | -inf |
| TD Bank | 91 | 0 | 1 | 1 | -inf |
| Deutsche Bundesbank | 128 | 0 | 1 | 1 | -inf |

---
