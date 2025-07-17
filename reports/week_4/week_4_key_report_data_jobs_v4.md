# Week 4 Practice - Data Jobs Dataset (Ultra-Refined v4)

**Description:** JOIN operations that combine information from different tables to reveal business insights impossible to obtain from individual tables
**Database:** data_jobs.db
**Total Exercises:** 6
**Focus Topics:** INNER JOIN, LEFT JOIN, Table aliases, Cross-table analysis, Business insights, Window functions (advanced)

*Report generated on: 2025-07-16 20:12:58*

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
| Albania | via LinkedIn Albania | 40 |
| Argentina | via LinkedIn | 30541 |
| Argentina | via Indeed | 4408 |
| Argentina | via BeBee | 2567 |
| Argentina | via ZipRecruiter | 2094 |
| Argentina | via Jobgether | 1524 |
| Argentina | via Recruit.net | 1474 |
| Argentina | via Trabajo.org - Vacantes De Empleo, Trabajo | 1157 |
| Argentina | via Upwork | 1022 |
| Argentina | via hh.ru | 629 |
| Argentina | via Linkedin | 627 |
| Argentina | via Snagajob | 620 |
| Argentina | via Startup Jobs | 575 |
| Argentina | via JobTeaser | 410 |
| Argentina | via HelloWork | 398 |
| Argentina | via Trabajo.org | 363 |
| Argentina | via Get.It | 345 |
| Argentina | via Totaljobs | 344 |
| Argentina | via Sercanto | 322 |
| Argentina | via Dice | 302 |

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
- **Execution time:** 0.029s
- **Rows returned:** 20
- **Columns:** platform_name, platform_capacity, unique_companies, actual_jobs_posted, avg_jobs_per_company

#### Top 20 Results

| platform_name | platform_capacity | unique_companies | actual_jobs_posted | avg_jobs_per_company |
| --- | --- | --- | --- | --- |
| via LinkedIn | 186679 | 38014 | 139951 | 3.68 |
| via BeBee | 103507 | 26651 | 77504 | 2.91 |
| via Trabajo.org | 61562 | 18572 | 46277 | 2.49 |
| via Recruit.net | 23646 | 8019 | 17730 | 2.21 |
| via ZipRecruiter | 15533 | 4694 | 11600 | 2.47 |
| via Jobs Trabajo.org | 10605 | 4739 | 7966 | 1.68 |
| via Snagajob | 9355 | 1418 | 6993 | 4.93 |
| via Trabajo.org - Vacantes De Empleo, Trabajo | 8919 | 1793 | 6606 | 3.68 |
| via BeBee India | 8642 | 2895 | 6468 | 2.23 |
| via BeBee Singapore | 7985 | 2920 | 6009 | 2.06 |
| via SimplyHired | 6632 | 3457 | 5009 | 1.45 |
| via Jobrapido.com | 6202 | 2730 | 4637 | 1.70 |
| via Sercanto | 5691 | 2504 | 4221 | 1.69 |
| via The Muse | 5578 | 378 | 4203 | 11.12 |
| via BeBee Portugal | 5493 | 1114 | 4108 | 3.69 |
| via Ai-Jobs.net | 5373 | 1334 | 4027 | 3.02 |
| via Adzuna | 5238 | 2284 | 3947 | 1.73 |
| via Emplois Trabajo.org | 5099 | 2050 | 3830 | 1.87 |
| via BeBee Canada | 4668 | 1814 | 3477 | 1.92 |
| via Dice | 4493 | 1248 | 3391 | 2.72 |

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
- **Execution time:** 0.018s
- **Rows returned:** 20
- **Columns:** job_country, data_scientist_positions, positions_with_salary, salary_data_percentage

#### Top 20 Results

| job_country | data_scientist_positions | positions_with_salary | salary_data_percentage |
| --- | --- | --- | --- |
| United States | 47966 | 3667 | 7.64 |
| Sudan | 29381 | 2334 | 7.94 |
| India | 18026 | 877 | 4.87 |
| United Kingdom | 15888 | 883 | 5.56 |
| France | 14559 | 855 | 5.87 |
| Germany | 14023 | 849 | 6.05 |
| Spain | 13294 | 841 | 6.33 |
| Singapore | 12629 | 844 | 6.68 |
| Italy | 12276 | 831 | 6.77 |
| Netherlands | 12258 | 838 | 6.84 |
| Portugal | 12066 | 840 | 6.96 |
| South Africa | 11817 | 839 | 7.10 |
| Mexico | 11508 | 847 | 7.36 |
| Switzerland | 11375 | 833 | 7.32 |
| Poland | 11334 | 852 | 7.52 |
| Chile | 11201 | 833 | 7.44 |
| Austria | 11192 | 829 | 7.41 |
| Belgium | 11160 | 832 | 7.46 |
| Ireland | 11147 | 831 | 7.45 |
| Canada | 11062 | 855 | 7.73 |

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
- **Execution time:** 0.015s
- **Rows returned:** 20
- **Columns:** platform_name, total_jobs, fulltime_jobs, contract_jobs, other_types, contract_percentage

#### Top 20 Results

| platform_name | total_jobs | fulltime_jobs | contract_jobs | other_types | contract_percentage |
| --- | --- | --- | --- | --- | --- |
| via LinkedIn | 135706 | 116039 | 12905 | 6762 | 9.51 |
| via BeBee | 75968 | 70044 | 889 | 5035 | 1.17 |
| via Trabajo.org | 46239 | 45557 | 1 | 681 | 0 |
| via Recruit.net | 17657 | 16153 | 1076 | 428 | 6.09 |
| via ZipRecruiter | 11514 | 10323 | 624 | 567 | 5.42 |
| via Jobs Trabajo.org | 7962 | 7607 | 0 | 355 | 0 |
| via Snagajob | 6993 | 5736 | 0 | 1257 | 0 |
| via Trabajo.org - Vacantes De Empleo, Trabajo | 6606 | 6559 | 1 | 46 | 0.02 |
| via BeBee India | 6455 | 6225 | 43 | 187 | 0.67 |
| via BeBee Singapore | 5996 | 4639 | 965 | 392 | 16.09 |
| via SimplyHired | 4963 | 4572 | 164 | 227 | 3.30 |
| via Jobrapido.com | 4573 | 4256 | 88 | 229 | 1.92 |
| via Sercanto | 4188 | 4062 | 29 | 97 | 0.69 |
| via The Muse | 4186 | 4010 | 23 | 153 | 0.55 |
| via BeBee Portugal | 4092 | 3943 | 31 | 118 | 0.76 |
| via Ai-Jobs.net | 4015 | 3760 | 57 | 198 | 1.42 |
| via Adzuna | 3947 | 3799 | 0 | 148 | 0 |
| via Emplois Trabajo.org | 3824 | 3713 | 0 | 111 | 0 |
| via BeBee Canada | 3402 | 3157 | 123 | 122 | 3.62 |
| via Dice | 3391 | 1499 | 1742 | 150 | 51.37 |

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
       COUNT(DISTINCT jp.job_location) AS unique_locations,
       COUNT(DISTINCT l.job_country) AS unique_countries,
       COUNT(jp.job_id) AS total_jobs
FROM companies AS c
INNER JOIN job_postings AS jp ON c.company_name = jp.company_name
LEFT JOIN locations AS l ON jp.job_location = l.job_location
WHERE jp.job_location NOT IN ('Remote', 'Anywhere', 'N/A', 'Various', 'Multiple Locations', 'Worldwide')
  AND jp.job_location IS NOT NULL
GROUP BY c.company_name
HAVING COUNT(DISTINCT jp.job_location) >= 10 AND COUNT(jp.job_id) >= 100
ORDER BY unique_locations DESC, unique_countries DESC
LIMIT 20;
```

### Results

✅ **Query executed successfully**
- **Execution time:** 0.057s
- **Rows returned:** 20
- **Columns:** company_name, unique_locations, unique_countries, total_jobs

#### Top 20 Results

| company_name | unique_locations | unique_countries | total_jobs |
| --- | --- | --- | --- |
| Robert Half | 336 | 18 | 1514 |
| Insight Global | 326 | 6 | 1890 |
| Guidehouse | 304 | 3 | 1607 |
| SynergisticIT | 290 | 2 | 1541 |
| Randstad | 289 | 35 | 1074 |
| Dice | 288 | 6 | 1518 |
| Michael Page | 278 | 38 | 1297 |
| Capital One | 273 | 6 | 1948 |
| Deloitte | 248 | 46 | 1633 |
| Hays | 222 | 32 | 925 |
| Citi | 218 | 29 | 2126 |
| Accenture | 215 | 49 | 1298 |
| Capgemini | 209 | 36 | 1210 |
| EY | 201 | 51 | 848 |
| Leidos | 200 | 14 | 957 |
| Experis | 191 | 25 | 756 |
| Flexjobs | 191 | 3 | 200 |
| PwC | 180 | 41 | 636 |
| Harnham | 173 | 12 | 1883 |
| Walmart | 169 | 8 | 1930 |

---

## Exercise 6: Platform Market Leadership Analysis (Advanced)

**Difficulty:** Hard
**Topics:** Common Table Expressions (CTE), Window Functions, ROW_NUMBER() OVER(), PARTITION BY, INNER JOIN, GROUP BY, HAVING, Subqueries
**Educational Focus:** Advanced exercise demonstrating window functions and CTEs to analyze market leadership patterns. Shows which platforms dominate in the most countries, revealing global platform strategies.

### Problem Statement

Find which platform is the #1 leader in each country, then count how many countries each platform leads. First, create a ranking of platforms within each country based on job count. Then, select only the #1 platform per country and count how many countries each platform leads. Your result should show platform name (`platform_name`), number of countries led (`countries_led`), and market share percentage (`market_share_percentage`). Only include platforms with at least 10 jobs per country. Order by countries led (highest first) and limit to 15 rows.

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
- **Execution time:** 0.042s
- **Rows returned:** 20
- **Columns:** platform_name, countries_led, market_share_percentage

#### Top 20 Results

| platform_name | countries_led | market_share_percentage |
| --- | --- | --- |
| via LinkedIn | 75 | 71.43 |
| via Trabajo.org | 4 | 3.81 |
| via Emplois Trabajo.org | 3 | 2.86 |
| via Nexxt | 2 | 1.90 |
| via Sercanto | 1 | 0.95 |
| via LinkedIn Guatemala | 1 | 0.95 |
| via LinkedIn Cambodia | 1 | 0.95 |
| via WhatJobs | 1 | 0.95 |
| via Great Zambia Jobs | 1 | 0.95 |
| via LinkedIn Maurice | 1 | 0.95 |
| via LinkedIn Albania | 1 | 0.95 |
| via BeBee | 1 | 0.95 |
| via LinkedIn Ethiopia | 1 | 0.95 |
| via Intellijobs.ai | 1 | 0.95 |
| via LinkedIn Senegal | 1 | 0.95 |
| via BeBee Kenya | 1 | 0.95 |
| via Rabota.md | 1 | 0.95 |
| via LinkedIn Macedonia | 1 | 0.95 |
| via LinkedIn Nepal | 1 | 0.95 |
| via 242 Jobs | 1 | 0.95 |

---
