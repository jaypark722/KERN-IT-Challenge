# Time-Keeping Application - Backend

A Flask-based RESTful API for time tracking and project management.

## Features

- **User Authentication**: JWT-based authentication with login/logout
- **Project Management**: Create, update, delete, and view projects
- **Time Tracking**: Record time entries with start/end times, automatic duration calculation
- **Filtering & Reporting**: Query time entries by project, date range, and billability

## Tech Stack

- **Framework**: Flask 3.0
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Authentication**: Flask-JWT-Extended
- **Migrations**: Flask-Migrate

## Setup Instructions

### Prerequisites

- Python 3.8+
- PostgreSQL database

### Installation

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment**:
   ```bash
   cp .env.example .env
   ```
   Edit `.env` with your database credentials and secret keys.

3. **Initialize database**:
   ```bash
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

4. **Run the application**:
   ```bash
   python run.py
   ```

The API will be available at `http://localhost:5000`

## API Endpoints

### Authentication
- `POST /auth/register` - Register a new user
- `POST /auth/login` - Login and receive JWT tokens
- `POST /auth/logout` - Logout (blacklist token)
- `POST /auth/refresh` - Refresh access token
- `GET /auth/me` - Get current user info

### Projects
- `GET /api/projects` - List all projects
- `GET /api/projects/<id>` - Get project details
- `POST /api/projects` - Create new project
- `PUT /api/projects/<id>` - Update project
- `DELETE /api/projects/<id>` - Delete project

### Time Entries
- `GET /api/entries` - List time entries (with filters)
- `GET /api/entries/<id>` - Get time entry details
- `POST /api/entries` - Create new time entry
- `PUT /api/entries/<id>` - Update time entry
- `DELETE /api/entries/<id>` - Delete time entry
- `GET /api/entries/summary` - Get time tracking statistics

## Database Models

### User
- Username, email, password (hashed)
- First name, last name
- Active status

### Project
- Name, description
- Status (active, archived, completed)
- Color (for UI)

### TimeEntry
- User and project references
- Start time, end time, duration (auto-calculated)
- Notes, billable flag

## Security

- Passwords are hashed using Werkzeug's security helpers
- JWT tokens for stateless authentication
- CORS enabled for frontend integration
- Token blacklisting for logout functionality
