# Time-Keeping Application - Frontend

A React-based single-page application for time tracking and project management.

## Features

- **User Authentication**: Secure login/registration with JWT tokens
- **Dashboard**: View summary statistics and recent activity
- **Time Entry Management**: Create, edit, delete, and filter time entries
- **Project Management**: Organize time entries by projects with custom colors
- **Responsive Design**: Clean, modern UI that works on desktop and mobile

## Tech Stack

- **Framework**: React 18
- **Routing**: React Router v6
- **HTTP Client**: Axios
- **State Management**: React Context API and Hooks
- **Styling**: Pure CSS with modern responsive design

## Setup Instructions

### Prerequisites

- Node.js 16+ and npm

### Installation

1. **Install dependencies**:
   ```bash
   npm install
   ```

2. **Configure environment**:
   ```bash
   cp .env.example .env
   ```
   Edit `.env` to set the backend API URL (default: `http://localhost:5000`)

3. **Start development server**:
   ```bash
   npm start
   ```

The app will be available at `http://localhost:3000`

### Build for Production

```bash
npm run build
```

This creates an optimized production build in the `build/` directory.

## Project Structure

```
src/
├── components/
│   ├── auth/              # Authentication components
│   │   ├── LoginScreen.js
│   │   └── LoginScreen.css
│   ├── common/            # Shared components
│   │   └── PrivateRoute.js
│   ├── projects/          # Project management
│   │   ├── ProjectList.js
│   │   └── ProjectList.css
│   ├── timeEntries/       # Time entry components
│   │   ├── TimeEntryTable.js
│   │   ├── TimeEntryTable.css
│   │   ├── TimeEntryForm.js
│   │   └── TimeEntryForm.css
│   └── views/             # Main views
│       ├── Dashboard.js
│       ├── Dashboard.css
│       ├── TimeEntryManagement.js
│       └── TimeEntryManagement.css
├── contexts/              # React contexts
│   └── AuthContext.js
├── services/              # API services
│   └── api.js
├── App.js                 # Main app component
├── App.css                # Global styles
├── index.js               # Entry point
└── index.css              # Base styles
```

## Key Components

### AuthContext
Manages user authentication state, login/logout, and JWT token handling with automatic refresh.

### Dashboard
Displays summary statistics, active projects, and recent time entries.

### TimeEntryManagement
Main view for managing time entries and projects with filtering capabilities.

### TimeEntryTable
Displays time entries in a table with filtering options (project, date range, billability).

### TimeEntryForm
Modal form for creating and editing time entries.

### ProjectList
Manages projects with CRUD operations and status tracking.

## API Integration

The frontend communicates with the Flask backend via RESTful API calls:

- `/auth/*` - Authentication endpoints
- `/api/projects` - Project management
- `/api/entries` - Time entry management

Axios interceptors handle:
- Automatic token injection
- Token refresh on 401 errors
- Error handling

## Styling

Clean, modern design with:
- Responsive grid layouts
- Custom button styles
- Form components
- Card-based UI
- Color-coded projects
- Status badges

## State Management

Uses React Context API for:
- Authentication state
- User information
- Token management

Component-level state with `useState` for:
- Form data
- Loading states
- Error handling
- Filters
