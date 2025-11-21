"""
Main application entry point
"""
from app import create_app, db
from app.models import User, Project, TimeEntry

app = create_app()


@app.shell_context_processor
def make_shell_context():
    """Make database models available in Flask shell"""
    return {
        'db': db,
        'User': User,
        'Project': Project,
        'TimeEntry': TimeEntry
    }


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000, use_reloader=False)
