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
import socket
import sys

from flask import Flask, jsonify, render_template, request
from flask_cors import CORS

from scripts.practice_app.data_service import DataService
from scripts.practice_app.sql_service import SQLService

app = Flask(__name__)
CORS(app)


def find_available_port(start_port=5001, max_attempts=10):
    """Find an available port starting from start_port with clear messaging."""
    for port in range(start_port, start_port + max_attempts):
        try:
            # Create a socket and try to bind to the port
            # Don't use SO_REUSEADDR for port detection - we want accurate availability
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.bind(("localhost", port))
                return port
        except OSError:
            # Port is already in use, show message and try the next one
            if port == start_port:
                print(
                    f"🔄 Another process running on port {port}, trying another port..."
                )
            else:
                print(f"🔄 Port {port} also busy, trying port {port + 1}...")
            continue

    # If we couldn't find an available port, raise an exception
    raise RuntimeError(
        f"Could not find an available port in range {start_port}-{start_port + max_attempts - 1}"
    )


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
    print(f"❌ Error initializing SQL service: {e}")
    print("")
    print(f"💡 Database not found for Week {week}. To fix this:")
    print("   Option 1 (Recommended): Run the full setup script:")
    print(f"     python setup.py {week}")
    print("")
    print("   Option 2: Create database manually, then restart the app:")
    if week == 4:
        print(
            "     python scripts/core/explore_dataset.py --dataset lukebarousse/data_jobs --create-database"
        )
        print(
            "     python scripts/data_schema_generation/create_tables_from_queries.py data_jobs"
        )
    elif week == 5:
        print(
            "     python scripts/core/explore_dataset.py --dataset Pablinho/movies-dataset --create-database"
        )
        print(
            "     python scripts/data_schema_generation/create_tables_from_queries.py data_movies_dataset"
        )
    else:
        print(f"     Check README.md for Week {week} database setup instructions")
    print("")
    print("🚫 App cannot start without database. Exiting...")

    sys.exit(1)


@app.route("/")
def index():
    """Main page with the SQL practice interface."""
    try:
        # Get table information for data dictionary
        tables = data_service.get_table_info()

        # Get exercise list
        exercises = data_service.get_exercise_list()

        # Get week metadata for header display
        week_metadata = data_service.get_week_metadata()

        return render_template(
            "index.html",
            tables=tables,
            exercises=exercises,
            week_metadata=week_metadata,
        )
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


@app.route("/api/score", methods=["POST"])
def score_query():
    """Score a user query against the expected solution."""
    if not sql_service:
        return jsonify({"error": "SQL service not available"}), 500

    try:
        data = request.get_json()
        user_query = data.get("user_query", "")
        solution_query = data.get("solution_query", "")

        if not user_query or not solution_query:
            return jsonify(
                {"error": "Both user_query and solution_query required"}
            ), 400

        # Execute both queries
        user_result = sql_service.execute_query(user_query)
        solution_result = sql_service.execute_query(solution_query)

        # Calculate score if both queries succeeded
        if user_result.get("success") and solution_result.get("success"):
            score_data = _calculate_query_score(user_result, solution_result)
            return jsonify(
                {
                    "success": True,
                    "user_result": user_result,
                    "solution_result": solution_result,
                    "score": score_data,
                }
            )
        else:
            # Return execution results even if one failed
            return jsonify(
                {
                    "success": False,
                    "user_result": user_result,
                    "solution_result": solution_result,
                    "score": {"percentage": 0, "details": "Query execution failed"},
                }
            )

    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500


def _calculate_query_score(user_result, solution_result):
    """Calculate the match score between user and solution results."""
    try:
        user_data = user_result.get("data", [])
        solution_data = solution_result.get("data", [])
        user_columns = user_result.get("columns", [])
        solution_columns = solution_result.get("columns", [])

        # Check if columns match
        if set(user_columns) != set(solution_columns):
            return {
                "percentage": 0,
                "details": f"Column mismatch. Expected: {solution_columns}, Got: {user_columns}",
                "matching_rows": 0,
                "total_expected_rows": len(solution_data),
                "user_row_count": len(user_data),
                "order_correct": False,
            }

        # If both results are empty, it's a perfect match
        if len(user_data) == 0 and len(solution_data) == 0:
            return {
                "percentage": 100,
                "details": "Perfect match - both queries returned no rows",
                "matching_rows": 0,
                "total_expected_rows": 0,
                "user_row_count": 0,
                "order_correct": True,
            }

        # Convert solution data to tuples for comparison
        # Sort by column names to ensure consistent ordering
        sorted_columns = sorted(solution_columns)

        def row_to_tuple(row):
            """Convert a row dict to a sorted tuple for comparison."""
            return tuple(str(row.get(col, "")) for col in sorted_columns)

        # Convert to tuples for comparison
        solution_tuples = [row_to_tuple(row) for row in solution_data]
        user_tuples = [row_to_tuple(row) for row in user_data]

        # Check if rows match regardless of order
        solution_set = set(solution_tuples)
        user_set = set(user_tuples)

        # Calculate matching rows
        matching_rows = len(solution_set.intersection(user_set))
        total_expected_rows = len(solution_data)
        user_row_count = len(user_data)

        # Check if user has the correct number of rows and all match
        has_exact_rows = user_row_count == total_expected_rows
        has_all_correct_rows = matching_rows == total_expected_rows
        has_perfect_content = has_exact_rows and has_all_correct_rows

        # Check if order is correct (only if they have perfect content)
        order_correct = has_perfect_content and solution_tuples == user_tuples

        # Calculate percentage based on completeness and correctness
        if total_expected_rows == 0:
            percentage = 100 if user_row_count == 0 else 0
        else:
            # Base percentage on matching rows, but penalize for missing or extra rows
            if user_row_count == total_expected_rows:
                # Same number of rows - percentage based on how many are correct
                percentage = round((matching_rows / total_expected_rows) * 100, 1)
            elif user_row_count < total_expected_rows:
                # Too few rows - even if all are correct, can't be 100%
                max_possible = round((user_row_count / total_expected_rows) * 100, 1)
                actual_score = round((matching_rows / total_expected_rows) * 100, 1)
                percentage = min(max_possible, actual_score)
            else:
                # Too many rows - penalize for extra rows
                percentage = round((matching_rows / total_expected_rows) * 100, 1)
                if percentage > 0:
                    # Apply penalty for extra rows (reduce by 10% for each extra row beyond 20% over)
                    extra_rows = user_row_count - total_expected_rows
                    if extra_rows > 0:
                        penalty = min(extra_rows * 5, 30)  # Max 30% penalty
                        percentage = max(0, percentage - penalty)

        # Special case: perfect content but wrong order
        if has_perfect_content and not order_correct:
            return {
                "percentage": 99,  # Almost perfect, but not quite
                "details": "Almost! But you need to get your results in the correct order!",
                "matching_rows": matching_rows,
                "total_expected_rows": total_expected_rows,
                "user_row_count": user_row_count,
                "order_correct": False,
                "has_perfect_content": True,
            }

        # Generate appropriate details message
        if percentage == 100:
            details = "Perfect match!"
        elif user_row_count < total_expected_rows:
            details = f"Found {matching_rows} correct rows, but you're missing {total_expected_rows - user_row_count} rows"
        elif user_row_count > total_expected_rows:
            details = f"Found {matching_rows} correct rows, but you have {user_row_count - total_expected_rows} extra rows"
        else:
            details = f"Found {matching_rows} of {total_expected_rows} expected rows"

        return {
            "percentage": percentage,
            "details": details,
            "matching_rows": matching_rows,
            "total_expected_rows": total_expected_rows,
            "user_row_count": user_row_count,
            "order_correct": order_correct if percentage == 100 else False,
            "has_perfect_content": has_perfect_content,
        }

    except Exception as e:
        return {
            "percentage": 0,
            "details": f"Error calculating score: {str(e)}",
            "matching_rows": 0,
            "total_expected_rows": len(solution_result.get("data", [])),
            "user_row_count": len(user_result.get("data", [])),
            "order_correct": False,
        }


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

    # Smart port detection with clear messaging
    try:
        # First try environment variable if set
        env_port = os.environ.get("SQL_PORT")
        if env_port:
            port = int(env_port)
        else:
            # Auto-detect available port with live messaging
            port = find_available_port(start_port=5001, max_attempts=10)
            if port != 5001:
                print(f"✅ Found available port {port}")

        print(f"🚀 Starting SQL Practice App on http://localhost:{port}")

        # Run the app - disable reloader to avoid confusing restart messages
        app.run(debug=True, host="0.0.0.0", port=port, use_reloader=False)

    except RuntimeError as e:
        print(f"❌ {e}")
        print("💡 Please check for running services and try again")
        sys.exit(1)
