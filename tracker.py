from js import document

def process_project():
    """Process project data and display results."""
    project_title = document.getElementById("project_title").value
    project_status = document.getElementById("project_status").value
    estimated_hours = document.getElementById("estimated_hours").value

    # Basic validation
    if not project_title or not estimated_hours:
        document.getElementById("result_area").innerHTML = "<p style='color: red;'>Please fill out all fields.</p>"
        return

    # Display project summary
    result_message = f"""
    <h3>Project Summary</h3>
    <p><b>Title:</b> {project_title}</p>
    <p><b>Status:</b> {project_status}</p>
    <p><b>Estimated Hours:</b> {estimated_hours}</p>
    """
    document.getElementById("result_area").innerHTML = result_message
