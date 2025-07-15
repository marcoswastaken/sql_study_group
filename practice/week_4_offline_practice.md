# Week 4 Practice

The data cards for a collection of tables is provided. For each exercise, come up with a SQL query that addresses the problem statement.

## 📚 Data Dictionary

### companies
**Row Count:** 111,985

| Column | Type | Nullable | Key | Description |
|--------|------|----------|-----|-------------|
| company_id | BIGINT | Yes |  | Unique identifier for each company, generated as a sequential number for JOIN operations |
| company_name | VARCHAR | Yes |  | Name of the company that posted job listings, ranging from startups to Fortune 500 companies |
| total_jobs | BIGINT | Yes |  | Total number of job postings from this company in the dataset, useful for analyzing employer activity |

### job_platforms
**Row Count:** 7,112

| Column | Type | Nullable | Key | Description |
|--------|------|----------|-----|-------------|
| platform_id | BIGINT | Yes |  | Unique identifier for each job platform, used as primary key for JOIN operations |
| platform_name | VARCHAR | Yes |  | Name of the job platform (e.g., 'via LinkedIn', 'via Indeed', 'via Glassdoor') |
| jobs_posted | BIGINT | Yes |  | Total number of job postings from this platform in the dataset, useful for platform popularity analysis |

### job_postings
**Row Count:** 589,306

| Column | Type | Nullable | Key | Description |
|--------|------|----------|-----|-------------|
| job_id | BIGINT | Yes |  | Unique identifier for each job posting, serves as primary key for the table |
| job_title_short | VARCHAR | Yes |  | Standardized job title category for easier grouping and analysis |
| job_title | VARCHAR | Yes |  | Full job title as posted by the employer |
| job_schedule_type | VARCHAR | Yes |  | Employment type (Full-time, Part-time, Contract, Contractor) |
| job_work_from_home | BOOLEAN | Yes |  | Boolean flag indicating remote work availability |
| job_posted_date | VARCHAR | Yes |  | Date and time when the job was posted, enables time-based analysis |
| job_no_degree_mention | BOOLEAN | Yes |  | Boolean flag indicating whether degree requirements are mentioned |
| job_health_insurance | BOOLEAN | Yes |  | Boolean flag indicating whether health insurance benefits are mentioned |
| salary_year_avg | DOUBLE | Yes |  | Average yearly salary when available, useful for salary analysis |
| salary_hour_avg | DOUBLE | Yes |  | Average hourly wage when available, useful for contract position analysis |
| company_name | VARCHAR | Yes |  | Name of the company posting the job, can be used for JOINs with companies table |
| job_location | VARCHAR | Yes |  | Location where the job is based, used for geographic analysis |
| job_via | VARCHAR | Yes |  | Platform where the job was posted, can be used for JOINs with job_platforms table |

### locations
**Row Count:** 1,318

| Column | Type | Nullable | Key | Description |
|--------|------|----------|-----|-------------|
| location_id | BIGINT | Yes |  | Unique identifier for each location, serves as primary key for location-based JOINs |
| job_location | VARCHAR | Yes |  | City and state/province where jobs are located, providing geographic granularity |
| job_country | VARCHAR | Yes |  | Country where the jobs are located, enables country-level analysis |
| job_count | BIGINT | Yes |  | Total number of jobs posted in this location, useful for market size analysis |

### salary_ranges
**Row Count:** 4

| Column | Type | Nullable | Key | Description |
|--------|------|----------|-----|-------------|
| range_id | BIGINT | Yes |  | Unique identifier for each salary range, serves as primary key |
| range_name | VARCHAR | Yes |  | Descriptive name for the salary range (e.g., 'Entry Level', 'Mid Level') |
| min_salary | INTEGER | Yes |  | Minimum salary amount for this range in USD |
| max_salary | INTEGER | Yes |  | Maximum salary amount for this range in USD |
| experience_level | VARCHAR | Yes |  | Experience level associated with this salary range (Junior, Mid, Senior, Executive) |

---

## 🎯 Practice Exercises

### Exercise 1: Platform Competition Analysis

**Problem Statement:**
Find out which job platforms are most active in different countries. The `locations` table contains country information, and `job_postings` contains which platform each job came from. Your result should show the country name (`job_country`), platform name (`job_via` AS `platform_name`), and how many jobs that platform posted in that country (`platform_jobs_in_country`). Only include platform-country combinations with at least 20 jobs. Order by country first, then by job count (highest first), and limit to 30 rows.

---

### Exercise 2: Platform Business Model Analysis

**Problem Statement:**
Compare job platforms to understand their business models. The `job_platforms` table shows each platform's total capacity, while `job_postings` shows actual usage. Your result should show the platform name (`platform_name`), total capacity (`jobs_posted` AS `platform_capacity`), number of different companies using the platform (`unique_companies`), actual jobs posted (`actual_jobs_posted`), and average jobs per company (`avg_jobs_per_company`). Only include platforms with at least 1000 actual jobs posted. Order by actual jobs posted (highest first) and limit to 15 rows.

---

### Exercise 3: Data Scientist Job Market Analysis

**Problem Statement:**
Analyze the job market for Data Scientists across different countries. Use the `job_postings` and `locations` tables to find jobs where the `job_title` contains 'Data Scientist'. Your result should show the country (`job_country`), total Data Scientist positions (`data_scientist_positions`), how many have salary data (`positions_with_salary`), and the percentage with salary data (`salary_data_percentage`). Only include countries with at least 100 Data Scientist positions. Order by total positions (highest first) and limit to 15 rows.

---

### Exercise 4: Employment Type Specialization by Platform

**Problem Statement:**
Examine what types of employment (Full-time, Contractor, etc.) different platforms specialize in. Join the `job_platforms` and `job_postings` tables, but only include jobs where `job_schedule_type` is not null. Your result should show the platform name (`platform_name`), total jobs (`total_jobs`), full-time jobs (`fulltime_jobs`), contractor jobs (`contract_jobs`), other employment types (`other_types`), and percentage of contractor jobs (`contract_percentage`). Order by total jobs first (highest first), then by contract percentage (highest first), and limit to 20 rows.

---

### Exercise 5: Global Company Expansion Analysis

**Problem Statement:**
Find companies that operate in many different places around the world. Use the `companies`, `job_postings`, and `locations` tables. Your result should show the company name (`company_name`), number of different locations (`unique_locations`), number of different countries (`unique_countries`), and total jobs posted (`total_jobs`). Only include companies with at least 10 different locations AND at least 100 total jobs. Order by unique locations first (highest first), then by unique countries (highest first), and limit to 20 rows.

---

### Exercise 6: Platform Market Leadership Analysis (Advanced)

**Problem Statement:**
Find which platform is the #1 leader in each country, then count how many countries each platform leads. First, create a ranking of platforms within each country based on job count. Then, select only the #1 platform per country and count how many countries each platform leads. Your result should show platform name (`platform_name`), number of countries led (`countries_led`), and market share percentage (`market_share_percentage`). Only include platforms with at least 10 jobs per country. Order by countries led (highest first) and limit to 15 rows.

---
