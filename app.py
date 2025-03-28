from flask import Flask, render_template, request, redirect, url_for, jsonify
import pyodbc
from datetime import datetime

app = Flask(__name__)

# ----------------------------------------------------------------------------
# SQL Connection Configuration
# ----------------------------------------------------------------------------
CONNECTION_STRING = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=wsil1-sql-p02;"
    "DATABASE=IT_Projects;"
    "UID=wsst_sqlwriter613;"
    "PWD=Wsst@Writer613;"
)

def get_connection():
    try:
        conn = pyodbc.connect(CONNECTION_STRING)
        return conn
    except pyodbc.Error as e:
        print(f"Database connection error: {e}")
        return None

# ----------------------------------------------------------------------------
# Home Route
# ----------------------------------------------------------------------------
@app.route('/')
def index():
    return render_template('index.html')

# ----------------------------------------------------------------------------
# List Projects Route
# ----------------------------------------------------------------------------
@app.route('/list_projects')
def list_projects():
    conn = get_connection()
    if not conn:
        return jsonify({"error": "Database connection failed."}), 500
    cursor = conn.cursor()
    cursor.execute(
        "SELECT ID, Title, Status, ActivityType, Department, StartDate, TargetDate, Owner FROM ITA_ProjectRequests"
    )
    projects = cursor.fetchall()
    conn.close()
    return render_template('list_projects.html', projects=projects)

# ----------------------------------------------------------------------------
# New Project Route
# ----------------------------------------------------------------------------
@app.route('/new_project', methods=['GET', 'POST'])
def new_project():
    if request.method == 'POST':
        conn = get_connection()
        if not conn:
            return jsonify({"error": "Database connection failed."}), 500
        cursor = conn.cursor()
        try:
            # Convert form fields
            title = request.form.get('title')
            status = request.form.get('status')
            activity_type = request.form.get('activity_type')
            category = request.form.get('category')
            background = request.form.get('background')
            description = request.form.get('description')
            justification = request.form.get('justification')
            department = request.form.get('department')
            owner = request.form.get('owner')
            start_date = request.form.get('start_date') or None
            target_date = request.form.get('target_date') or None
            estimated_hours = request.form.get('estimated_hours')
            estimated_hours = int(estimated_hours) if estimated_hours and estimated_hours.strip() != "" else None
            lead = request.form.get('lead')
            it_team = request.form.get('it_team')
            other_team = request.form.get('other_team')
            rank = request.form.get('rank')
            fiscal_year = request.form.get('fiscal_year')
            project_progress = request.form.get('project_progress')
            project_progress = int(project_progress) if project_progress and project_progress.strip() != "" else 0
            color = request.form.get('color')
            car = request.form.get('car')
            po = request.form.get('po')
            comments = request.form.get('comments')

            # Insert project record
            cursor.execute(
                """
                INSERT INTO ITA_ProjectRequests 
                (Title, Status, ActivityType, Category, Background, Description, Justification, Department, Owner, StartDate, TargetDate, EstimatedHours, Lead, ITTeam, OtherTeam, Rank, FiscalYear, ProjectProgress, Color, CARNumber, PONumber, Comments)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    title, status, activity_type, category, background, description,
                    justification, department, owner, start_date, target_date,
                    estimated_hours, lead, it_team, other_team, rank, fiscal_year,
                    project_progress, color, car, po, comments
                )
            )
            # Retrieve the newly inserted project's ID
            project_id = cursor.execute("SELECT SCOPE_IDENTITY()").fetchone()[0]

            # Insert Milestones (if any)
            milestone_titles = request.form.getlist('milestone_title[]')
            milestone_start_dates = request.form.getlist('milestone_start_date[]')
            milestone_due_dates = request.form.getlist('milestone_due_date[]')
            milestone_progresses = request.form.getlist('milestone_progress[]')
            milestone_comments = request.form.getlist('milestone_comments[]')

            for i in range(len(milestone_titles)):
                progress = milestone_progresses[i]
                progress = int(progress) if progress and progress.strip() != "" else 0
                cursor.execute(
                    """
                    INSERT INTO ITA_Milestones 
                    (ProjectID, MilestoneNumber, MilestoneTitle, StartDate, DueDate, Progress, Comments)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        project_id,
                        i + 1,
                        milestone_titles[i],
                        milestone_start_dates[i] or None,
                        milestone_due_dates[i] or None,
                        progress,
                        milestone_comments[i]
                    )
                )

            conn.commit()
            return redirect(url_for('list_projects'))
        except Exception as e:
            print(f"Error during project creation: {e}")
            conn.rollback()
        finally:
            conn.close()
    return render_template('new_project.html')

# ----------------------------------------------------------------------------
# Update Project Route
# ----------------------------------------------------------------------------
@app.route('/update_project/<int:project_id>', methods=['GET', 'POST'])
def update_project(project_id):
    conn = get_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        try:
            # Convert form fields for update
            title = request.form.get('title')
            status = request.form.get('status')
            activity_type = request.form.get('activity_type')
            category = request.form.get('category')
            background = request.form.get('background')
            description = request.form.get('description')
            justification = request.form.get('justification')
            department = request.form.get('department')
            owner = request.form.get('owner')
            start_date = request.form.get('start_date') or None
            target_date = request.form.get('target_date') or None
            estimated_hours = request.form.get('estimated_hours')
            estimated_hours = int(estimated_hours) if estimated_hours and estimated_hours.strip() != "" else None
            lead = request.form.get('lead')
            it_team = request.form.get('it_team')
            other_team = request.form.get('other_team')
            rank = request.form.get('rank')
            fiscal_year = request.form.get('fiscal_year')
            project_progress = request.form.get('project_progress')
            project_progress = int(project_progress) if project_progress and project_progress.strip() != "" else 0
            color = request.form.get('color')
            car = request.form.get('car')
            po = request.form.get('po')
            comments = request.form.get('comments')

            cursor.execute(
                """
                UPDATE ITA_ProjectRequests
                SET Title=?, Status=?, ActivityType=?, Category=?, Background=?, Description=?, Justification=?, Department=?, Owner=?, StartDate=?, TargetDate=?, EstimatedHours=?, Lead=?, ITTeam=?, OtherTeam=?, Rank=?, FiscalYear=?, ProjectProgress=?, Color=?, CARNumber=?, PONumber=?, Comments=?
                WHERE ID=?
                """,
                (
                    title, status, activity_type, category, background, description,
                    justification, department, owner, start_date, target_date,
                    estimated_hours, lead, it_team, other_team, rank, fiscal_year,
                    project_progress, color, car, po, comments, project_id
                )
            )

            # Delete existing milestones and reinsert updated ones
            cursor.execute("DELETE FROM ITA_Milestones WHERE ProjectID=?", project_id)

            milestone_titles = request.form.getlist('milestone_title[]')
            milestone_start_dates = request.form.getlist('milestone_start_date[]')
            milestone_due_dates = request.form.getlist('milestone_due_date[]')
            milestone_progresses = request.form.getlist('milestone_progress[]')
            milestone_comments = request.form.getlist('milestone_comments[]')

            for i in range(len(milestone_titles)):
                progress = milestone_progresses[i]
                progress = int(progress) if progress and progress.strip() != "" else 0
                cursor.execute(
                    """
                    INSERT INTO ITA_Milestones 
                    (ProjectID, MilestoneNumber, MilestoneTitle, StartDate, DueDate, Progress, Comments)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        project_id,
                        i + 1,
                        milestone_titles[i],
                        milestone_start_dates[i] or None,
                        milestone_due_dates[i] or None,
                        progress,
                        milestone_comments[i]
                    )
                )

            conn.commit()
            return redirect(url_for('list_projects'))
        except Exception as e:
            print(f"Error during project update: {e}")
            conn.rollback()
        finally:
            conn.close()

    # GET method: retrieve the project and its milestones
    cursor.execute("SELECT * FROM ITA_ProjectRequests WHERE ID=?", (project_id,))
    project = cursor.fetchone()
    if not project:
        conn.close()
        return "Project not found", 404

    # Convert project record to list so we can modify date fields;
    # Only call strftime if the field is not already a string.
    project = list(project)
    # In ITA_ProjectRequests: StartDate at index 10, TargetDate at index 11
    if project[10] and not isinstance(project[10], str):
        project[10] = project[10].strftime("%Y-%m-%d")
    if project[11] and not isinstance(project[11], str):
        project[11] = project[11].strftime("%Y-%m-%d")

    cursor.execute("SELECT * FROM ITA_Milestones WHERE ProjectID=? ORDER BY MilestoneNumber", (project_id,))
    milestones = cursor.fetchall()
    milestones_list = []
    for m in milestones:
        m = list(m)
        # For ITA_Milestones, based on your table:
        # m[0] = MilestoneID, m[1] = ProjectID, m[2] = MilestoneNumber, m[3] = MilestoneTitle,
        # m[4] = StartDate, m[5] = DueDate, m[6] = Progress, m[7] = Comments, etc.
        if m[4] and not isinstance(m[4], str):
            m[4] = m[4].strftime("%Y-%m-%d")
        if m[5] and not isinstance(m[5], str):
            m[5] = m[5].strftime("%Y-%m-%d")
        milestones_list.append(m)
    conn.close()

    return render_template('update_project.html', project=project, milestones=milestones_list)

# ----------------------------------------------------------------------------
# Close Project Route
# ----------------------------------------------------------------------------
@app.route('/close_project/<int:project_id>', methods=['POST'])
def close_project(project_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            UPDATE ITA_ProjectRequests
            SET Status='Completed/Closed'
            WHERE ID=?
            """,
            (project_id,)
        )
        conn.commit()
        return redirect(url_for('list_projects'))
    except Exception as e:
        print(f"Error closing project: {e}")
        conn.rollback()
    finally:
        conn.close()

# ----------------------------------------------------------------------------
# Delete Project Route
# ----------------------------------------------------------------------------
@app.route('/delete_project/<int:project_id>', methods=['POST'])
def delete_project(project_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM ITA_Milestones WHERE ProjectID=?", (project_id,))
        cursor.execute("DELETE FROM ITA_ProjectRequests WHERE ID=?", (project_id,))
        conn.commit()
        return redirect(url_for('list_projects'))
    except Exception as e:
        print(f"Error deleting project: {e}")
        conn.rollback()
    finally:
        conn.close()

# ----------------------------------------------------------------------------
# Run Flask Application
# ----------------------------------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True)
