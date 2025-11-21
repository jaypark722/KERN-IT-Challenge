# 📚 Quick Reference Guide

## Starting the Application

### Production / Deployment 🐳
**Docker (Recommended for production):**
```bash
docker-compose up -d
```
Access at: http://localhost

### Development
**Double-click:** `START.bat` (Windows)
**Or run:** `python launch.py`

### Manual Way
See [START_HERE.md](START_HERE.md) for detailed instructions.

**Need deployment help?** See [DEPLOYMENT.md](DEPLOYMENT.md)

---

## First Time Use

1. **Register an Account**
   - Click "Don't have an account? Register"
   - Fill in username, email, and password
   - Click "Register"

2. **Create Your First Project**
   - After logging in, go to "Time Entries" tab
   - Click the "Projects" tab
   - Click "+ New Project"
   - Enter project name, description, and select status
   - Click "Create Project"

3. **Track Your First Time Entry**
   - Go back to "Time Entries" tab
   - Click "+ New Time Entry"
   - Select a project
   - Set start date/time (defaults to now)
   - Optionally set end date/time
   - Add notes about what you worked on
   - Toggle "Billable" if applicable
   - Click "Save"

---

## Common Tasks

### View Dashboard
- Click "Dashboard" in the navigation
- See overview of recent entries and active projects

### Filter Time Entries
- Go to Time Entry Management
- Use the filter dropdowns:
  - Filter by project
  - Filter by date range
  - Filter by billable status

### Edit a Time Entry
- Find the entry in the Time Entries table
- Click the "Edit" button (pencil icon)
- Make your changes
- Click "Save"

### Delete a Time Entry
- Find the entry in the Time Entries table
- Click the "Delete" button (trash icon)
- Confirm deletion

### Manage Projects
- Go to "Time Entries" → "Projects" tab
- Create, edit, or view project details
- Change project status (active/completed/on-hold)

---

## URLs

- **Frontend:** http://localhost:3000
- **Backend API:** http://127.0.0.1:5000
- **API Documentation:** See backend/README.md

---

## Troubleshooting

### Using Docker

**Container won't start:**
```bash
docker-compose logs backend
docker-compose logs frontend
docker-compose logs db
```

**Restart everything:**
```bash
docker-compose restart
```

**Rebuild containers:**
```bash
docker-compose down
docker-compose up -d --build
```

**Reset database:**
```bash
docker-compose down -v  # Removes all data!
docker-compose up -d
```

### Using Development Mode

### Backend won't start
- Make sure Python 3.11+ is installed
- Check that port 5000 is not in use
- Activate virtual environment: `.\backend\venv\Scripts\Activate.ps1`
- Reinstall dependencies: `pip install -r requirements.txt`

### Frontend won't start
- Make sure Node.js 16+ is installed
- Check that port 3000 is not in use
- Clear node_modules: `rm -rf node_modules` then `npm install`

### Can't login
- Clear browser localStorage (F12 → Console → `localStorage.clear()`)
- Refresh the page
- Try registering a new account

### Time format showing AM/PM
- This is controlled by your browser/system settings
- Data is always stored in 24-hour format
- Time displays in tables use 24-hour format

---

## Default Ports

- Backend: 5000
- Frontend: 3000

To change ports:
- **Backend:** Edit `backend/run.py` (line with `app.run(...)`)
- **Frontend:** Edit `frontend/package.json` or set PORT environment variable

---

## Stopping the Application

- Close both terminal windows (backend and frontend)
- Or press `Ctrl+C` in each terminal window

---

## Database Location

SQLite database file: `backend/timekeeper.db`

To reset the database:
1. Stop the backend
2. Delete `timekeeper.db`
3. Run migrations again: `flask db upgrade`

---

## Getting Help

- Check [README.md](README.md) for project overview
- Check [START_HERE.md](START_HERE.md) for setup instructions
- Check backend/README.md for API documentation
- Check frontend/README.md for frontend details
