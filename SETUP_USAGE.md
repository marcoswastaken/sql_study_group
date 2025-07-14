# SQL Study Group - Quick Setup Guide

## For New Users

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

### What Happens
1. **Auto-detects dataset**: Reads week exercise file → determines dataset (data_jobs, movies, etc.)
2. **Installs dependencies**: Runs `pip install -r requirements.txt`
3. **Creates database**: Downloads data from HuggingFace + creates tables
4. **Starts web app**: Launches Flask interface at `http://localhost:5000`

### Manual Control (if needed)
```bash
# Just start the app for specific week (if database exists)
python app.py 4              # Week 4
python app.py 5              # Week 5
SQL_WEEK=5 python app.py     # Week 5 via environment variable

# Check what weeks are available
python -c "from setup import list_available_weeks; print(list_available_weeks())"

# Get help
python setup.py --help
python app.py --help
```

### Dataset Auto-Detection
- Week 4 → `data_jobs` dataset (785K job postings)
- Week 5 → `movies` dataset (if created)
- Week X → Any dataset specified in exercise metadata

### Troubleshooting
- **Port 5000 in use**: The app will show an error - stop other services or use different port
- **Dependencies fail**: Try `pip install -r requirements.txt` manually
- **Database errors**: Check if table creation queries exist for your dataset
- **No exercises found**: Make sure `exercises/week_X/` directory exists

### For Developers
- Setup script: `setup.py` (handles everything)
- App only: `app.py` (requires existing database)
- Original setup: `scripts/utilities/setup_sql_environment.py` (data_jobs only)
