# SQL Study Group - Quick Setup Guide

## For New Users

### One-Command Setup
```bash
# Clone the repository
git clone <repo-url>
cd sql_study_group

# Setup and start Week 4 (default) - recreates tables for fresh start
python setup.py

# Or setup and start any specific week - recreates tables
python setup.py 5

# Preserve existing tables (don't recreate)
python setup.py --keep-tables
python setup.py 5 --keep-tables
```

### What Happens
1. **Auto-detects dataset**: Reads week exercise file → determines dataset (data_jobs, movies, etc.)
2. **Installs dependencies**: Runs `pip install -r requirements.txt`
3. **Creates database**: Downloads data from HuggingFace + creates tables
4. **Starts web app**: Launches Flask interface at `http://localhost:5001`

### Manual Control (if needed)
```bash
# Create database for specific week (required for first-time setup)
python scripts/core/explore_dataset.py --dataset lukebarousse/data_jobs --create-database     # Week 4
python scripts/core/explore_dataset.py --dataset Pablinho/movies-dataset --create-database  # Week 5

# Create database tables
python scripts/data_schema_generation/create_tables_from_queries.py data_jobs                # Week 4
python scripts/data_schema_generation/create_tables_from_queries.py data_movies_dataset     # Week 5

# Start the app for specific week (requires database to exist)
python app.py 4              # Week 4
python app.py 5              # Week 5
SQL_WEEK=5 python app.py     # Week 5 via environment variable

# Check what weeks are available
python -c "from setup import list_available_weeks; print(list_available_weeks())"

# Get help
python setup.py --help
python app.py --help
```

**Note:** Use `python setup.py [week]` for automatic setup instead of manual steps.

### Dataset Auto-Detection
- Week 4 → `data_jobs` dataset (785K job postings)
- Week 5 → `movies` dataset (if created)
- Week X → Any dataset specified in exercise metadata

### Troubleshooting
- **Port 5001 in use**: The app will show an error - stop other services or use different port
- **Dependencies fail**: Try `pip install -r requirements.txt` manually
- **Database errors**: Check if table creation queries exist for your dataset
- **Tables already exist**: By default, setup recreates tables for fresh start. Use `--keep-tables` to preserve existing data
- **No exercises found**: Make sure `exercises/week_X/` directory exists

### For Developers
- Setup script: `setup.py` (handles everything)
- App only: `app.py` (requires existing database)
- Original setup: `scripts/utilities/setup_sql_environment.py` (data_jobs only)
