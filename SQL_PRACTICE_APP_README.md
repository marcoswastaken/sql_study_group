# SQL Practice App

A simple web interface for practicing SQL queries using the Week 4 JOIN operations exercises with the data jobs dataset.

## Features

- **Data Dictionary**: Interactive table schema reference showing all available tables and columns
- **Exercise Selection**: Choose from 6 JOIN-focused exercises with varying difficulty levels
- **Query Editor**: Write and test SQL queries in a syntax-highlighted editor
- **Query Execution**: Run queries against the SQLite database and see results in real-time
- **Query Validation**: Validate SQL syntax without executing queries
- **Solution Viewing**: View official solutions and expected results for each exercise

## Quick Start

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Application**
   ```bash
   python app.py
   ```

3. **Access the App**
   - Open your browser and go to `http://localhost:5000`
   - The app will automatically load with the data dictionary and available exercises

## How to Use

### 1. Review the Data Dictionary
- The left sidebar shows all available tables (`companies`, `locations`, `job_platforms`, `job_postings`, `salary_ranges`)
- Each table shows column names, data types, and key relationships
- Use this reference while writing your queries

### 2. Select an Exercise
- Click on any exercise in the left sidebar to view its problem statement
- Each exercise shows:
  - **Difficulty level** (Easy/Medium/Hard)
  - **Topics covered** (INNER JOIN, LEFT JOIN, etc.)
  - **Educational focus** explaining the learning objectives

### 3. Write Your Query
- Enter your SQL query in the text area
- Use the table names and column names from the data dictionary
- The editor supports multi-line queries

### 4. Test Your Query
- **Execute Query**: Run your query and see the results
- **Validate Query**: Check syntax without executing
- **Show Solution**: View the official solution and expected results

### 5. View Results
- Query results are displayed in a formatted table
- Execution time and row count are shown
- Error messages provide feedback for debugging

## Example Workflow

1. Select "Exercise 1: Platform Competition Analysis"
2. Review the problem statement asking for platform activity by country
3. Check the data dictionary for `locations` and `job_postings` tables
4. Write a query using INNER JOIN to combine the tables
5. Execute the query and review results
6. Compare with the official solution if needed

## Technical Details

- **Backend**: Flask (Python)
- **Database**: SQLite with ~590K job postings
- **Frontend**: HTML/CSS/JavaScript
- **Dataset**: lukebarousse/data_jobs from HuggingFace

## API Endpoints

- `GET /` - Main application interface
- `GET /api/exercises` - List all exercises
- `GET /api/exercises/{id}` - Get exercise details
- `POST /api/execute` - Execute SQL query
- `POST /api/validate` - Validate SQL syntax
- `GET /api/tables` - Get table schema information

## Educational Focus

This app is designed for Week 4 of the SQL curriculum, focusing on:
- INNER JOIN operations
- LEFT JOIN operations  
- Table aliases and relationships
- Cross-table analysis
- Business insights from joined data
- Window functions (advanced exercises)

## Troubleshooting

- **Database not found**: Ensure `datasets/data_jobs.db` exists in the project directory
- **Port already in use**: The app runs on port 5000 by default
- **Query timeouts**: Queries are limited to 1000 rows for performance
- **Syntax errors**: Use the "Validate Query" button to check syntax before execution

## Development

To extend or modify the app:

1. **Add new exercises**: Update `exercises/week_4/week_4_key_v4.json`
2. **Modify table schema**: Update `schemas/data_schema_data_jobs.json`
3. **Change styling**: Edit the `<style>` section in `templates/index.html`
4. **Add new API endpoints**: Extend `app.py`

## Pre-commit Hooks

The project includes ruff linting and formatting:

```bash
# Install pre-commit hooks
pre-commit install

# Run hooks manually
pre-commit run --all-files
```

## Future Enhancements

- Solution comparison and scoring
- Query history and bookmarking
- Export results to CSV
- Multiple database support
- User authentication and progress tracking 