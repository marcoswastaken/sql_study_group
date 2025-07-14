# SQL Study Group Curriculum

A systematic curriculum for learning SQL through real-world datasets and hands-on practice.

## Quick Start

```bash
# Setup environment
pip install -r requirements.txt

# Create database and practice materials
python scripts/utilities/setup_sql_environment.py
python scripts/utilities/verify_environment.py

# Generate curriculum materials
python scripts/asset_generation/generate_syllabus.py
```

## What You'll Learn

- **SQL Fundamentals** - SELECT, WHERE, GROUP BY, ORDER BY
- **JOIN Operations** - INNER, LEFT, RIGHT, complex multi-table joins
- **Data Analysis** - Aggregations, window functions, CTEs
- **Real-world Skills** - Working with messy data, performance optimization

## Practice Dataset

**785,741 real data job postings** from 2023, normalized into 6 related tables:
- `companies` - Company information
- `jobs` - Job postings with foreign keys
- `locations` - Geographic data
- `platforms` - Job posting platforms
- `skills` - Technical skills
- `job_skills` - Many-to-many job-skill relationships

## Project Structure

```
sql_study_group/
├── syllabus.md                  # 8-week curriculum outline
├── datasets/
│   └── data_jobs.db            # Practice database
├── schemas/
│   └── data_schema_jobs.json   # Database documentation
├── exercises/
│   └── week_4_key.json         # Exercise solutions with tests
├── practice/                   # Student worksheets
├── solutions/                  # Instructor solutions
└── scripts/                    # Curriculum generation tools
    ├── asset_generation/       # Syllabus and schema tools
    ├── exercise_generation/    # Exercise creation
    ├── core/                   # SQL helper utilities
    ├── tests/                  # Testing framework
    └── utilities/              # Setup and verification
```

## Getting Started

### Prerequisites
- Python 3.12+
- Git

### Installation

1. **Clone and setup:**
   ```bash
   git clone <repo-url>
   cd sql_study_group
   pip install -r requirements.txt
   ```

2. **Initialize database:**
   ```bash
   python scripts/utilities/setup_sql_environment.py
   ```

3. **Verify installation:**
   ```bash
   python scripts/utilities/verify_environment.py
   ```

### Practice Options

**Option 1: Jupyter Notebooks (Interactive)**
```bash
jupyter notebook
# Open week_4_sql_practice.ipynb
```

**Option 2: Direct SQL Practice**
```python
from scripts.core.sql_helper import SQLHelper
helper = SQLHelper()
helper.execute_query("SELECT * FROM companies LIMIT 5")
```

**Option 3: Markdown Worksheets**
- Work through files in `practice/` directory
- Check answers in `solutions/` directory

## Curriculum Overview

| Week | Topic | Key Skills |
|------|-------|------------|
| 1-2 | Basic Queries | SELECT, WHERE, ORDER BY |
| 3 | Aggregation | GROUP BY, COUNT, SUM, AVG |
| 4 | JOIN Operations | INNER/LEFT JOIN, multi-table |
| 5-6 | Advanced Queries | Subqueries, CTEs, window functions |
| 7-8 | Real-world Analysis | Performance, complex business logic |

## For Instructors

### Generate New Materials
```bash
# Update syllabus
python scripts/asset_generation/generate_syllabus.py

# Create schema documentation
python scripts/data_schema_generation/generate_data_schema_jobs.py

# Generate exercise keys
python scripts/exercise_generation/generate_week_4_key.py
```

### Test Environment
```bash
python scripts/tests/test_sql_helper_comprehensive.py
```

## Troubleshooting

**Database not found?**
- Run: `python scripts/utilities/setup_sql_environment.py`

**Import errors?**
- Check: `python scripts/utilities/verify_environment.py`

**Need help?**
- Check solution files in `solutions/` directory
- Review schema documentation in `schemas/`

## Contributing

This curriculum is designed to be systematic and reproducible. See `SQL_CURRICULUM_PROCESS.md` for the complete development methodology.

---

**Dataset:** [Luke Barousse's Data Jobs](https://huggingface.co/datasets/lukebarousse/data_jobs) - 785K real job postings from 2023

Ready to start? Check out `syllabus.md` for the full 8-week curriculum! 🚀
