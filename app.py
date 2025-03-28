from flask import Flask, request, jsonify
import pyodbc
from datetime import datetime

app = Flask(__name__)

# ----------------------------------------------------------------------------
# 1) SQL Connection Configuration
# ----------------------------------------------------------------------------
CONNECTION_STRING = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=wsil1-sql-p02;"  # Your server
    "DATABASE=IT_Projects;"  # Your database
    "UID=wsst_sqlwriter613;"  # Your SQL username
    "PWD=Wsst@Writer613;"     # Your SQL password
)


# ----------------------------------------------------------------------------
# 2) Database Connection Helper
# ----------------------------------------------------------------------------
def get_connection():
    """Returns a connection to SQL Server."""
    try:
        conn = pyodbc.connect(CONNECTION_STRING)
        return conn
    except pyodbc.Error as e:
        print(f"Database connection error: {e}")
        return None


# ----------------------------------------------------------------------------
# 3) Get Project Details and Milestones by Project ID
# ----------------------------------------------------------------------------
@app.route("/get_project_details/<int:project_id>", methods=["GET"])
def get_project_details(project_id):
    """Fetch project details and milestones by project ID."""
    conn = get_connection()
    if not conn:
        return jsonify({"error": "Database connection failed."}), 500

    cursor = conn.cursor()
    # Fetch project data
    cursor.execute("SELECT * FROM ITA_ProjectRequests WHERE ID=?", (project_id,))
    project = cursor.fetchone()

    if not project:
        return jsonify({"error": "Project not found."}), 404

    # Prepare project details
    project_data = {
        "title": project[1],
        "status": project[2],
        "activity_type": project[3],
        "category": project[4],
        "department": project[8],
        "start_date": project[10].strftime("%Y-%m-%d") if project[10] else "",
        "target_date": project[11].strftime("%Y-%m-%d") if project[11] else "",
        "comments": project[22],
    }

    # Fetch milestones for the project
    cursor.execute("SELECT * FROM ITA_Milestones WHERE ProjectID=?", (project_id,))
    milestones = [
        {
            "title": m[2],
            "start_date": m[3].strftime("%Y-%m-%d") if m[3] else "",
            "due_date": m[4].strftime("%Y-%m-%d") if m[4] else "",
            "progress": m[5],
            "comments": m[6],
        }
        for m in cursor.fetchall()
    ]

    conn.close()

    # Return project and milestones
    return jsonify({"success": True, "project": project_data, "milestones": milestones})


# ----------------------------------------------------------------------------
# 4) Run the Flask Application
# ----------------------------------------------------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
