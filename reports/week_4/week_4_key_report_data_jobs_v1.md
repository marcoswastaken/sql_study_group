# Week 4 Practice - Data Jobs Dataset

**Description:** JOIN operations on real-world data job postings
**Database:** data_jobs.db
**Total Exercises:** 8
**Focus Topics:** INNER JOIN, LEFT JOIN, Table aliases, Primary/Foreign keys

*Report generated on: 2025-07-12 00:24:19*

---

## Exercise 1: Company Job Postings

**Difficulty:** Easy
**Topics:** INNER JOIN, Table aliases, WHERE clause, ORDER BY
**Educational Focus:** Basic INNER JOIN syntax with table aliases

### Problem Statement

Find all Data Scientist job postings along with company names. Show the job title, company name, and posted date. Use INNER JOIN to only show jobs that have company information.

### SQL Solution

```sql
SELECT jp.job_title, c.company_name, jp.job_posted_date
FROM job_postings AS jp
INNER JOIN companies AS c ON jp.company_name = c.company_name
WHERE jp.job_title_short = 'Data Scientist'
ORDER BY jp.job_posted_date DESC
LIMIT 10;
```

### Results

✅ **Query executed successfully**
- **Execution time:** 0.106s
- **Rows returned:** 20
- **Columns:** job_title, company_name, job_posted_date

#### Top 20 Results

| job_title | company_name | job_posted_date |
| --- | --- | --- |
| Data Scientist III with Security Clearance | ManTech International | 2023-12-31 23:40:03 |
| Data Scientist II with Security Clearance | ManTech International | 2023-12-31 23:40:03 |
| Data Scientist with Security Clearance | CACI | 2023-12-31 23:40:00 |
| Data scientist | Cognizant Technology Solutions | 2023-12-31 23:40:00 |
| Principal data scientist experimentation personalization | Jobzem (7580326) | 2023-12-31 23:37:30 |
| Digital Analytics Specialist | Verndale | 2023-12-31 23:36:27 |
| Instructor of Data Science | Credence Management Solutions, LLC | 2023-12-31 23:31:59 |
| Lead Data Scientist | Vistra Corporate Services Company | 2023-12-31 23:31:54 |
| Sr. Data Scientist (Modeling) with Security Clearance | CACI | 2023-12-31 23:01:00 |
| Data Scientist | ekom21 - KGRZ Hessen | 2023-12-31 22:27:02 |
| Manager, Data Science | Atlassian | 2023-12-31 22:00:43 |
| Data Scientist | IBM | 2023-12-31 20:26:59 |
| Data Scientist-International E-commerce | Byte Dance | 2023-12-31 20:07:41 |
| Lead Data Scientist | Epsilon India | 2023-12-31 20:05:32 |
| Cleared Workforce Analytics Consultant | Guidehouse | 2023-12-31 20:01:00 |
| Data scientist with deep learning expertise to help in research paper | Upwork | 2023-12-31 20:00:51 |
| Director, Data Scientist | Prudential Financial, Inc. | 2023-12-31 20:00:32 |
| Data Scientist | Alp Consulting Ltd. | 2023-12-31 19:05:32 |
| AI Engineer / Data Scientist with NLP Expertise - Contract to Hire | Upwork | 2023-12-31 18:40:00 |
| Analysts | Consafe Logistics | 2023-12-31 18:28:32 |

---

## Exercise 2: All Companies with Job Counts

**Difficulty:** Medium
**Topics:** LEFT JOIN, COUNT, GROUP BY, Table aliases
**Educational Focus:** LEFT JOIN to include all records from left table, handling NULLs

### Problem Statement

List all companies and count how many job postings they have. Include companies even if they don't have any job postings in the job_postings table (show 0 for them). Use LEFT JOIN to ensure all companies are included.

### SQL Solution

```sql
SELECT c.company_name, COUNT(jp.job_id) AS job_count
FROM companies AS c
LEFT JOIN job_postings AS jp ON c.company_name = jp.company_name
GROUP BY c.company_name
ORDER BY job_count DESC
LIMIT 20;
```

### Results

✅ **Query executed successfully**
- **Execution time:** 0.025s
- **Rows returned:** 20
- **Columns:** company_name, job_count

#### Top 20 Results

| company_name | job_count |
| --- | --- |
| Emprego | 4962 |
| Booz Allen Hamilton | 2198 |
| Dice | 2139 |
| Harnham | 1902 |
| Citi | 1611 |
| Confidenziale | 1525 |
| Listopro | 1511 |
| Capital One | 1446 |
| Walmart | 1431 |
| Robert Half | 1374 |
| UnitedHealth Group | 1350 |
| Michael Page | 1318 |
| Guidehouse | 1270 |
| Accenture | 1258 |
| Deloitte | 1245 |
| SynergisticIT | 1144 |
| Capgemini | 1111 |
| Randstad | 1051 |
| Upwork | 1035 |
| Amazon | 954 |

---

## Exercise 3: Platform Job Distribution

**Difficulty:** Medium
**Topics:** INNER JOIN, COUNT, GROUP BY, WHERE clause
**Educational Focus:** INNER JOIN with aggregation and filtering

### Problem Statement

Show which job platforms are posting the most Data Engineer jobs. Include platform name and job count. Use INNER JOIN to connect job postings with platforms.

### SQL Solution

```sql
SELECT jpl.platform_name, COUNT(jp.job_id) AS job_count
FROM job_platforms AS jpl
INNER JOIN job_postings AS jp ON jpl.platform_name = jp.job_via
WHERE jp.job_title_short = 'Data Engineer'
GROUP BY jpl.platform_name
ORDER BY job_count DESC
LIMIT 10;
```

### Results

✅ **Query executed successfully**
- **Execution time:** 0.006s
- **Rows returned:** 20
- **Columns:** platform_name, job_count

#### Top 20 Results

| platform_name | job_count |
| --- | --- |
| via LinkedIn | 44075 |
| via BeBee | 13518 |
| via Indeed | 8465 |
| via Trabajo.org | 6819 |
| via Recruit.net | 3828 |
| via ZipRecruiter | 2311 |
| via BeBee India | 1766 |
| via SimplyHired | 1553 |
| via Jobrapido.com | 1452 |
| via BeBee Singapore | 1269 |
| via Jobs Trabajo.org | 1255 |
| via Dice | 1182 |
| via Trabajo.org - Vacantes De Empleo, Trabajo | 1112 |
| via hh.ru | 1108 |
| via Sercanto | 1018 |
| via Adzuna | 946 |
| via The Muse | 924 |
| via Emplois Trabajo.org | 918 |
| via Ai-Jobs.net | 852 |
| via WJHL Jobs | 834 |

---

## Exercise 4: Jobs by Location

**Difficulty:** Medium
**Topics:** LEFT JOIN, WHERE IN, ORDER BY, Table aliases
**Educational Focus:** LEFT JOIN with multiple column sorting and filtering

### Problem Statement

List all job postings with their location details. Show job title, location, and country. Use LEFT JOIN to include jobs even if location information is missing.

### SQL Solution

```sql
SELECT jp.job_title_short, jp.job_location, l.job_country
FROM job_postings AS jp
LEFT JOIN locations AS l ON jp.job_location = l.job_location
WHERE jp.job_title_short IN ('Data Scientist', 'Data Engineer', 'Data Analyst')
ORDER BY l.job_country, jp.job_location
LIMIT 15;
```

### Results

✅ **Query executed successfully**
- **Execution time:** 0.013s
- **Rows returned:** 20
- **Columns:** job_title_short, job_location, job_country

#### Top 20 Results

| job_title_short | job_location | job_country |
| --- | --- | --- |
| Data Engineer | Tirana, Albania | Albania |
| Data Analyst | Tirana, Albania | Albania |
| Data Analyst | Tirana, Albania | Albania |
| Data Analyst | Tirana, Albania | Albania |
| Data Analyst | Tirana, Albania | Albania |
| Data Analyst | Tirana, Albania | Albania |
| Data Engineer | Tirana, Albania | Albania |
| Data Analyst | Tirana, Albania | Albania |
| Data Scientist | Tirana, Albania | Albania |
| Data Engineer | Tirana, Albania | Albania |
| Data Analyst | Tirana, Albania | Albania |
| Data Engineer | Tirana, Albania | Albania |
| Data Analyst | Tirana, Albania | Albania |
| Data Analyst | Tirana, Albania | Albania |
| Data Analyst | Tirana, Albania | Albania |
| Data Analyst | Tirana, Albania | Albania |
| Data Scientist | Tirana, Albania | Albania |
| Data Analyst | Tirana, Albania | Albania |
| Data Engineer | Tirana, Albania | Albania |
| Data Analyst | Tirana, Albania | Albania |

---

## Exercise 5: Salary Range Classification

**Difficulty:** Hard
**Topics:** INNER JOIN, BETWEEN, IS NOT NULL, Table aliases
**Educational Focus:** Conditional JOIN using BETWEEN clause

### Problem Statement

Classify Data Scientist jobs by salary ranges. Show job title, salary, and experience level. Use a conditional JOIN to match salaries with appropriate ranges.

### SQL Solution

```sql
SELECT jp.job_title, jp.salary_year_avg, sr.range_name, sr.experience_level
FROM job_postings AS jp
INNER JOIN salary_ranges AS sr ON jp.salary_year_avg BETWEEN sr.min_salary AND sr.max_salary
WHERE jp.job_title_short = 'Data Scientist'
  AND jp.salary_year_avg IS NOT NULL
ORDER BY jp.salary_year_avg DESC
LIMIT 10;
```

### Results

✅ **Query executed successfully**
- **Execution time:** 0.005s
- **Rows returned:** 20
- **Columns:** job_title, salary_year_avg, range_name, experience_level

#### Top 20 Results

| job_title | salary_year_avg | range_name | experience_level |
| --- | --- | --- | --- |
| Geographic Information Systems Analyst - GIS Analyst | 585000 | Executive | Executive |
| Staff Data Scientist/Quant Researcher | 550000 | Executive | Executive |
| Staff Data Scientist - Business Analytics | 525000 | Executive | Executive |
| Data Scientist (L5) - Member Product | 450000 | Executive | Executive |
| Applied Data Science or Machine Learning Leader | 425000 | Executive | Executive |
| Director of Data Science (Hybrid) | 375000 | Executive | Executive |
| Director, Data Scientist | 375000 | Executive | Executive |
| Director of Data Science | 375000 | Executive | Executive |
| Data Scientist | 375000 | Executive | Executive |
| Director, Data Science & Advanced Analytics | 375000 | Executive | Executive |
| Director, Data Science & Customer Analytics | 375000 | Executive | Executive |
| Director , Data Science | 375000 | Executive | Executive |
| Data Science Director | 375000 | Executive | Executive |
| Director Data Science | 375000 | Executive | Executive |
| Data Scientist SME | 375000 | Executive | Executive |
| Data Scientist | 375000 | Executive | Executive |
| Data Scientist | 375000 | Executive | Executive |
| Data Scientist | 375000 | Executive | Executive |
| Data Scientist | 375000 | Executive | Executive |
| VP Data Science | 375000 | Executive | Executive |

---

## Exercise 6: Comprehensive Job Analysis

**Difficulty:** Hard
**Topics:** Multiple JOINs, INNER JOIN, LEFT JOIN, WHERE clause
**Educational Focus:** Combining multiple JOIN types in a single query

### Problem Statement

Create a comprehensive report showing job title, company name, location, country, and platform for Data Analyst positions. Use multiple JOINs to combine information from different tables.

### SQL Solution

```sql
SELECT jp.job_title, c.company_name, jp.job_location, l.job_country, jp.job_via
FROM job_postings AS jp
INNER JOIN companies AS c ON jp.company_name = c.company_name
LEFT JOIN locations AS l ON jp.job_location = l.job_location
WHERE jp.job_title_short = 'Data Analyst'
  AND jp.job_location IS NOT NULL
ORDER BY l.job_country, jp.job_location
LIMIT 12;
```

### Results

✅ **Query executed successfully**
- **Execution time:** 0.024s
- **Rows returned:** 20
- **Columns:** job_title, company_name, job_location, job_country, job_via

#### Top 20 Results

| job_title | company_name | job_location | job_country | job_via |
| --- | --- | --- | --- | --- |
| Data Analyst | Intercom Data Service Group | Tirana, Albania | Albania | via LinkedIn Albania |
| GIS Data Analyst | INOVA \| Software Development Company | Tirana, Albania | Albania | via LinkedIn Albania |
| Data Analyst | We Are Fiber | Tirana, Albania | Albania | via LinkedIn Albania |
| Data Analytics Specialist With SQL & Tableau | AUTO1 Group | Tirana, Albania | Albania | via Ai-Jobs.net |
| Data Analyst | AUTO1 Group | Tirana, Albania | Albania | via LinkedIn Albania |
| Data Analyst | Bulls Media Albania | Tirana, Albania | Albania | via LinkedIn Albania |
| Junior Data Quality Specialist with financial background | AUTO1 Group | Tirana, Albania | Albania | via Ai-Jobs.net |
| Data Analyst | iKanbi Albania Sh.a. | Tirana, Albania | Albania | via LinkedIn |
| Data Analyst | BI2Value GmbH | Tirana, Albania | Albania | via LinkedIn Albania |
| Data Migration Analyst \| Digital Banking Solutions | Deloitte | Tirana, Albania | Albania | via LinkedIn Albania |
| Lead Data Analyst | Partner.al SHPK | Tirana, Albania | Albania | via LinkedIn Albania |
| Data Analyst and Hr assistente | Eurostep Commerce | Tirana, Albania | Albania | via LinkedIn Albania |
| Data Analyst | AUTO1 Group | Tirana, Albania | Albania | via LinkedIn Albania |
| Data Analyst | Integrated Tech Solutions ITS | Tirana, Albania | Albania | via LinkedIn Albania |
| Data Analytics Specialist With SQL & Tableau | AUTO1 Group | Tirana, Albania | Albania | via SmartRecruiters Job Search |
| GIS Data Analyst | INOVA \| Software Development Company | Tirana, Albania | Albania | via LinkedIn Albania |
| Analyst Dataminer-(H/F) Permanent contract Centre- Algeria | Societe Generale SA | Algeria | Algeria | via Emplois Trabajo.org |
| IT/Data Analyst Intern | Smollan | Algeria | Algeria | via LinkedIn |
| Data Analyste | Société privée | Algeria | Algeria | via BeBee |
| ADV Central | SARL SIFAR DISTRIBUTION | Algeria | Algeria | via Trabajo.org |

---

## Exercise 7: Platform Performance Analysis

**Difficulty:** Hard
**Topics:** LEFT JOIN, GROUP BY, HAVING, COUNT
**Educational Focus:** Understanding primary/foreign key relationships through JOINs

### Problem Statement

Compare platform performance by showing platform name, total jobs posted, and average jobs per platform. Use PRIMARY KEY and FOREIGN KEY concepts through JOINs.

### SQL Solution

```sql
SELECT jpl.platform_name, jpl.jobs_posted, COUNT(jp.job_id) AS actual_jobs
FROM job_platforms AS jpl
LEFT JOIN job_postings AS jp ON jpl.platform_name = jp.job_via
GROUP BY jpl.platform_name, jpl.jobs_posted
HAVING COUNT(jp.job_id) > 100
ORDER BY actual_jobs DESC
LIMIT 15;
```

### Results

✅ **Query executed successfully**
- **Execution time:** 0.011s
- **Rows returned:** 20
- **Columns:** platform_name, jobs_posted, actual_jobs

#### Top 20 Results

| platform_name | jobs_posted | actual_jobs |
| --- | --- | --- |
| via LinkedIn | 186679 | 139839 |
| via BeBee | 103507 | 77541 |
| via Trabajo.org | 61562 | 46264 |
| via Indeed | 42756 | 32035 |
| via Recruit.net | 23646 | 17835 |
| via ZipRecruiter | 15533 | 11629 |
| via Jobs Trabajo.org | 10605 | 7920 |
| via Trabajo.org - Vacantes De Empleo, Trabajo | 8919 | 6665 |
| via BeBee India | 8642 | 6483 |
| via BeBee Singapore | 7985 | 5873 |
| via SimplyHired | 6632 | 4941 |
| via Jobrapido.com | 6202 | 4709 |
| via Sercanto | 5691 | 4268 |
| via The Muse | 5578 | 4167 |
| via BeBee Portugal | 5493 | 4115 |
| via Ai-Jobs.net | 5373 | 4059 |
| via Adzuna | 5238 | 3856 |
| via Emplois Trabajo.org | 5099 | 3816 |
| via Dice | 4493 | 3400 |
| via BeBee Belgique | 4421 | 3324 |

---

## Exercise 8: Remote Work by Company

**Difficulty:** Hard
**Topics:** LEFT JOIN, COUNT, CASE WHEN, GROUP BY, HAVING
**Educational Focus:** LEFT JOIN with conditional aggregation

### Problem Statement

Analyze remote work opportunities by company. Show company name, total jobs, and count of remote jobs. Include companies even if they don't offer remote work.

### SQL Solution

```sql
SELECT c.company_name,
       COUNT(jp.job_id) AS total_jobs,
       COUNT(CASE WHEN jp.job_work_from_home = 'True' THEN 1 END) AS remote_jobs
FROM companies AS c
LEFT JOIN job_postings AS jp ON c.company_name = jp.company_name
GROUP BY c.company_name
HAVING COUNT(jp.job_id) > 5
ORDER BY remote_jobs DESC
LIMIT 10;
```

### Results

✅ **Query executed successfully**
- **Execution time:** 0.024s
- **Rows returned:** 20
- **Columns:** company_name, total_jobs, remote_jobs

#### Top 20 Results

| company_name | total_jobs | remote_jobs |
| --- | --- | --- |
| Listopro | 1511 | 1196 |
| Dice | 2139 | 1093 |
| Upwork | 1035 | 1007 |
| Get It Recruit - Information Technology | 706 | 675 |
| Harnham | 1902 | 310 |
| EPAM Systems | 831 | 308 |
| EPAM Anywhere | 254 | 229 |
| TELUS International AI Data Solutions | 202 | 185 |
| Turing | 601 | 163 |
| Robert Half | 1374 | 156 |
| Peroptyx | 269 | 146 |
| Luxoft | 390 | 134 |
| Jobot | 843 | 115 |
| RemoteWorker UK | 208 | 115 |
| Motion Recruitment | 764 | 102 |
| Braintrust | 158 | 102 |
| Patterned Learning AI | 162 | 94 |
| Talentify.io | 89 | 88 |
| UnitedHealth Group | 1350 | 87 |
| Verizon | 344 | 85 |

---
