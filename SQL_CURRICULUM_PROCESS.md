# SQL Curriculum MVP Process

## Overview
Simple, repeatable process for generating SQL practice materials from syllabus + dataset + week number.

## MVP Steps

### Step 1: Instructor Provides Syllabus Schema
Instructor creates syllabus content in structured JSON format and saves as `syllabus_schema.json`.

**Required Schema Format:**
```json
{
  "metadata": {
    "title": "8-Week SQL Study Group Syllabus",
    "description": "Comprehensive week-by-week breakdown with specific LeetCode problems and learning objectives",
    "duration_weeks": 8,
    "target_audience": "SQL learners progressing from basic to intermediate level",
    "created": "2024",
    "last_updated": "2024-12-19"
  },
  "weeks": [
    {
      "number": 4,
      "title": "JOIN Operations",
      "intro": null,
      "core_concepts": [
        "Primary/foreign keys",
        "INNER JOIN",
        "LEFT JOIN (or LEFT OUTER JOIN)",
        "ON clause",
        "Table aliases in joins"
      ],
      "learning_objectives": [
        "Identify when JOIN is needed",
        "Write INNER JOIN and LEFT JOIN queries",
        "Understand how NULLs are handled in LEFT JOINs"
      ],
      "sqlzoo": [
        {
          "title": "7. The JOIN operation",
          "url": "https://sqlzoo.net/wiki/The_JOIN_operation"
        },
        {
          "title": "8. More JOIN operations",
          "url": "https://sqlzoo.net/wiki/More_JOIN_operations",
          "description": "Start this section"
        }
      ],
      "leetcode": [
        {
          "title": "175. Combine Two Tables",
          "url": null,
          "description": "Basic LEFT JOIN"
        },
        {
          "title": "197. Rising Temperature",
          "url": null,
          "description": "Requires a JOIN (often self-join conceptually or using date functions)"
        }
      ],
      "additional_resources": [
        {
          "title": "Mode Analytics SQL Tutorial: Joins",
          "url": "https://mode.com/sql-tutorial/sql-joins/"
        }
      ],
      "note": null
    }
  ],
  "study_tips": [
    "Practice Regularly: Dedicate at least 2-3 hours per week to hands-on practice",
    "Join Online Communities: Participate in SQL forums and Discord communities"
  ]
}
```

**Field Definitions:**
- `intro`: Optional introductory text for the week (use `null` if none)
- `note`: Optional note at end of week (use `null` if none)  
- `url`: Optional URL for resources (use `null` if none)
- `description`: Optional description for SQLZoo/LeetCode items

### Step 2: Generate Syllabus Markdown
**Script:** `generate_syllabus.py`

**Process:**
1. Reads `syllabus_schema.json`
2. Converts structured data to formatted markdown
3. Outputs `syllabus.md`

**Features:**
- Bulleted core concepts and learning objectives
- Clickable links for resources with URLs
- Sub-bullet descriptions for exercises
- Notes appear at end of applicable weeks

### Step 3: Instructor Provides Week Number and Dataset
Instructor specifies:
- Week number (e.g., 4)
- Dataset source (HuggingFace link, local file, or existing dataset)

### Step 4: Dataset Exploration
**Script:** `explore_dataset.py`

**Process:**
1. Load dataset into DuckDB
2. Generate basic stats (table count, row count, column types)
3. Identify potential relationships
4. Output dataset summary

**Dataset Summary Format:**
```json
{
  "dataset_name": "data_jobs",
  "total_records": 785741,
  "table_count": 1,
  "columns": [
    {"name": "company_name", "type": "VARCHAR", "sample_values": ["Google", "Apple"]},
    {"name": "job_title", "type": "VARCHAR", "sample_values": ["Data Scientist", "Analyst"]}
  ],
  "suitability_assessment": "Good for JOIN exercises - rich categorical data"
}
```

### Step 5: Agent Review & Discussion
Agent reviews dataset summary and discusses with instructor:
- Suitability for week topics
- Potential child table opportunities
- Any data quality concerns

### Step 6: Generate Child Tables (If Needed)
**Script:** `generate_child_tables.py`

**Process:**
1. Identify normalization opportunities (companies, locations, skills, etc.)
2. Extract unique values into dimension tables
3. Create foreign key relationships
4. Generate SQL creation scripts

### Step 7: Generate Data Schema Documentation
**Script:** `generate_data_schema.py` (already built as `generate_data_jobs_schema.py`)

**Process:**
1. Generate comprehensive schema with metadata, tables, relationships
2. Include creation queries showing how child tables were derived
3. Add sample data for each table
4. Document relationships between tables
5. Add educational schema notes

**Schema Format:**
```json
{
  "metadata": {
    "database_name": "data_jobs.db",
    "description": "Normalized schema for real-world data analytics job postings dataset",
    "total_tables": 6,
    "total_records": 987313,
    "source": "Luke Barousse Data Jobs Dataset from HuggingFace",
    "hf_source": "lukebarousse/data_jobs",
    "original_dataset_size": 785741,
    "normalization_approach": "Dimensional modeling with fact table and dimension tables"
  },
  "tables": [
    {
      "id": 1,
      "name": "companies",
      "description": "Contains information about companies that post job listings",
      "creation_query": "CREATE TABLE companies AS\nSELECT DISTINCT \n    ROW_NUMBER() OVER (ORDER BY company_name) as company_id,\n    company_name\nFROM raw_jobs_data \nWHERE company_name IS NOT NULL;",
      "row_count": 139983,
      "columns": [
        {
          "name": "company_id",
          "type": "INTEGER",
          "nullable": false,
          "primary_key": true,
          "description": "Unique identifier for each company",
          "foreign_key": ""
        },
        {
          "name": "company_name",
          "type": "VARCHAR",
          "nullable": true,
          "primary_key": false,
          "description": "Name of the company posting the job",
          "foreign_key": ""
        }
      ],
      "sample_data": [
        {
          "company_id": "1",
          "company_name": "Boehringer Ingelheim"
        }
      ]
    }
  ],
  "relationships": [
    {
      "type": "one-to-many",
      "from_table": "companies",
      "from_column": "company_id",
      "to_table": "jobs",
      "to_column": "company_id",
      "description": "One company can have many job postings"
    }
  ],
  "schema_notes": [
    "Database follows normalized design principles with dimensional modeling approach",
    "All dimension tables were extracted from the original dataset",
    "Schema is optimized for educational SQL exercises and real-world analysis"
  ]
}
```

### Step 8: Generate Exercises and Solutions
Agent reviews datasets and topics to generate practice exercises.

**Process:**
1. Load week topics from structured syllabus
2. Generate exercises that cover each topic using the dataset
3. Create SQL solutions for each exercise
4. Format as exercise key

**Exercise Key Format:**
```json
{
  "exercises": [
    {
      "id": "exercise_1",
      "statement": "Find all job postings for companies in California",
      "solution": "SELECT j.* FROM jobs j JOIN companies c ON j.company_id = c.company_id WHERE c.state = 'California'",
      "difficulty": NULL,
      "topics": ["INNER JOIN", "WHERE clause"]
    }
  ]
}
```

### Step 9: Test All Solutions
**Script:** `test_solutions.py`

**Process:**
1. Load exercise key
2. Execute each solution query using `sql_helper.py`
3. Capture results and performance metrics
4. Update key with sample results

### Step 10: Instructor Review & Iteration
1. Instructor reviews generated exercises
2. Provides feedback on difficulty, relevance, coverage
3. Agent adjusts exercises based on feedback (revise difficulty and topics)
4. Repeat Steps 8-9 until satisfied

### Step 11: Generate Practice Materials
**Script:** `generate_practice_worksheet.py`

**Generates:**
- `practice/week_X_practice.md` - Student worksheet with exercises only
- `solutions/week_X_solutions.md` - Instructor solutions with explanations

## Project Structure (MVP)

```
sql_study_group/
├── syllabus.md                          # Generated syllabus from schema
├── datasets/
│   └── data_jobs.db                     # jobs datasets
├── schemas/
│   └── data_schema_jobs.json            # Schema documentation for jobs dataset
├── exercises/
│   └── week_4_key.json                  # Exercise key for Week 4
├── practice/
│   └── week_4_practice.md               # Student worksheet for Week 4
├── solutions/
│   └── week_4_solutions.md              # Solution to the Week 4 worksheet
└── scripts/
    ├── asset_generation/
    │   ├── syllabus_schema.json         # Structured syllabus schema
    │   └── generate_syllabus.py         # Step 2 (already built)
    ├── exercise_generation/
    │   └── generate_week_4_key.py       # Exercise extraction (adapt for Step 8)
    ├── data_schema_generation/
    │   ├── generate_data_schema_jobs.py # Step 7 (already built)
    │   └── table_creation_queries_jobs.json # SQL creation queries
    ├── core/
    │   └── sql_helper.py                # SQL execution framework
    ├── tests/
    │   └── test_sql_helper_comprehensive.py # Comprehensive testing
    ├── utilities/
    │   ├── setup_sql_environment.py     # Database setup
    │   └── verify_environment.py        # Environment verification
    ├── explore_dataset.py               # Step 4 (to be built)
    ├── generate_child_tables.py         # Step 6 (to be built)
    ├── generate_exercises.py            # Step 8 (to be built)
    ├── test_solutions.py                # Step 9 (to be built)
    └── generate_practice_worksheet.py   # Step 11 (to be built)
```

## Scripts We Already Have
- `scripts/core/sql_helper.py` - SQL execution framework
- `scripts/asset_generation/generate_syllabus.py` - Converts structured JSON schema to formatted markdown (Step 2)
  - Handles URLs for SQLZoo, LeetCode, and additional resources
  - Supports intro and note fields for each week
  - Generates clean, readable markdown with proper formatting
- `scripts/data_schema_generation/generate_data_schema_jobs.py` - Comprehensive schema documentation (Step 7)
  - Tracks HuggingFace source dataset
  - Documents all child tables with creation queries
  - Includes relationships, sample data, and educational notes
- `scripts/exercise_generation/generate_week_4_key.py` - Exercise extraction (can adapt for Step 8)
- `scripts/asset_generation/syllabus_schema.json` - Complete structured syllabus with all 8 weeks
- `scripts/utilities/setup_sql_environment.py` - Database creation and setup
- `scripts/utilities/verify_environment.py` - Environment verification and testing

## Scripts We Need to Build
- `scripts/explore_dataset.py` - Dataset exploration and assessment
- `scripts/generate_child_tables.py` - Child table generation
- `scripts/generate_exercises.py` - Exercise generation
- `scripts/test_solutions.py` - Solution testing
- `scripts/generate_practice_worksheet.py` - Worksheet generation

## Next Steps
1. ✅ Created structured syllabus schema with URL support and intro/note fields
2. ✅ Built syllabus generation script that converts schema to markdown
3. Build `explore_dataset.py` for dataset assessment
4. Test MVP process with Week 4 data_jobs dataset
5. Refine scripts based on results
6. Apply to additional weeks

This MVP focuses on the core workflow we need to generate quality practice materials efficiently. 