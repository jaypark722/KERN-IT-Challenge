# 🚀 SIMPLIFIED START GUIDE

Follow these steps **exactly** to get the app running.

## ✅ What You've Done So Far

- ✅ Created virtual environment
- ✅ Installed Python packages

## 📋 What's Next

### Step 1: Install PostgreSQL

**Download:** https://www.postgresql.org/download/windows/

1. Click "Download the installer"
2. Download the latest version for Windows x86-64
3. Run the installer
4. **Important settings during installation:**
   - Components: Select all (PostgreSQL Server, pgAdmin 4, Command Line Tools)
   - Password: Choose a password (remember it! e.g., `postgres123`)
   - Port: Keep default `5432`
   - Locale: Default locale
5. Let it complete (may take 5-10 minutes)

### Step 2: Create the Database

After PostgreSQL is installed:

1. **Open pgAdmin 4** (it was installed with PostgreSQL)
   - Search for "pgAdmin" in Windows Start menu
   
2. **Connect to server:**
   - Double-click "PostgreSQL" on the left
   - Enter the password you set during installation

3. **Create database:**
   - Right-click "Databases"
   - Select "Create" → "Database"
   - Name: `timekeeper`
   - Click "Save"

**Alternative (Command Line):**
If you prefer command line, open a NEW PowerShell window:
```powershell
# Add PostgreSQL to PATH for this session
$env:Path += ";C:\Program Files\PostgreSQL\16\bin"

# Connect to PostgreSQL
psql -U postgres

# Enter your password when prompted
# Then type:
CREATE DATABASE timekeeper;

# Exit
\q
```

### Step 3: Configure Backend

In your **current PowerShell window** (backend folder):

```powershell
# Create .env file
copy .env.example .env

# Open it for editing
notepad .env
```

**Edit the .env file** - Change this line:
```
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/timekeeper
```
Replace `YOUR_PASSWORD` with the password you set for PostgreSQL (e.g., `postgres123`)

**Save and close Notepad**

### Step 4: Initialize Database

Still in the same PowerShell window:
```powershell
# Set Flask app
$env:FLASK_APP = "run.py"

# Initialize database migrations
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### Step 5: Start Backend Server

```powershell
python run.py
```

✅ **Success!** You should see:
```
 * Running on http://127.0.0.1:5000
```

**KEEP THIS WINDOW OPEN!**

---

## 🎨 Now Start the Frontend

### Step 6: Frontend Setup (NEW PowerShell Window)

**Open a NEW PowerShell window:**
- Press `Win + X`
- Select "Windows PowerShell"

```powershell
# Go to frontend folder
cd "e:\Boar\My Documents\becode\Repositories\KERN-IT\frontend"

# Install packages (first time only)
npm install

# Start the app
npm start
```

Your browser should open to **http://localhost:3000**

---

## 🎉 You're Ready!

### First Time:
1. Click "Don't have an account? Register"
2. Create your account
3. Login
4. Start using the app!

---

## 🆘 Troubleshooting

### "npm: command not found"
**Problem:** Node.js not installed

**Fix:**
1. Download from: https://nodejs.org/
2. Install the LTS version
3. **Restart PowerShell**
4. Try `npm install` again

### Backend database error
**Problem:** Can't connect to PostgreSQL

**Fix:**
1. Check PostgreSQL is running:
   - Open Windows Services (search "Services" in Start menu)
   - Find "postgresql-x64-16" (or similar)
   - If stopped, right-click → Start
2. Check your password in `.env` file matches PostgreSQL password

### Port 5000 already in use
**Fix:**
```powershell
# Find and kill the process
netstat -ano | findstr :5000
# Note the PID (last number), then:
taskkill /PID <number> /F
```

---

## 📊 Current Status Check

Run these to verify everything:

### Check Python environment:
```powershell
# In backend folder
python --version
# Should show Python 3.14.x
```

### Check Node.js:
```powershell
node --version
npm --version
# Should show version numbers
```

### Check if backend is running:
Open browser: http://localhost:5000/api/projects
- If you see JSON response (even if empty `[]`), backend works!

---

## 🔄 Restarting Later

**Backend (Terminal 1):**
```powershell
cd "e:\Boar\My Documents\becode\Repositories\KERN-IT\backend"
.\venv\Scripts\Activate.ps1
python run.py
```

**Frontend (Terminal 2):**
```powershell
cd "e:\Boar\My Documents\becode\Repositories\KERN-IT\frontend"
npm start
```

---

**You're doing great! Just need PostgreSQL installed and you're all set! 🚀**
