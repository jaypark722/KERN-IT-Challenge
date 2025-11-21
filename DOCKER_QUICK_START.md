# 🐳 Docker Quick Start

## For Users Who Just Want to Run the App

### 1. Install Docker
- **Windows/Mac:** [Download Docker Desktop](https://www.docker.com/products/docker-desktop)
- **Linux:** `curl -fsSL https://get.docker.com | sh`

### 2. Start the Application
```bash
# Navigate to project folder
cd KERN-IT

# Start everything
docker compose up -d
```

### 3. Access the App
Open your browser to: **http://localhost**

That's it! The app is running with:
- PostgreSQL database
- Flask API backend  
- React frontend

---

## Useful Commands

```bash
# View logs
docker compose logs -f

# Stop the application
docker compose down

# Restart after code changes
docker compose restart backend
docker compose restart frontend

# Reset everything (⚠️ deletes all data)
docker compose down -v
docker compose up -d --build
```

---

## What Gets Installed?

Docker will automatically:
- ✅ Install PostgreSQL database
- ✅ Install all Python dependencies
- ✅ Install all Node.js dependencies
- ✅ Build the React app
- ✅ Configure Nginx web server
- ✅ Run database migrations

**No manual setup required!**

---

## For Production Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for:
- Environment configuration
- Security best practices
- Cloud platform deployment (AWS, Azure, DigitalOcean, etc.)
- HTTPS setup
- Backup strategies
- Monitoring and scaling

---

## Switching Between Docker and Development Mode

**Docker (Production):**
```bash
docker compose up -d
```
Access at: http://localhost

**Development Mode (SQLite):**
```bash
python launch.py
```
Access at: http://localhost:3000

Both modes work! Choose based on your needs:
- **Docker** → Production, deployment, team collaboration
- **Development** → Coding, testing, debugging
