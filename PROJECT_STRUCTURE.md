# Time-Keeping Application - Project Structure

Complete file structure of the Time-Keeping Application.

```
KERN-IT/
│
├── README.md                          # Main project documentation
├── SETUP_GUIDE.md                     # Detailed setup instructions
├── .gitignore                         # Root gitignore
│
├── backend/                           # Flask API Backend
│   ├── app/
│   │   ├── __init__.py               # Application factory
│   │   ├── models/
│   │   │   ├── __init__.py           # Models package init
│   │   │   ├── user.py               # User model (auth, hashed passwords)
│   │   │   ├── project.py            # Project model (name, status, color)
│   │   │   └── time_entry.py         # TimeEntry model (duration tracking)
│   │   └── routes/
│   │       ├── __init__.py           # Routes package init
│   │       ├── auth.py               # Auth endpoints (login, logout, register)
│   │       ├── projects.py           # Project CRUD endpoints
│   │       └── time_entries.py       # Time entry CRUD + summary endpoints
│   ├── config.py                      # Flask configuration
│   ├── run.py                         # Application entry point
│   ├── requirements.txt               # Python dependencies
│   ├── .env.example                   # Environment template
│   ├── .gitignore                     # Backend gitignore
│   └── README.md                      # Backend documentation
│
└── frontend/                          # React Frontend SPA
    ├── public/
    │   └── index.html                # HTML template
    ├── src/
    │   ├── components/
    │   │   ├── auth/
    │   │   │   ├── LoginScreen.js    # Login/Register form
    │   │   │   └── LoginScreen.css   # Login styles
    │   │   ├── common/
    │   │   │   └── PrivateRoute.js   # Route protection HOC
    │   │   ├── projects/
    │   │   │   ├── ProjectList.js    # Project management UI
    │   │   │   └── ProjectList.css   # Project styles
    │   │   ├── timeEntries/
    │   │   │   ├── TimeEntryTable.js # Time entry table with filters
    │   │   │   ├── TimeEntryTable.css
    │   │   │   ├── TimeEntryForm.js  # Create/Edit time entry form
    │   │   │   └── TimeEntryForm.css
    │   │   └── views/
    │   │       ├── Dashboard.js      # Main dashboard view
    │   │       ├── Dashboard.css
    │   │       ├── TimeEntryManagement.js  # Time entry management view
    │   │       └── TimeEntryManagement.css
    │   ├── contexts/
    │   │   └── AuthContext.js        # Authentication context & hooks
    │   ├── services/
    │   │   └── api.js                # Axios instance with interceptors
    │   ├── App.js                     # Main app with routing
    │   ├── App.css                    # Global app styles
    │   ├── index.js                   # React entry point
    │   └── index.css                  # Base styles
    ├── package.json                   # Node dependencies
    ├── .env.example                   # Environment template
    ├── .gitignore                     # Frontend gitignore
    └── README.md                      # Frontend documentation
```

## Component Relationships

### Backend Data Flow
```
Client Request
    ↓
Flask Routes (auth.py, projects.py, time_entries.py)
    ↓
JWT Authentication (flask-jwt-extended)
    ↓
Database Models (User, Project, TimeEntry)
    ↓
SQLAlchemy ORM
    ↓
PostgreSQL Database
```

### Frontend Component Hierarchy
```
App.js (Router + AuthProvider)
    ├── LoginScreen (Public)
    └── PrivateRoute
        ├── Dashboard
        │   ├── Summary Cards
        │   ├── Project Cards
        │   └── Recent Entries Table
        └── TimeEntryManagement
            ├── TimeEntryTable (with filters)
            ├── TimeEntryForm (modal)
            └── ProjectList
```

### State Management Flow
```
AuthContext (Global)
    ├── User State
    ├── Token Management
    └── Auth Methods (login, logout, refresh)

Component State (Local)
    ├── Form Data (useState)
    ├── Loading States (useState)
    ├── Error Handling (useState)
    └── Filters (useState)
```

## Key Files Description

### Backend

**`app/__init__.py`**
- Application factory pattern
- Initializes Flask extensions (SQLAlchemy, Migrate, JWT, CORS)
- Registers blueprints

**`app/models/user.py`**
- User authentication model
- Password hashing with Werkzeug
- Relationship to TimeEntry

**`app/models/project.py`**
- Project organization model
- Status tracking (active/completed/archived)
- Statistics calculation methods

**`app/models/time_entry.py`**
- Time tracking model
- Auto-calculates duration
- Foreign keys to User and Project

**`app/routes/auth.py`**
- JWT token creation and validation
- Login/logout/register endpoints
- Token blacklist management

**`app/routes/projects.py`**
- Project CRUD operations
- Optional statistics inclusion
- JWT protection

**`app/routes/time_entries.py`**
- Time entry CRUD operations
- Advanced filtering (project, date, billability)
- Summary statistics endpoint

**`config.py`**
- Database configuration
- JWT settings
- CORS configuration

### Frontend

**`App.js`**
- Main application component
- React Router setup
- Protected route configuration

**`contexts/AuthContext.js`**
- Global authentication state
- Login/logout/register methods
- Token refresh logic
- Auto-fetch user on mount

**`services/api.js`**
- Axios HTTP client
- Request interceptor (adds token)
- Response interceptor (handles 401, refreshes token)

**`components/auth/LoginScreen.js`**
- Dual-mode form (login/register)
- Form validation
- Error handling

**`components/views/Dashboard.js`**
- Summary statistics display
- Active projects overview
- Recent entries list
- Navigation to detailed views

**`components/views/TimeEntryManagement.js`**
- Tab-based navigation (Entries/Projects)
- Modal form management
- Data fetching and refresh

**`components/timeEntries/TimeEntryTable.js`**
- Filterable table display
- Project/date/billability filters
- Edit/delete actions
- Summary footer

**`components/timeEntries/TimeEntryForm.js`**
- Create/edit modal form
- Project selection
- Date/time pickers
- Billable checkbox

**`components/projects/ProjectList.js`**
- Project CRUD interface
- Inline form for create/edit
- Status management
- Color picker

## Dependencies Overview

### Backend (Python)
- **Flask**: Web framework
- **SQLAlchemy**: ORM for database
- **Flask-Migrate**: Database migrations
- **Flask-JWT-Extended**: JWT authentication
- **Flask-CORS**: Cross-origin support
- **psycopg2-binary**: PostgreSQL driver
- **Werkzeug**: Security utilities

### Frontend (JavaScript)
- **React**: UI library
- **React Router**: Client-side routing
- **Axios**: HTTP client
- **React Scripts**: Build tooling

## 🎨 Styling Architecture

### CSS Structure
- **index.css**: Base/reset styles, typography
- **App.css**: Global component styles (buttons, forms, cards, tables)
- **Component CSS**: Scoped styles for each component

### Design System
- **Colors**: Blue (#3B82F6) primary, semantic colors for status
- **Typography**: System fonts, consistent sizing
- **Spacing**: 4px base unit, consistent padding/margins
- **Responsive**: Mobile-first, breakpoint at 768px
- **Components**: Reusable button, form, card, table styles

## 🔒 Security Features

1. **Password Security**: Werkzeug hashing (pbkdf2:sha256)
2. **JWT Tokens**: Short-lived access (1h), long refresh (30d)
3. **Token Blacklist**: Logout invalidates tokens
4. **CORS**: Configured for specific origins
5. **SQL Injection**: Protected via SQLAlchemy ORM
6. **Environment Variables**: Sensitive data in .env

## 📝 Database Schema Summary

```sql
users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
)

projects (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    status VARCHAR(20) DEFAULT 'active',
    color VARCHAR(7) DEFAULT '#3B82F6',
    created_at TIMESTAMP,
    updated_at TIMESTAMP
)

time_entries (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    project_id INTEGER REFERENCES projects(id),
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP,
    duration INTEGER,  -- seconds
    notes TEXT,
    is_billable BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
)
```

## 🚀 Running the Application

### Development Mode
1. **Terminal 1** (Backend):
   ```bash
   cd backend
   venv\Scripts\activate
   python run.py
   ```

2. **Terminal 2** (Frontend):
   ```bash
   cd frontend
   npm start
   ```

### Access Points
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:5000
- **PostgreSQL**: localhost:5432

---

**Complete full-stack Time-Keeping Application ready for development!** 🎉
