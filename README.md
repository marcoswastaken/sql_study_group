# SQL Study Group Curriculum

A systematic curriculum for learning SQL through real-world datasets and hands-on practice.

## System Requirements

Before running the setup script, ensure you have:

- **Python 3.8+** - The setup script requires Python with `venv` module support
- **Git** - For cloning the repository
- **Internet connection** - To download datasets from HuggingFace

### Python Installation Check
```bash
python --version    # Should show Python 3.8 or higher
python -m venv --help    # Should show venv module help (not error)
```

**Note:** The setup script automatically handles:
- ✅ Virtual environment creation
- ✅ Dependency installation
- ✅ Database setup
- ✅ App startup

You don't need to install any packages manually - the script handles everything!

## Quick Start

### Command-Line Setup

First, clone the repository. Navigate to the directory where you want to save the repository and run these commands:

```bash
# Clone the repository
git clone https://github.com/marcoswastaken/sql_study_group.git
cd sql_study_group
```

Then, run the setup script:

```bash
# Setup and start Week 4 (default)
python setup.py
```

If you want to load the exercises from a different week, you can specify the week number in the setup script:

```bash
# Setup and start any specific week
python setup.py 5
```

### Manual Setup (if needed)

```bash
# Install dependencies
pip install -r requirements.txt

# Create database for specific week (required for first-time setup)
python scripts/core/explore_dataset.py --dataset lukebarousse/data_jobs --create-database     # Week 4
python scripts/core/explore_dataset.py --dataset Pablinho/movies-dataset --create-database  # Week 5

# Create database tables
python scripts/data_schema_generation/create_tables_from_queries.py data_jobs                # Week 4
python scripts/data_schema_generation/create_tables_from_queries.py data_movies_dataset     # Week 5

# Start the app for specific week
python app.py 4              # Week 4
python app.py 5              # Week 5
SQL_WEEK=5 python app.py     # Week 5 via environment variable
```

**Note:** For first-time setup, it's easier to use `python setup.py [week]` which handles everything automatically.

### What You Get

- **Complete Automation**: One command handles everything from setup to app startup
- **Interactive Web Interface**: Practice SQL queries in your browser at `http://localhost:5001`
- **Real Datasets**: 785K+ job postings and other real-world data
- **Progressive Exercises**: From basic SELECT to complex JOINs and window functions
- **Instant Feedback**: Execute queries and see results immediately
- **Isolated Environment**: Uses its own virtual environment, won't affect your system

## What You'll Learn

- **SQL Fundamentals** - SELECT, WHERE, GROUP BY, ORDER BY
- **JOIN Operations** - INNER, LEFT, RIGHT, complex multi-table joins
- **Data Analysis** - Aggregations, window functions, CTEs
- **Real-world Skills** - Working with messy data, performance optimization

## Curriculum Overview

| Week | Topic | Key Skills |
|------|-------|------------|
| 1-2 | Basic Queries | SELECT, WHERE, ORDER BY |
| 3 | Aggregation | GROUP BY, COUNT, SUM, AVG |
| 4 | JOIN Operations | INNER/LEFT JOIN, multi-table |
| 5-6 | Advanced Queries | Subqueries, CTEs, window functions |
| 7-8 | Real-world Analysis | Performance, complex business logic |

## How It Works

The setup script automatically:

1. **Detects the dataset** from your chosen week's exercise file
2. **Downloads data** from HuggingFace (data_jobs, movies, etc.)
3. **Creates database tables** optimized for learning
4. **Starts the web app** with exercises ready to practice

The app adapts to different weeks and datasets automatically - no manual configuration needed!

## For Instructors

See `SQL_CURRICULUM_PROCESS.md` for the complete development methodology and how to create new curriculum materials.

---

## Dataset Sources

We use real-world datasets for authentic learning experiences:

**Week 4 (JOINs):** [Luke Barousse's Data Jobs](https://huggingface.co/datasets/lukebarousse/data_jobs) - 785K real job postings from 2023

**Week 5 (Advanced JOINs/Subqueries):** [Pablinho's Movies Dataset](https://huggingface.co/datasets/Pablinho/movies-dataset) - 9.8K movies with ratings, languages, and metadata (CC0 1.0 license)

Ready to start? Run `python setup.py` and begin practicing! 🚀
