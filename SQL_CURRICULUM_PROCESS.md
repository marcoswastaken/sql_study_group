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

### Step 4: Dataset Exploration + Database Creation

**Script:** `scripts/core/explore_dataset.py`

**Command:**

```bash
python scripts/core/explore_dataset.py --dataset lukebarousse/data_jobs --create-database
```

**Process:**

1. Load dataset from HuggingFace 
2. Generate comprehensive analysis (metadata, column types, data quality)
3. Identify potential relationships and normalization opportunities
4. Output detailed dataset summary to `/scripts/data_schema_generation/` directory
5. Create normalized database as `datasets/data_jobs.db` (using `--create-database` flag)
   - Single download for both analysis and database creation
   - Required for Step 6 validation and Step 7 table creation

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
Agent receives detailed curriculum generation prompt and creates educational tables:

**Process:**

1. Agent receives prompt specifying week topics and dataset to use
2. Agent reviews `syllabus_schema.json` for week topics (e.g., INNER JOIN, LEFT JOIN, primary/foreign keys)
3. Agent reviews `data_schema_[dataset].json` and `initial_exploration_[dataset].json` for dataset structure
4. Agent creates `table_creation_queries_[dataset].json` with several table creation queries, to create tables designed for progressive complexity
5. Agent validates the generated JSON object using the `validate_table_creation_queries.py` script
6. Agent iterates on table creation queries until all quality tests pass in the validation script
7. Agent discusses suitability, table design choices, and educational value with instructor

**Key Requirements:**

- Design meaningful tables for business scenarios (not "meaningless" data)
- Create tables that will allow for exercises with progressive complexity, from simple lookups to complex relationships
- Include intentional NULLs for LEFT JOIN practice, for example
- Ensure compatibility with existing sql_helper framework

### Step 6: Generate Child Tables (If Needed)
Agent create a new script to generate child tables if needed, `generate_child_tables_[dataset].py`, e.g. `generate_child_tables_[dataset].py`. 

**Process:**
1. Identify normalization opportunities (companies, locations, skills, etc.)
2. Extract unique values into dimension tables
3. Create foreign key relationships
4. Generate SQL creation scripts

### Step 7: Generate Data Schema Documentation
**Two-Phase Approach:**

**Phase 1:** `create_tables_from_queries.py --dataset [dataset]`
- Executes table creation queries from `table_creation_queries_[dataset].json`
- Creates educational tables in the database deterministically
- Reports creation status and row counts

**Phase 2:** `generate_data_schema_generic.py --dataset [dataset]`
- Introspects database structure and generates comprehensive schema
- Combines deterministic generation with strategic blanks for agent enhancement
- Outputs structured prompt for semantic field completion

**Process:**
1. Run Phase 1 to create tables from JSON queries
2. Run Phase 2 to generate schema template with enhancement prompt
3. Agent enhances semantic fields (descriptions, educational context, relationships)
4. Run `validate_data_schema.py --dataset [dataset]` to verify completion
5. Fix any empty fields or validation issues identified
6. Results in complete `data_schema_[dataset].json` ready for curriculum use

**Key Benefits:**
- Fully generic - works with any dataset following naming conventions
- Separates deterministic generation from semantic enhancement
- Maintains educational focus through structured agent prompts

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
    │   ├── initial_exploration_data_jobs.json # Dataset exploration output
    │   └── table_creation_queries_jobs.json # SQL creation queries
    ├── core/
    │   ├── sql_helper.py                # SQL execution framework
    │   └── explore_dataset.py           # Step 4 (built)
    ├── tests/
    │   ├── test_core_sql_helper.py      # SQL helper tests
    │   └── test_core_explore_dataset.py # Dataset exploration tests
    ├── utilities/
    │   ├── setup_sql_environment.py     # Database setup
    │   └── verify_environment.py        # Environment verification
    ├── generate_child_tables.py         # Step 6 (to be built)
    ├── generate_exercises.py            # Step 8 (to be built)
    ├── test_solutions.py                # Step 9 (to be built)
    └── generate_practice_worksheet.py   # Step 11 (to be built)
```

## Scripts We Already Have
- `scripts/core/sql_helper.py` - SQL execution framework
- `scripts/core/explore_dataset.py` - Dataset exploration and assessment (Step 4)
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
- `scripts/generate_child_tables.py` - Child table generation
- `scripts/generate_exercises.py` - Exercise generation
- `scripts/test_solutions.py` - Solution testing
- `scripts/generate_practice_worksheet.py` - Worksheet generation

## Next Steps
1. ✅ Created structured syllabus schema with URL support and intro/note fields
2. ✅ Built syllabus generation script that converts schema to markdown
3. ✅ Built `explore_dataset.py` for dataset assessment
4. Test MVP process with Week 4 data_jobs dataset
5. Refine scripts based on results
6. Apply to additional weeks

This MVP focuses on the core workflow we need to generate quality practice materials efficiently. 