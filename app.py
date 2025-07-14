"""
SQL Practice App - Main Flask application

Usage:
    python app.py [week_number]

Examples:
    python app.py           # Uses Week 4 (default)
    python app.py 5         # Uses Week 5
    SQL_WEEK=5 python app.py  # Uses Week 5 via environment variable
"""

import os
import sys

from flask import Flask, jsonify, render_template, request
from flask_cors import CORS

from scripts.practice_app.data_service import DataService
from scripts.practice_app.sql_service import SQLService

app = Flask(__name__)
CORS(app)


# Configuration: Week selection
# Priority: Command line arg > Environment variable > Default (4)
def get_week_config():
    """Get week configuration from command line args or environment variables."""
    # Check for help request
    if len(sys.argv) > 1 and sys.argv[1] in ["-h", "--help", "help"]:
        print(__doc__)
        print("Environment Variables:")
        print("  SQL_WEEK=N    Set week number (default: 4)")
        print("\nThe app will automatically detect the dataset from exercise metadata.")
        sys.exit(0)

    # Check command line arguments
    if len(sys.argv) > 1:
        try:
            return int(sys.argv[1])
        except ValueError:
            print(
                f"Warning: Invalid week argument '{sys.argv[1]}', using default week 4"
            )

    # Check environment variable
    week = os.environ.get("SQL_WEEK", "4")
    try:
        return int(week)
    except ValueError:
        print(
            f"Warning: Invalid SQL_WEEK environment variable '{week}', using default week 4"
        )
        return 4


# Initialize services
week = get_week_config()
print(f"🎯 Loading exercises for Week {week}")

data_service = DataService(week=week)
try:
    sql_service = SQLService(data_service.get_database_path())
    print(f"📊 Connected to database: {data_service.get_current_dataset()}")
except Exception as e:
    print(f"Error initializing SQL service: {e}")
    sql_service = None


@app.route("/")
def index():
    """Main page with the SQL practice interface."""
    try:
        # Get table information for data dictionary
        tables = data_service.get_table_info()

        # Get exercise list
        exercises = data_service.get_exercise_list()

        return render_template("index.html", tables=tables, exercises=exercises)
    except Exception as e:
        return f"Error loading application: {e}", 500


@app.route("/api/exercises")
def get_exercises():
    """Get list of all exercises."""
    try:
        exercises = data_service.get_exercise_list()
        return jsonify(exercises)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/exercises/<int:exercise_id>")
def get_exercise(exercise_id):
    """Get details for a specific exercise."""
    try:
        exercise = data_service.get_exercise_details(exercise_id)
        if exercise:
            return jsonify(exercise)
        else:
            return jsonify({"error": "Exercise not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/tables")
def get_tables():
    """Get table schema information."""
    try:
        tables = data_service.get_table_info()
        return jsonify(tables)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/tables/<table_name>/sample")
def get_sample_data(table_name):
    """Get sample data from a table."""
    if not sql_service:
        return jsonify({"error": "SQL service not available"}), 500

    try:
        sample_data = sql_service.get_sample_data(table_name)
        return jsonify(sample_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/execute", methods=["POST"])
def execute_query():
    """Execute a SQL query."""
    if not sql_service:
        return jsonify({"error": "SQL service not available"}), 500

    try:
        data = request.get_json()
        query = data.get("query", "")

        if not query:
            return jsonify({"error": "No query provided"}), 400

        # Execute the query
        result = sql_service.execute_query(query)
        return jsonify(result)

    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500


@app.route("/api/validate", methods=["POST"])
def validate_query():
    """Validate a SQL query without executing it."""
    if not sql_service:
        return jsonify({"error": "SQL service not available"}), 500

    try:
        data = request.get_json()
        query = data.get("query", "")

        if not query:
            return jsonify({"error": "No query provided"}), 400

        # Validate the query
        result = sql_service.validate_query(query)
        return jsonify(result)

    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500


@app.route("/api/database/info")
def get_database_info():
    """Get general database information."""
    if not sql_service:
        return jsonify({"error": "SQL service not available"}), 500

    try:
        table_info = sql_service.get_table_info()
        return jsonify(table_info)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({"error": "Endpoint not found"}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return jsonify({"error": "Internal server error"}), 500


if __name__ == "__main__":
    # Check if database file exists
    try:
        db_path = data_service.get_database_path()
        print(f"Using database: {db_path}")
    except Exception as e:
        print(f"Warning: Database not found: {e}")

    # Run the app
    app.run(debug=True, host="0.0.0.0", port=5000)
