# Exercise Generation Scripts

This directory contains scripts for generating SQL exercises and practice materials.

## Scripts

### `generate_student_practice_guide.py`

Creates markdown files with data dictionaries and problem statements for offline practice.

**Purpose:** Students can work on SQL queries without database access, then test their solutions later using the web interface.

**Usage:**
```bash
# Generate practice guide for Week 4 (default)
python generate_student_practice_guide.py

# Generate practice guide for Week 5
python generate_student_practice_guide.py 5

# Specify custom output path
python generate_student_practice_guide.py 4 -o custom_practice_guide.md
```

**Features:**
- Auto-detects dataset from exercise key metadata
- Comprehensive data dictionary with table schemas and relationships
- Problem statements with spaces for SQL solutions
- Instructions for testing solutions with setup script
- Outputs markdown files to `practice/` directory

**Output Example:**
```
practice/week_4_offline_practice.md
```

**What Students Get:**
- Complete data dictionary with table descriptions and column details
- All exercise problem statements
- Formatted spaces to write SQL queries
- Instructions on how to test their solutions

**Typical Workflow:**
1. Instructor runs script to generate practice guide
2. Students work on exercises offline using the guide
3. Students test their solutions using `python setup.py [week]`
4. Students compare performance and optimize queries

### Other Scripts

- `generate_exercises.py` - Creates exercise JSON files with problem statements and solutions
- `test_solutions.py` - Validates exercise solutions and tests query performance
- `generate_exercise_report.py` - Creates comprehensive reports with exercise analysis
- `generate_week_4_key.py` - Legacy script for Week 4 exercise generation
