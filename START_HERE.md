# 🚀 Getting Started - Time-Keeping Application

This guide will help you start the application from scratch.

## 🎯 Choose Your Method

### Method 1: Docker (Easiest for Production) 🐳

**Prerequisites:** Install [Docker Desktop](https://www.docker.com/products/docker-desktop)

```bash
docker-compose up -d
```

**That's it!** Access the app at http://localhost

**Learn more:** See [DEPLOYMENT.md](DEPLOYMENT.md) for complete deployment guide including cloud platforms!

---

### Method 2: Python Launcher (Easy for Development)

**Prerequisites:** Python 3.11+ and Node.js 16+

```powershell
# Simply run:
python launch.py

# Or double-click:
START.bat
```

This will automatically start both servers and open your browser!

---

## 📝 Method 3: Manual Setup (Full Control)

If you prefer to start servers manually or need more control, follow these steps:

## Step 1: Set Up the Backend (Flask API)

**Good news!** This app uses SQLite, so no database installation needed!

### Open PowerShell in the project folder:
```powershell
cd "e:\Boar\My Documents\becode\Repositories\KERN-IT\backend"
```

### Create a Python virtual environment:
```powershell
python -m venv venv
```

### Activate the virtual environment:
```powershell
.\venv\Scripts\Activate.ps1
```
*Your prompt should now show `(venv)` at the beginning*

**Note:** If you get an error about execution policies, run this first:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Install Python packages:
```powershell
pip install -r requirements.txt
```
*This will take a minute or two*

**Note:** The .env file is already set up - no database password needed with SQLite!

### Initialize the database:
```powershell
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### Start the backend server:
```powershell
python run.py
```

✅ **Backend is now running!** You should see:
```
 * Running on http://127.0.0.1:5000
```

**Keep this PowerShell window open!**

## Step 2: Set Up the Frontend (React)

### Open a NEW PowerShell window:
Press `Win + X` and select "Windows PowerShell"

### Navigate to the frontend folder:
```powershell
cd "e:\Boar\My Documents\becode\Repositories\KERN-IT\frontend"
```

### Install Node packages:
```powershell
npm install
```
*This will take a few minutes*

### Create the .env file:
```powershell
# Copy the example file
copy .env.example .env
```
*The default settings should work fine*

### Start the frontend server:
```powershell
npm start
```

✅ **Frontend is now running!** 

Your browser should automatically open to `http://localhost:3000`

If it doesn't, manually open your browser and go to: **http://localhost:3000**

## Step 3: Use the Application

### First Time Setup:

1. **On the login screen**, click **"Don't have an account? Register"**

2. **Register a new account:**
   - Username: `admin` (or whatever you like)
   - Email: `admin@example.com`
   - Password: `password123`
   - Click **"Register"**

3. **Login:**
   - Use the username and password you just created
   - Click **"Sign In"**

4. **You're in!** You should now see the Dashboard

### Create Your First Project:

1. Click **"Time Entries"** in the top menu
2. Click the **"Projects"** tab
3. Click **"+ New Project"**
4. Fill in:
   - Name: `My First Project`
   - Description: `Testing the app`
   - Status: `Active`
   - Pick a color you like
5. Click **"Save"**

### Track Your First Time Entry:

1. Click the **"Time Entries"** tab
2. Click **"+ New Time Entry"**
3. Fill in:
   - Project: Select `My First Project`
   - Start Time: (defaults to now)
   - End Time: Set it to an hour from start time
   - Notes: `Testing time tracking`
   - Leave "Billable" checked
4. Click **"Create"**

🎉 **You're tracking time!**

## Troubleshooting

### "ModuleNotFoundError" when starting backend
- Make sure your virtual environment is activated: `.\venv\Scripts\Activate.ps1`
- Reinstall packages: `pip install -r requirements.txt`

### "npm: command not found"
- Node.js is not installed
- Download from: https://nodejs.org/
- Install the LTS (Long Term Support) version
- Restart PowerShell after installation

### Frontend shows blank page or errors
- Make sure backend is running in the other PowerShell window
- Check browser console (F12) for errors
- Make sure you ran `npm install` successfully

### "Compiled successfully" but page won't load
- The frontend may exit after compiling - just run `npm start` again
- Check that backend is still running on port 5000

### Port already in use
**Backend (Port 5000):**
```powershell
# Find what's using port 5000
netstat -ano | findstr :5000
# Kill the process (replace PID with the number from above)
taskkill /PID <PID> /F
```

**Frontend (Port 3000):**
```powershell
# Find what's using port 3000
netstat -ano | findstr :3000
# Kill the process
taskkill /PID <PID> /F
```

## Stopping the Application

### To stop the servers:
- In each PowerShell window, press **`Ctrl + C`**
- Type `Y` if prompted

### Next time you want to start:

**Backend (Terminal 1):**
```powershell
cd "e:\Boar\My Documents\becode\Repositories\KERN-IT\backend"
.\venv\Scripts\Activate
python run.py
```

**Frontend (Terminal 2):**
```powershell
cd "e:\Boar\My Documents\becode\Repositories\KERN-IT\frontend"
npm start
```

## Summary - What You Need Running

For the app to work, you need **2 things running**:
1. ✅ Backend Flask server (Terminal 1: `python run.py`)
2. ✅ Frontend React server (Terminal 2: `npm start`)

**Database:** SQLite runs automatically - no separate service needed!

---

**Need more help?** Check the detailed `SETUP_GUIDE.md` in the project root folder.
