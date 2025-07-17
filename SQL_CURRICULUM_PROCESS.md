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
python scripts/core/explore_dataset.py --dataset lukebarousse/data_jobs
```

**Process:**

1. Load dataset from HuggingFace
2. Generate comprehensive analysis (metadata, column types, data quality)
3. Identify potential relationships and normalization opportunities
4. Auto-saves to `scripts/data_schema_generation/initial_exploration_[dataset].json` (script handles path)
5. Create normalized database as `datasets/data_[dataset].db` automatically using `--create-database` flag
   - Uses absolute project-relative paths for consistent placement
   - Converts dashes to underscores in dataset names (e.g., "movies-dataset" → "data_movies_dataset.db")
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

### Step 7: Generate Schema Documentation

**Script:** `scripts/data_schema_generation/generate_data_schema_generic.py --dataset [dataset]`

**Process:**
1. Introspect database structure from created tables
2. Generate comprehensive schema template with strategic blanks for agent enhancement
3. Agent enhances semantic fields (descriptions, educational context, relationships)
4. Validate completeness using `scripts/data_schema_generation/validate_data_schema.py`
5. Output complete `schemas/data_schema_[dataset].json`

### Step 8: Generate Initial Exercises

**Script:** `scripts/exercise_generation/generate_exercises.py` (or adapt existing week-specific scripts)

**Process:**
1. Agent reviews syllabus topics and dataset schema
2. Generates exercises covering each topic with progressive difficulty
3. Creates SQL solutions and validates syntax
4. Outputs `exercises/week_X/week_X_key.json` with complete exercise metadata (organized by week)

**Key Requirements:**
- Questions must demonstrate educational value of target concepts
- Solutions must be tested and include sample results
- Progressive difficulty from Easy → Medium → Hard

### Step 9: Test and Validate Exercises

**Script:** `scripts/exercise_generation/test_solutions.py --exercise-key [file] --dataset [dataset]`

**Process:**
1. **Validate exercise metadata structure and required fields**:
   - Verify required metadata fields (title, description, week, database, generated_date)
   - Check exercise structure (id, title, statement, difficulty, topics, solution)
   - Validate database and schema file existence
   - Ensure exercise IDs are numeric and difficulty values are valid
   - Confirm topics arrays are properly structured
2. Execute all SQL solutions against database
3. Capture execution time, row counts, and sample results
4. Update exercise key with test results and metadata
5. Verify 100% success rate before proceeding

**Validation Requirements:**
- All required metadata fields must be present and non-empty
- Exercise IDs must be numeric
- Difficulty must be one of: Easy, Medium, Hard
- Topics must be non-empty arrays
- Database file and schema file must exist for specified dataset

### Step 10: Review and Improve Exercises

**Manual Review Process:**
1. Instructor/agent reviews exercise educational value
2. Identifies exercises that could be done without target concepts (e.g., joins that don't add value)
3. Redesigns exercises to ensure concepts are essential for solving problems
4. Creates improved version (e.g., `week_X_key_v2.json`) if needed
5. Re-runs Step 9 to validate improvements

### Step 11: Generate Documentation and Reports

**Scripts:**
- `scripts/exercise_generation/generate_exercise_report.py` - Comprehensive report with results
- Manual documentation of improvements and rationale

**Outputs:**
- `reports/week_X/week_X_[dataset]_report.md` - Complete exercise report with sample results (organized by week)
- `exercises/week_X/week_X_analysis.md` - Analysis of improvements made (if applicable)
- Final validated exercise key ready for student use

### Step 12: Generate Student Practice Guide

**Script:** `scripts/exercise_generation/generate_student_practice_guide.py [week_number]`

**Purpose:** Create offline practice guides for students with data dictionaries and problem statements. Students can work on SQL queries without database access, then test solutions later using the web interface.

**Features:**
- Comprehensive data dictionary with table schemas and relationships
- Problem statements with spaces for SQL solutions
- Auto-detects dataset from exercise key metadata
- Generates markdown files in `practice/` directory
- Includes instructions for testing solutions with setup script

**Output:**
- `practice/week_X_offline_practice.md` - Complete practice guide with data dictionary and exercises

## Project Structure (Current)

```
sql_study_group/
├── setup.py                            # One-command setup script for any week
├── app.py                              # Flask web application for practice
├── syllabus.md                         # Generated syllabus from schema
├── datasets/
│   ├── data_jobs.db                    # Job market dataset (auto-generated)
│   └── data_movies_dataset.db          # Movies dataset (auto-generated)
├── schemas/
│   └── data_schema_data_jobs.json      # Schema documentation for data_jobs dataset
├── exercises/
│   └── week_4/
│       ├── week_4_key_v1.json          # Exercise key for Week 4 (version 1)
│       ├── week_4_key_v2.json          # Enhanced exercise key for Week 4 (version 2)
│       ├── week_4_key_v3.json          # Exercise key for Week 4 (version 3)
│       └── week_4_key_v4.json          # Latest exercise key for Week 4 (version 4)
├── practice/
│   ├── week_2_practice.md              # Student worksheets
│   ├── week_3_practice.md
│   └── week_4_practice.md
├── solutions/
│   ├── week_2_practice_solutions.md    # Solution worksheets
│   ├── week_3_practice_solutions.md
│   └── week_4_practice_solutions.md
├── reports/
│   └── week_4/
│       ├── week_4_key_report_data_jobs_v1.md   # Exercise report for Week 4 (v1)
│       └── week_4_key_report_data_jobs_v2.md   # Enhanced exercise report (v2)
├── templates/
│   └── index.html                      # Web interface template
└── scripts/
    ├── practice_app/
    │   ├── data_service.py             # Exercise and schema data loading
    │   └── sql_service.py              # SQL execution service
    ├── asset_generation/
    │   ├── syllabus_schema.json        # Structured syllabus schema
    │   └── generate_syllabus.py        # Step 2 (built)
    ├── exercise_generation/
    │   ├── generate_exercises.py       # Generic exercise generation framework
    │   ├── test_solutions.py           # Solution testing and validation
    │   └── generate_exercise_report.py # Report generation
    ├── data_schema_generation/
    │   ├── create_tables_from_queries.py          # Step 6 (built)
    │   ├── generate_data_schema_generic.py        # Step 7 (built)
    │   ├── validate_data_schema.py                # Schema validation (built)
    │   ├── validate_table_creation_queries.py     # Table query validation (built)
    │   ├── initial_exploration_data_jobs.json     # Dataset exploration output
    │   └── table_creation_queries_data_jobs.json  # SQL creation queries
    ├── core/
    │   ├── sql_helper.py               # SQL execution framework
    │   └── explore_dataset.py          # Step 4 (built)
    ├── tests/
    │   ├── test_core_sql_helper.py     # SQL helper tests
    │   └── test_core_explore_dataset.py # Dataset exploration tests
    └── utilities/
        ├── setup_sql_environment.py   # Legacy database setup (data_jobs only)
        └── verify_environment.py      # Environment verification
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

### Exercise Generation
- `scripts/exercise_generation/generate_exercises.py` - Generic exercise generation framework (Step 8)
- `scripts/exercise_generation/test_solutions.py` - Solution testing and validation (Step 9)
- `scripts/exercise_generation/generate_exercise_report.py` - Report generation (Step 11)
- `scripts/exercise_generation/generate_student_practice_guide.py` - Creates offline practice guides

### Test Infrastructure
- `scripts/tests/test_core_sql_helper.py` - SQL helper tests
- `scripts/tests/test_core_explore_dataset.py` - Dataset exploration tests

## Scripts We Need to Build
- `scripts/exercise_generation/generate_practice_worksheet.py` - Student worksheet generation (optional)

## Current Status
1. ✅ **Step 1**: Structured syllabus schema with URL support and intro/note fields
2. ✅ **Step 2**: Syllabus generation script (converts schema to markdown)
3. ✅ **Step 3**: Process defined for instructor input
4. ✅ **Step 4**: Dataset exploration and database creation
5. ✅ **Step 5**: Agent review and table creation queries with validation
6. ✅ **Step 6**: Execute table creation queries
7. ✅ **Step 7**: Schema documentation generation
8. ✅ **Step 8**: Exercise generation (generic framework implemented)
9. ✅ **Step 9**: Solution testing and validation
10. ✅ **Step 10**: Exercise review and improvement process
11. ✅ **Step 11**: Documentation and report generation
12. ✅ **Step 12**: Student practice guide generation

## Key Process Improvements Made
- **Comprehensive validation**: Multiple validation scripts ensure quality at each step
- **Improved determinism**: SETSEED ensures consistent results across runs
- **Educational focus**: Step 10 ensures exercises demonstrate true value of target concepts
- **Complete testing**: All SQL solutions are validated and include sample results
- **Automated reporting**: Detailed reports with execution metrics and sample data

This process provides a complete, replicable workflow for generating high-quality SQL curriculum materials.

## Quick Start: Running the App for Any Week

For students or instructors who want to quickly start practicing with any week's exercises:

### One-Command Setup
```bash
# Clone the repository
git clone <repo-url>
cd sql_study_group

# Setup and start Week 4 (default)
python setup.py

# Or setup and start any specific week
python setup.py 5
```

### Manual Setup (if needed)
```bash
# Install dependencies
pip install -r requirements.txt

# Start the app for specific week
python app.py 4              # Week 4
python app.py 5              # Week 5
SQL_WEEK=5 python app.py     # Week 5 via environment variable
```

### What the setup script does:
1. **Detects dataset**: Reads the week's exercise file to determine which dataset to use
2. **Downloads data**: Automatically downloads the dataset from HuggingFace
3. **Creates tables**: Uses the table creation queries to build the database
4. **Starts app**: Launches the Flask web interface at `http://localhost:5001`

The app automatically adapts to different weeks and datasets based on the exercise metadata.
