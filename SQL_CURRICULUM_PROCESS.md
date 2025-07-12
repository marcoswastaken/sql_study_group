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

**Script:** `scripts/asset_generation/generate_syllabus.py`

**Process:**

1. Reads `scripts/asset_generation/syllabus_schema.json`
2. Converts structured data to formatted markdown
3. Outputs `syllabus.md` to root directory

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
python scripts/core/explore_dataset.py --dataset lukebarousse/data_jobs --output initial_exploration_data_jobs.json
```

**Process:**

1. Load dataset from HuggingFace 
2. Generate comprehensive analysis (metadata, column types, data quality)
3. Identify potential relationships and normalization opportunities
4. Output detailed dataset summary to `scripts/data_schema_generation/initial_exploration_[dataset].json`
5. Create normalized database as `datasets/[dataset].db` automatically
   - Single download for both analysis and database creation
   - Required for Step 5 validation and Step 7 table creation

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

### Step 5: Agent Review & Table Creation Queries

Agent receives detailed curriculum generation prompt and creates educational tables:

**Process:**

1. Agent receives prompt specifying week topics and dataset to use
2. Agent reviews `scripts/asset_generation/syllabus_schema.json` for week topics (e.g., INNER JOIN, LEFT JOIN, primary/foreign keys)
3. Agent reviews `scripts/data_schema_generation/initial_exploration_[dataset].json` for dataset structure
4. Agent creates `scripts/data_schema_generation/table_creation_queries_[dataset].json` with several table creation queries designed for progressive complexity
5. Agent validates the generated JSON using `scripts/data_schema_generation/validate_table_creation_queries.py --dataset [dataset]`
6. Agent iterates on table creation queries until all quality tests pass (percentage usage, randomness, etc.)
7. Agent discusses suitability, table design choices, and educational value with instructor

**Key Requirements:**

- Design meaningful tables for business scenarios (not "meaningless" data)
- Create tables with progressive complexity, from simple lookups to complex relationships
- Use percentage-based sampling (75%+ of available data) with deterministic seeding
- Include intentional data scenarios for LEFT JOIN practice
- Ensure compatibility with existing sql_helper framework

**Critical Validation Requirements:**
- Tables must use 75%+ of available data (not arbitrary small numbers)
- Random sampling must be deterministic (using SETSEED)
- Validation script must pass all tests before proceeding

### Step 6: Execute Table Creation Queries

**Script:** `scripts/data_schema_generation/create_tables_from_queries.py --dataset [dataset]`

**Process:**
1. Read validated table creation queries from `table_creation_queries_[dataset].json`
2. Execute each query to create educational tables in the database
3. Report creation status and row counts for each table
4. Clean up any test tables to keep database tidy
5. Verify all tables were created successfully

**Key Features:**
- Deterministic execution using seeded random sampling
- Comprehensive error handling and reporting
- Database cleanup to maintain clean state
- Validation of table creation success

**Requirements:**
- Table creation queries must pass validation from Step 5
- Database must be accessible and writable
- All queries must execute successfully before proceeding

### Step 7: Generate Data Schema Documentation

**Script:** `scripts/data_schema_generation/generate_data_schema_generic.py --dataset [dataset]`

**Process:**
1. Introspect database structure from tables created in Step 6
2. Generate comprehensive schema template with strategic blanks for agent enhancement
3. Output structured prompt for semantic field completion
4. Create `schemas/data_schema_[dataset].json` template

**Agent Enhancement:**
- Agent enhances semantic fields (descriptions, educational context, relationships)
- Agent completes all empty description fields and educational purposes
- Agent fixes any malformed relationships or inconsistencies

**Final Validation:**
- Run `scripts/data_schema_generation/validate_data_schema.py --dataset [dataset]` to verify completion
- All fields must be populated before proceeding to Step 8
- Results in complete `schemas/data_schema_[dataset].json` ready for curriculum use

**Key Benefits:**
- Fully generic - works with any dataset following naming conventions
- Separates deterministic generation from semantic enhancement
- Maintains educational focus through structured agent prompts
- Provides comprehensive validation to ensure completeness

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

## Project Structure (Current)

```
sql_study_group/
├── syllabus.md                          # Generated syllabus from schema
├── datasets/
│   └── data_jobs.db                     # Job market dataset
├── schemas/
│   └── data_schema_data_jobs.json       # Schema documentation for data_jobs dataset
├── exercises/
│   └── week_4_key.json                  # Exercise key for Week 4
├── practice/
│   ├── week_2_practice.md               # Student worksheets
│   ├── week_3_practice.md
│   └── week_4_practice.md
├── solutions/
│   ├── week_2_practice_solutions.md     # Solution worksheets
│   ├── week_3_practice_solutions.md
│   └── week_4_practice_solutions.md
└── scripts/
    ├── asset_generation/
    │   ├── syllabus_schema.json         # Structured syllabus schema
    │   └── generate_syllabus.py         # Step 2 (built)
    ├── exercise_generation/
    │   └── generate_week_4_key.py       # Exercise extraction (adapt for Step 8)
    ├── data_schema_generation/
    │   ├── create_tables_from_queries.py          # Step 7 Phase 1 (built)
    │   ├── generate_data_schema_generic.py        # Step 7 Phase 2 (built)
    │   ├── validate_data_schema.py                # Schema validation (built)
    │   ├── validate_table_creation_queries.py     # Table query validation (built)
    │   ├── initial_exploration_data_jobs.json     # Dataset exploration output
    │   └── table_creation_queries_data_jobs.json  # SQL creation queries
    ├── core/
    │   ├── sql_helper.py                # SQL execution framework
    │   └── explore_dataset.py           # Step 4 (built)
    ├── tests/
    │   ├── test_core_sql_helper.py      # SQL helper tests
    │   └── test_core_explore_dataset.py # Dataset exploration tests
    └── utilities/
        ├── setup_sql_environment.py    # Database setup
        └── verify_environment.py       # Environment verification
```

## Scripts We Already Have (Updated)

### Core Infrastructure
- `scripts/core/sql_helper.py` - SQL execution framework
- `scripts/core/explore_dataset.py` - Dataset exploration and assessment (Step 4)
- `scripts/utilities/setup_sql_environment.py` - Database creation and setup
- `scripts/utilities/verify_environment.py` - Environment verification and testing

### Asset Generation
- `scripts/asset_generation/generate_syllabus.py` - Converts structured JSON schema to formatted markdown (Step 2)
  - Handles URLs for SQLZoo, LeetCode, and additional resources
  - Supports intro and note fields for each week
  - Generates clean, readable markdown with proper formatting
- `scripts/asset_generation/syllabus_schema.json` - Complete structured syllabus with all 8 weeks

### Data Schema Generation (Complete)
- `scripts/data_schema_generation/create_tables_from_queries.py` - Step 6 (built)
  - Executes table creation queries from JSON
  - Creates educational tables deterministically
  - Reports creation status and row counts
  - Cleans up test tables to keep database tidy
- `scripts/data_schema_generation/generate_data_schema_generic.py` - Step 7 (built)
  - Introspects database structure and generates schema template
  - Combines deterministic generation with strategic blanks for agent enhancement
  - Outputs structured prompt for semantic field completion
- `scripts/data_schema_generation/validate_data_schema.py` - Schema validation (built)
  - Validates completeness of schema documentation
  - Checks for empty fields and missing educational context
  - Ensures all requirements are met
- `scripts/data_schema_generation/validate_table_creation_queries.py` - Table query validation (built)
  - Validates percentage usage requirements (75%+ of data)
  - Checks for deterministic random sampling (SETSEED)
  - Ensures educational table design quality

### Exercise Generation (Partial)
- `scripts/exercise_generation/generate_week_4_key.py` - Exercise extraction (can adapt for Step 8)

### Test Infrastructure
- `scripts/tests/test_core_sql_helper.py` - SQL helper tests
- `scripts/tests/test_core_explore_dataset.py` - Dataset exploration tests

## Scripts We Need to Build
- `scripts/exercise_generation/generate_exercises.py` - Exercise generation (Step 8)
- `scripts/exercise_generation/test_solutions.py` - Solution testing (Step 9)
- `scripts/exercise_generation/generate_practice_worksheet.py` - Worksheet generation (Step 11)

## Current Status (Updated)
1. ✅ **Step 1**: Structured syllabus schema with URL support and intro/note fields
2. ✅ **Step 2**: Syllabus generation script (converts schema to markdown)
3. ✅ **Step 3**: Process defined for instructor input
4. ✅ **Step 4**: Dataset exploration and database creation
5. ✅ **Step 5**: Agent review and table creation queries with validation
6. ✅ **Step 6**: Execute table creation queries (built)
7. ✅ **Step 7**: Schema documentation generation (built)
8. 🔄 **Step 8**: Exercise generation (ready to build)
9. 🔄 **Step 9**: Solution testing (ready to build)
10. 🔄 **Step 10**: Instructor review process (ready to implement)
11. 🔄 **Step 11**: Practice material generation (ready to build)

## Key Process Improvements Made
- **Restored Step 6**: Execute table creation queries to actually create tables in database
- **Enhanced Step 5**: Added percentage-based sampling validation with 75% minimum requirement
- **Clarified Step 7**: Focused on schema documentation generation from created tables
- **Fixed file paths**: All scripts now have correct relative paths
- **Updated validation**: Multiple validation scripts ensure quality at each step
- **Improved determinism**: SETSEED ensures consistent results across runs

This process now reflects the actual implemented workflow and provides a solid foundation for generating quality SQL curriculum materials. 