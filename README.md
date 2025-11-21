# Time-Keeping Application

A full-stack web application for tracking time across projects with a RESTful API backend and modern React frontend.

## What Does This App Do?

**Time Keeper** is a professional time tracking application that helps you:
- **Track Time**: Log hours worked on different projects with start/end times
- **Manage Projects**: Create and organize multiple projects with custom details
- **Billable Hours**: Mark time entries as billable or non-billable for invoicing
- **Filter & Search**: Find time entries by project, date range, or billing status
- **View Statistics**: See summary reports of total hours worked
- **User Authentication**: Secure login system with JWT tokens

Perfect for freelancers, consultants, or anyone who needs to track time spent on various projects!

## Key Features

### User Management
- Secure registration and login
- JWT token-based authentication
- Password hashing with Werkzeug

### Project Management
- Create, edit, and delete projects
- Set project status (active, completed, on-hold)
- Add project descriptions and details
- View project statistics

### Time Tracking
- Log time entries with start and end times
- Support for both AM/PM and 24-hour time formats
- Add notes to each time entry
- Mark entries as billable or non-billable
- Edit or delete existing entries
- Calculate duration automatically

### Dashboard & Reports
- View recent time entries at a glance
- See active projects with statistics
- Filter entries by project, date range, or billing status
- Summary statistics for total hours worked

## Quick Start

### Option 1: Docker (Recommended)

The easiest way to run the application:

```bash
docker-compose up -d
```

This will:
- Start PostgreSQL database
- Build and start Flask backend
- Build and start React frontend with Nginx
- Run database migrations automatically

**Access the application:**
- Frontend: http://localhost
- Backend API: http://localhost:5000

To stop the services:
```bash
docker-compose down
```

---

## Option 2: Manual Setup

If you prefer to run the backend and frontend separately for development:

##  Architecture

### Backend (Flask + SQLite)
- **Framework**: Flask 3.0
- **Database**: SQLite with SQLAlchemy ORM (no installation required!)
- **Authentication**: JWT-based with token refresh
- **API**: RESTful endpoints with JSON responses
- **Python Version**: 3.13+ recommended (3.11+ supported)

### Frontend (React)
- **Framework**: React 18 with functional components
- **Routing**: React Router v6
- **State Management**: Context API + Hooks
- **Styling**: Modern responsive CSS with component-scoped styles
- **HTTP Client**: Axios with JWT interceptors

## Project Structure

```
KERN-IT/
├── backend/                 # Flask API server
│   ├── app/
│   │   ├── models/         # Database models (User, Project, TimeEntry)
│   │   ├── routes/         # API endpoints (auth, projects, time_entries)
│   │   └── __init__.py     # Application factory
│   ├── config.py           # Configuration settings
│   ├── run.py              # Application entry point
│   ├── requirements.txt    # Python dependencies
│   └── README.md           # Backend documentation
│
└── frontend/               # React SPA
    ├── public/
    ├── src/
    │   ├── components/     # React components
    │   │   ├── auth/       # Login/Register
    │   │   ├── common/     # Shared components
    │   │   ├── projects/   # Project management
    │   │   ├── timeEntries/# Time entry components
    │   │   └── views/      # Dashboard, TimeEntryManagement
    │   ├── contexts/       # AuthContext
    │   ├── services/       # API service layer
    │   └── App.js          # Main application
    ├── package.json        # Node dependencies
    └── README.md           # Frontend documentation
```

### Prerequisites

- **Python 3.8+**
- **Node.js 16+** and npm
- **PostgreSQL 12+** (or use Docker which includes PostgreSQL)

### Backend Setup

1. **Navigate to backend directory**:
   ```bash
   cd backend
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**:
   ```bash
   cp .env.example .env
   ```
   Edit `.env` with your database URL and secret keys.

5. **Initialize database**:
   ```bash
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

6. **Run the server**:
   ```bash
   python run.py
   ```
   Backend runs at `http://localhost:5000`

### Frontend Setup

1. **Navigate to frontend directory**:
   ```bash
   cd frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Configure environment**:
   ```bash
   cp .env.example .env
   ```

4. **Start development server**:
   ```bash
   npm start
   ```
   Frontend runs at `http://localhost:3000`

## Database Schema

### User
- `id`, `username`, `email`, `password_hash`
- `first_name`, `last_name`, `is_active`
- Timestamps: `created_at`, `updated_at`

### Project
- `id`, `name`, `description`, `status`
- `color` (for UI display)
- Timestamps: `created_at`, `updated_at`

### TimeEntry
- `id`, `user_id`, `project_id`
- `start_time`, `end_time`, `duration` (calculated)
- `notes`, `is_billable`
- Timestamps: `created_at`, `updated_at`

## Authentication

JWT-based authentication with:
- Access tokens (1 hour expiry)
- Refresh tokens (30 days expiry)
- Automatic token refresh on 401 errors
- Token blacklisting for logout

## Features

### Dashboard
- Summary statistics (total hours, billable/non-billable)
- Active projects overview
- Recent time entries

### Time Entry Management
- Create/Edit/Delete time entries
- Filter by project, date range, billability
- Automatic duration calculation
- Notes for each entry

### Project Management
- CRUD operations for projects
- Custom colors for visual distinction
- Status tracking (active, completed, archived)
- Project-level statistics

## API Endpoints

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login
- `POST /auth/logout` - Logout
- `POST /auth/refresh` - Refresh token
- `GET /auth/me` - Get current user

### Projects
- `GET /api/projects` - List projects
- `POST /api/projects` - Create project
- `PUT /api/projects/:id` - Update project
- `DELETE /api/projects/:id` - Delete project

### Time Entries
- `GET /api/entries` - List entries (with filters)
- `POST /api/entries` - Create entry
- `PUT /api/entries/:id` - Update entry
- `DELETE /api/entries/:id` - Delete entry
- `GET /api/entries/summary` - Get statistics

## Technologies Used

### Backend
- Flask 3.0
- SQLAlchemy (ORM)
- Flask-Migrate (Database migrations)
- Flask-JWT-Extended (Authentication)
- Flask-CORS (CORS support)
- psycopg2-binary (PostgreSQL adapter)
- Werkzeug (Password hashing)

### Frontend
- React 18
- React Router v6
- Axios
- CSS3 (Responsive design)

## Development Notes

- Backend uses application factory pattern
- Frontend uses functional components and hooks
- JWT tokens stored in localStorage
- Automatic token refresh on expiration
- CORS enabled for cross-origin requests
- Password hashing with Werkzeug
- Responsive design for mobile/tablet/desktop

## Security Considerations

- Passwords hashed using Werkzeug
- JWT tokens for stateless authentication
- Token blacklisting for logout
- CORS configuration
- Environment variables for sensitive data
- SQL injection protection via ORM

## License

This project is created for educational purposes.

## Author

KERN-IT Project

---

**Happy Time Tracking! ⏱️**
