# Week 4 Practice - Data Jobs Dataset (Ultra-Refined v4)

**Description:** JOIN operations that combine information from different tables to reveal business insights impossible to obtain from individual tables
**Database:** data_jobs.db
**Total Exercises:** 6
**Focus Topics:** INNER JOIN, LEFT JOIN, Table aliases, Cross-table analysis, Business insights, Window functions (advanced)

*Report generated on: 2025-07-14 07:28:31*

---

## Exercise 1: Platform Competition Analysis

**Difficulty:** Medium
**Topics:** INNER JOIN, GROUP BY, HAVING, Market analysis
**Educational Focus:** Shows how joining location data with job postings reveals platform competition patterns across different geographic markets. Removed unnecessary WHERE constraint to simplify query while maintaining educational value.

### Problem Statement

Find out which job platforms are most active in different countries. The `locations` table contains country information, and `job_postings` contains which platform each job came from. Your result should show the country name (`job_country`), platform name (`job_via` AS `platform_name`), and how many jobs that platform posted in that country (`platform_jobs_in_country`). Only include platform-country combinations with at least 20 jobs. Order by country first, then by job count (highest first), and limit to 30 rows.

### SQL Solution

```sql
SELECT l.job_country,
       jp.job_via AS platform_name,
       COUNT(jp.job_id) AS platform_jobs_in_country
FROM locations AS l
INNER JOIN job_postings AS jp ON l.job_location = jp.job_location
GROUP BY l.job_country, jp.job_via
HAVING COUNT(jp.job_id) >= 20
ORDER BY l.job_country, platform_jobs_in_country DESC
LIMIT 30;
```

### Results

✅ **Query executed successfully**
- **Execution time:** 0.121s
- **Rows returned:** 20
- **Columns:** job_country, platform_name, platform_jobs_in_country

#### Top 20 Results

| job_country | platform_name | platform_jobs_in_country |
| --- | --- | --- |
| Albania | via LinkedIn Albania | 54 |
| Argentina | via LinkedIn | 30337 |
| Argentina | via Indeed | 4413 |
| Argentina | via BeBee | 2613 |
| Argentina | via ZipRecruiter | 2115 |
| Argentina | via Jobgether | 1547 |
| Argentina | via Recruit.net | 1479 |
| Argentina | via Trabajo.org - Vacantes De Empleo, Trabajo | 1187 |
| Argentina | via Upwork | 995 |
| Argentina | via hh.ru | 646 |
| Argentina | via Snagajob | 624 |
| Argentina | via Linkedin | 604 |
| Argentina | via Startup Jobs | 562 |
| Argentina | via JobTeaser | 399 |
| Argentina | via HelloWork | 398 |
| Argentina | via Trabajo.org | 348 |
| Argentina | via Totaljobs | 344 |
| Argentina | via Get.It | 332 |
| Argentina | via Sercanto | 317 |
| Argentina | via Dice | 314 |

---

## Exercise 2: Platform Business Model Analysis

**Difficulty:** Medium
**Topics:** INNER JOIN, COUNT DISTINCT, GROUP BY, HAVING, Business model analysis
**Educational Focus:** Demonstrates combining platform capacity data with actual usage patterns to understand business models. Shows realistic utilization rates (~75%) and employer diversity across 60+ platforms.

### Problem Statement

Compare job platforms to understand their business models. The `job_platforms` table shows each platform's total capacity, while `job_postings` shows actual usage. Your result should show the platform name (`platform_name`), total capacity (`jobs_posted` AS `platform_capacity`), number of different companies using the platform (`unique_companies`), actual jobs posted (`actual_jobs_posted`), and average jobs per company (`avg_jobs_per_company`). Only include platforms with at least 1000 actual jobs posted. Order by actual jobs posted (highest first) and limit to 15 rows.

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
HAVING COUNT(jp.job_id) >= 1000
ORDER BY actual_jobs_posted DESC
LIMIT 15;
```

### Results

✅ **Query executed successfully**
- **Execution time:** 0.028s
- **Rows returned:** 20
- **Columns:** platform_name, platform_capacity, unique_companies, actual_jobs_posted, avg_jobs_per_company

#### Top 20 Results

| platform_name | platform_capacity | unique_companies | actual_jobs_posted | avg_jobs_per_company |
| --- | --- | --- | --- | --- |
| via LinkedIn | 186679 | 37996 | 139839 | 3.68 |
| via BeBee | 103507 | 26626 | 77541 | 2.91 |
| via Trabajo.org | 61562 | 18543 | 46264 | 2.49 |
| via Indeed | 42756 | 16396 | 32035 | 1.95 |
| via Recruit.net | 23646 | 7999 | 17835 | 2.23 |
| via ZipRecruiter | 15533 | 4733 | 11629 | 2.46 |
| via Jobs Trabajo.org | 10605 | 4692 | 7920 | 1.69 |
| via Trabajo.org - Vacantes De Empleo, Trabajo | 8919 | 1787 | 6665 | 3.73 |
| via BeBee India | 8642 | 2895 | 6483 | 2.24 |
| via BeBee Singapore | 7985 | 2869 | 5873 | 2.05 |
| via SimplyHired | 6632 | 3427 | 4941 | 1.44 |
| via Jobrapido.com | 6202 | 2744 | 4709 | 1.72 |
| via Sercanto | 5691 | 2538 | 4268 | 1.68 |
| via The Muse | 5578 | 372 | 4167 | 11.20 |
| via BeBee Portugal | 5493 | 1128 | 4115 | 3.65 |
| via Ai-Jobs.net | 5373 | 1344 | 4059 | 3.02 |
| via Adzuna | 5238 | 2289 | 3856 | 1.68 |
| via Emplois Trabajo.org | 5099 | 2043 | 3816 | 1.87 |
| via Dice | 4493 | 1221 | 3400 | 2.78 |
| via BeBee Belgique | 4421 | 1296 | 3324 | 2.56 |

---

## Exercise 3: Data Scientist Job Market Analysis

**Difficulty:** Medium
**Topics:** INNER JOIN, LIKE pattern matching, WHERE conditions, GROUP BY, HAVING, CASE WHEN, Percentage calculation
**Educational Focus:** Shows how joins enable cross-table analysis by combining job classification data with geographic information. Simplified by removing redundant salary columns and focusing on data availability patterns.

### Problem Statement

Analyze the job market for Data Scientists across different countries. Use the `job_postings` and `locations` tables to find jobs where the `job_title` contains 'Data Scientist'. Your result should show the country (`job_country`), total Data Scientist positions (`data_scientist_positions`), how many have salary data (`positions_with_salary`), and the percentage with salary data (`salary_data_percentage`). Only include countries with at least 100 Data Scientist positions. Order by total positions (highest first) and limit to 15 rows.

### SQL Solution

```sql
SELECT l.job_country,
       COUNT(jp.job_id) AS data_scientist_positions,
       COUNT(CASE WHEN jp.salary_year_avg IS NOT NULL THEN 1 END) AS positions_with_salary,
       ROUND(COUNT(CASE WHEN jp.salary_year_avg IS NOT NULL THEN 1 END) * 100.0 / COUNT(jp.job_id), 2) AS salary_data_percentage
FROM job_postings AS jp
INNER JOIN locations AS l ON jp.job_location = l.job_location
WHERE jp.job_title LIKE '%Data Scientist%'
GROUP BY l.job_country
HAVING COUNT(jp.job_id) >= 100
ORDER BY data_scientist_positions DESC
LIMIT 15;
```

### Results

✅ **Query executed successfully**
- **Execution time:** 0.047s
- **Rows returned:** 20
- **Columns:** job_country, data_scientist_positions, positions_with_salary, salary_data_percentage

#### Top 20 Results

| job_country | data_scientist_positions | positions_with_salary | salary_data_percentage |
| --- | --- | --- | --- |
| United States | 48006 | 3666 | 7.64 |
| Sudan | 29440 | 2351 | 7.99 |
| India | 17950 | 879 | 4.90 |
| United Kingdom | 15883 | 874 | 5.50 |
| France | 14550 | 851 | 5.85 |
| Germany | 13953 | 850 | 6.09 |
| Spain | 13239 | 838 | 6.33 |
| Singapore | 12572 | 837 | 6.66 |
| Netherlands | 12267 | 835 | 6.81 |
| Italy | 12237 | 833 | 6.81 |
| Portugal | 12011 | 839 | 6.99 |
| South Africa | 11800 | 835 | 7.08 |
| Mexico | 11515 | 844 | 7.33 |
| Switzerland | 11350 | 834 | 7.35 |
| Poland | 11288 | 847 | 7.50 |
| Austria | 11185 | 828 | 7.40 |
| Belgium | 11185 | 831 | 7.43 |
| Chile | 11181 | 831 | 7.43 |
| Ireland | 11129 | 832 | 7.48 |
| Canada | 11028 | 853 | 7.73 |

---

## Exercise 4: Employment Type Specialization by Platform

**Difficulty:** Medium
**Topics:** INNER JOIN, CASE WHEN, WHERE IS NOT NULL, GROUP BY, Percentage calculation, NOT IN operator
**Educational Focus:** Reveals platform specialization patterns by combining platform data with employment type information. Enhanced with other_types column to capture all employment data comprehensively.

### Problem Statement

Examine what types of employment (Full-time, Contractor, etc.) different platforms specialize in. Join the `job_platforms` and `job_postings` tables, but only include jobs where `job_schedule_type` is not null. Your result should show the platform name (`platform_name`), total jobs (`total_jobs`), full-time jobs (`fulltime_jobs`), contractor jobs (`contract_jobs`), other employment types (`other_types`), and percentage of contractor jobs (`contract_percentage`). Order by total jobs first (highest first), then by contract percentage (highest first), and limit to 20 rows.

### SQL Solution

```sql
SELECT jpl.platform_name,
       COUNT(jp.job_id) AS total_jobs,
       COUNT(CASE WHEN jp.job_schedule_type = 'Full-time' THEN 1 END) AS fulltime_jobs,
       COUNT(CASE WHEN jp.job_schedule_type = 'Contractor' THEN 1 END) AS contract_jobs,
       COUNT(CASE WHEN jp.job_schedule_type NOT IN ('Full-time', 'Contractor') THEN 1 END) AS other_types,
       ROUND(COUNT(CASE WHEN jp.job_schedule_type = 'Contractor' THEN 1 END) * 100.0 / COUNT(jp.job_id), 2) AS contract_percentage
FROM job_platforms AS jpl
INNER JOIN job_postings AS jp ON jpl.platform_name = jp.job_via
WHERE jp.job_schedule_type IS NOT NULL
GROUP BY jpl.platform_name
ORDER BY total_jobs DESC, contract_percentage DESC
LIMIT 20;
```

### Results

✅ **Query executed successfully**
- **Execution time:** 0.02s
- **Rows returned:** 20
- **Columns:** platform_name, total_jobs, fulltime_jobs, contract_jobs, other_types, contract_percentage

#### Top 20 Results

| platform_name | total_jobs | fulltime_jobs | contract_jobs | other_types | contract_percentage |
| --- | --- | --- | --- | --- | --- |
| via LinkedIn | 135548 | 116025 | 12863 | 6660 | 9.49 |
| via BeBee | 76052 | 70066 | 898 | 5088 | 1.18 |
| via Trabajo.org | 46227 | 45547 | 1 | 679 | 0 |
| via Indeed | 31597 | 28447 | 1283 | 1867 | 4.06 |
| via Recruit.net | 17763 | 16274 | 1080 | 409 | 6.08 |
| via ZipRecruiter | 11540 | 10372 | 628 | 540 | 5.44 |
| via Jobs Trabajo.org | 7915 | 7542 | 0 | 373 | 0 |
| via Trabajo.org - Vacantes De Empleo, Trabajo | 6664 | 6619 | 1 | 44 | 0.02 |
| via BeBee India | 6467 | 6228 | 40 | 199 | 0.62 |
| via BeBee Singapore | 5862 | 4491 | 983 | 388 | 16.77 |
| via SimplyHired | 4894 | 4497 | 152 | 245 | 3.11 |
| via Jobrapido.com | 4646 | 4336 | 85 | 225 | 1.83 |
| via Sercanto | 4230 | 4117 | 26 | 87 | 0.61 |
| via The Muse | 4152 | 3977 | 19 | 156 | 0.46 |
| via BeBee Portugal | 4099 | 3959 | 32 | 108 | 0.78 |
| via Ai-Jobs.net | 4048 | 3795 | 56 | 197 | 1.38 |
| via Adzuna | 3855 | 3710 | 0 | 145 | 0 |
| via Emplois Trabajo.org | 3811 | 3696 | 0 | 115 | 0 |
| via Dice | 3400 | 1503 | 1759 | 138 | 51.74 |
| via BeBee Belgique | 3234 | 3007 | 54 | 173 | 1.67 |

---

## Exercise 5: Global Company Expansion Analysis

**Difficulty:** Hard
**Topics:** INNER JOIN, LEFT JOIN, COUNT DISTINCT, GROUP BY, HAVING, Multiple conditions
**Educational Focus:** Demonstrates complex multi-table joins to analyze company expansion patterns across geographic markets

### Problem Statement

Find companies that operate in many different places around the world. Use the `companies`, `job_postings`, and `locations` tables. Your result should show the company name (`company_name`), number of different locations (`unique_locations`), number of different countries (`unique_countries`), and total jobs posted (`total_jobs`). Only include companies with at least 10 different locations AND at least 100 total jobs. Order by unique locations first (highest first), then by unique countries (highest first), and limit to 20 rows.

### SQL Solution

```sql
SELECT c.company_name,
       COUNT(DISTINCT l.job_location) AS unique_locations,
       COUNT(DISTINCT l.job_country) AS unique_countries,
       COUNT(jp.job_id) AS total_jobs
FROM companies AS c
INNER JOIN job_postings AS jp ON c.company_name = jp.company_name
LEFT JOIN locations AS l ON jp.job_location = l.job_location
GROUP BY c.company_name
HAVING COUNT(DISTINCT l.job_location) >= 10 AND COUNT(jp.job_id) >= 100
ORDER BY unique_locations DESC, unique_countries DESC
LIMIT 20;
```

### Results

✅ **Query executed successfully**
- **Execution time:** 0.125s
- **Rows returned:** 20
- **Columns:** company_name, unique_locations, unique_countries, total_jobs

#### Top 20 Results

| company_name | unique_locations | unique_countries | total_jobs |
| --- | --- | --- | --- |
| Dice | 215 | 73 | 81307 |
| Randstad | 212 | 73 | 2133 |
| Robert Half | 199 | 73 | 12881 |
| Deloitte | 197 | 76 | 2325 |
| Accenture | 191 | 75 | 3194 |
| Michael Page | 190 | 74 | 4449 |
| Capgemini | 183 | 74 | 3178 |
| EY | 159 | 77 | 2244 |
| SynergisticIT | 153 | 73 | 3532 |
| Experis | 144 | 73 | 2375 |
| IBM | 143 | 73 | 2240 |
| Amazon | 142 | 77 | 2423 |
| TEKsystems | 142 | 73 | 3523 |
| PwC | 136 | 76 | 1867 |
| Harnham | 126 | 73 | 24495 |
| CGI | 125 | 73 | 3947 |
| ClickJobs.io | 121 | 73 | 2732 |
| Cognizant | 118 | 74 | 4137 |
| Diverse Lynx | 117 | 73 | 1769 |
| IQVIA | 113 | 76 | 2294 |

---

## Exercise 6: Platform Market Leadership Analysis (Advanced)

**Difficulty:** Hard
**Topics:** Common Table Expressions (CTE), Window Functions, ROW_NUMBER() OVER(), PARTITION BY, INNER JOIN, GROUP BY, HAVING, Subqueries
**Educational Focus:** Advanced exercise demonstrating window functions and CTEs to analyze market leadership patterns. Shows which platforms dominate in the most countries, revealing global platform strategies.

### Problem Statement

This is an advanced exercise using window functions. Find which platform is the #1 leader in each country, then count how many countries each platform leads. First, create a ranking of platforms within each country based on job count. Then, select only the #1 platform per country and count how many countries each platform leads. Your result should show platform name (`platform_name`), number of countries led (`countries_led`), and market share percentage (`market_share_percentage`). Only include platforms with at least 10 jobs per country. Order by countries led (highest first) and limit to 15 rows.

### SQL Solution

```sql
WITH platform_rankings AS (
  SELECT 
    l.job_country,
    jp.job_via AS platform_name,
    COUNT(jp.job_id) AS platform_jobs,
    ROW_NUMBER() OVER (PARTITION BY l.job_country ORDER BY COUNT(jp.job_id) DESC) AS country_rank
  FROM locations AS l
  INNER JOIN job_postings AS jp ON l.job_location = jp.job_location
  GROUP BY l.job_country, jp.job_via
  HAVING COUNT(jp.job_id) >= 10
)
SELECT 
  platform_name,
  COUNT(*) AS countries_led,
  ROUND(COUNT(*) * 100.0 / (SELECT COUNT(DISTINCT job_country) FROM platform_rankings WHERE country_rank = 1), 2) AS market_share_percentage
FROM platform_rankings
WHERE country_rank = 1
GROUP BY platform_name
ORDER BY countries_led DESC
LIMIT 15;
```

### Results

✅ **Query executed successfully**
- **Execution time:** 0.043s
- **Rows returned:** 20
- **Columns:** platform_name, countries_led, market_share_percentage

#### Top 20 Results

| platform_name | countries_led | market_share_percentage |
| --- | --- | --- |
| via LinkedIn | 75 | 72.12 |
| via Emplois Trabajo.org | 3 | 2.88 |
| via Trabajo.org | 3 | 2.88 |
| via Nexxt | 2 | 1.92 |
| via Sercanto | 1 | 0.96 |
| via LinkedIn Guatemala | 1 | 0.96 |
| via LinkedIn Cambodia | 1 | 0.96 |
| via LinkedIn Albania | 1 | 0.96 |
| via BeBee Kenya | 1 | 0.96 |
| via Great Zambia Jobs | 1 | 0.96 |
| via LinkedIn Maurice | 1 | 0.96 |
| via LinkedIn Ethiopia | 1 | 0.96 |
| via BeBee الكويت | 1 | 0.96 |
| via LinkedIn Macedonia | 1 | 0.96 |
| via LinkedIn Nepal | 1 | 0.96 |
| via LinkedIn Senegal | 1 | 0.96 |
| via Intellijobs.ai | 1 | 0.96 |
| via Whatjobs? Jobs In The Uganda | 1 | 0.96 |
| via 242 Jobs | 1 | 0.96 |
| via LinkedIn Azerbaijan | 1 | 0.96 |

---
