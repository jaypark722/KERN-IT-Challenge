# 🚀 Deployment Guide - Time Keeper Application

This guide covers deploying the Time Keeper application using Docker for production environments.

## 📋 Table of Contents

- [Prerequisites](#prerequisites)
- [Quick Start with Docker](#quick-start-with-docker)
- [Production Deployment](#production-deployment)
- [Cloud Platform Deployment](#cloud-platform-deployment)
- [Environment Configuration](#environment-configuration)
- [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Install Docker

**Windows:**
- Download [Docker Desktop for Windows](https://www.docker.com/products/docker-desktop)
- Install and restart your computer
- Verify: `docker --version` and `docker-compose --version`

**Mac:**
- Download [Docker Desktop for Mac](https://www.docker.com/products/docker-desktop)
- Install and start Docker Desktop
- Verify: `docker --version` and `docker-compose --version`

**Linux:**
```bash
# Ubuntu/Debian
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo apt-get install docker-compose-plugin

# Verify
docker --version
docker compose version
```

---

## Quick Start with Docker

### 1. Start the Application

From the project root directory:

```bash
docker-compose up -d
```

This will:
- Pull required images (PostgreSQL, Python, Node.js)
- Build backend and frontend containers
- Start the database
- Run database migrations
- Start all services

### 2. Access the Application

- **Frontend:** http://localhost
- **Backend API:** http://localhost:5000
- **Database:** localhost:5432

### 3. View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f db
```

### 4. Stop the Application

```bash
docker-compose down
```

To also remove database data:
```bash
docker-compose down -v
```

---

## Production Deployment

### Step 1: Configure Environment Variables

Create `.env` file in the project root:

```env
# Database Configuration
POSTGRES_DB=timekeeper
POSTGRES_USER=timekeeper
POSTGRES_PASSWORD=CHANGE_THIS_STRONG_PASSWORD_123!

# Backend Configuration
SECRET_KEY=CHANGE_THIS_TO_A_RANDOM_STRING_MIN_32_CHARS
JWT_SECRET_KEY=CHANGE_THIS_TO_ANOTHER_RANDOM_STRING_MIN_32_CHARS
FLASK_ENV=production

# Frontend Configuration (if deploying to a domain)
REACT_APP_API_URL=https://your-domain.com/api
```

**Generate secure keys:**
```bash
# On Linux/Mac
openssl rand -hex 32

# On Windows (PowerShell)
[Convert]::ToBase64String((1..32 | ForEach-Object { Get-Random -Maximum 256 }))
```

### Step 2: Update docker-compose.yml

For production, modify `docker-compose.yml`:

```yaml
version: '3.8'

services:
  db:
    image: postgres:15-alpine
    restart: always
    environment:
      POSTGRES_DB: ${POSTGRES_DB}
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    # Don't expose port externally in production
    # ports:
    #   - "5432:5432"

  backend:
    build: ./backend
    restart: always
    environment:
      DATABASE_URL: postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@db:5432/${POSTGRES_DB}
      SECRET_KEY: ${SECRET_KEY}
      JWT_SECRET_KEY: ${JWT_SECRET_KEY}
      FLASK_ENV: production
    depends_on:
      - db
    # Only expose internally
    expose:
      - "5000"

  frontend:
    build: ./frontend
    restart: always
    ports:
      - "80:80"
    depends_on:
      - backend

volumes:
  postgres_data:
```

### Step 3: Build and Deploy

```bash
# Build containers
docker-compose build

# Start in production mode
docker-compose up -d

# Check status
docker-compose ps
```

### Step 4: Set Up HTTPS (Recommended)

Add Nginx reverse proxy with Let's Encrypt SSL:

```yaml
# Add to docker-compose.yml
  nginx:
    image: nginx:alpine
    restart: always
    ports:
      - "443:443"
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./certbot/conf:/etc/letsencrypt
      - ./certbot/www:/var/www/certbot
    depends_on:
      - frontend
      - backend

  certbot:
    image: certbot/certbot
    volumes:
      - ./certbot/conf:/etc/letsencrypt
      - ./certbot/www:/var/www/certbot
    command: certonly --webroot -w /var/www/certbot --force-renewal --email your@email.com -d your-domain.com --agree-tos
```

---

## Cloud Platform Deployment

### AWS (Amazon Web Services)

**Option 1: EC2 Instance**

1. Launch Ubuntu EC2 instance
2. Install Docker:
   ```bash
   sudo apt update
   sudo apt install docker.io docker-compose
   ```
3. Clone repository and deploy:
   ```bash
   git clone <your-repo>
   cd KERN-IT
   docker-compose up -d
   ```
4. Configure security group to allow ports 80, 443

**Option 2: AWS ECS (Elastic Container Service)**

1. Push images to ECR (Elastic Container Registry)
2. Create ECS task definition
3. Deploy as ECS service
4. Use RDS for PostgreSQL database

### DigitalOcean

**Using DigitalOcean App Platform:**

1. Connect your GitHub repository
2. Configure build settings:
   - Backend: Dockerfile at `backend/Dockerfile`
   - Frontend: Dockerfile at `frontend/Dockerfile`
3. Add PostgreSQL database
4. Configure environment variables
5. Deploy

**Using Droplet:**

1. Create Ubuntu Droplet
2. SSH into droplet
3. Install Docker:
   ```bash
   curl -fsSL https://get.docker.com -o get-docker.sh
   sudo sh get-docker.sh
   ```
4. Clone and deploy:
   ```bash
   git clone <your-repo>
   cd KERN-IT
   docker-compose up -d
   ```

### Heroku

Create `heroku.yml`:

```yaml
build:
  docker:
    web: frontend/Dockerfile
    api: backend/Dockerfile
```

Deploy:
```bash
heroku create your-app-name
heroku stack:set container
heroku addons:create heroku-postgresql:hobby-dev
git push heroku main
```

### Azure

Use Azure Container Instances or Azure App Service with Docker support.

### Google Cloud Platform

Use Cloud Run or Compute Engine with Docker.

---

## Environment Configuration

### Backend Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://user:pass@host:5432/db` |
| `SECRET_KEY` | Flask secret key (min 32 chars) | Random string |
| `JWT_SECRET_KEY` | JWT signing key (min 32 chars) | Random string |
| `FLASK_ENV` | Environment mode | `production` |

### Frontend Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `REACT_APP_API_URL` | Backend API URL | `http://localhost:5000` or `https://api.yourdomain.com` |

---

## Database Backup & Restore

### Backup Database

```bash
# Export database
docker-compose exec db pg_dump -U timekeeper timekeeper > backup.sql

# Or with Docker
docker exec timekeeper-db pg_dump -U timekeeper timekeeper > backup.sql
```

### Restore Database

```bash
# Import database
docker-compose exec -T db psql -U timekeeper timekeeper < backup.sql

# Or with Docker
docker exec -i timekeeper-db psql -U timekeeper timekeeper < backup.sql
```

---

## Monitoring & Maintenance

### Health Checks

```bash
# Check container status
docker-compose ps

# Check container health
docker inspect --format='{{.State.Health.Status}}' timekeeper-backend

# Check logs for errors
docker-compose logs --tail=100 backend
```

### Update Application

```bash
# Pull latest code
git pull origin main

# Rebuild containers
docker-compose build

# Restart with zero downtime
docker-compose up -d --no-deps --build backend
docker-compose up -d --no-deps --build frontend
```

### Database Migrations

```bash
# Create new migration
docker-compose exec backend flask db migrate -m "Description"

# Apply migrations
docker-compose exec backend flask db upgrade

# Rollback migration
docker-compose exec backend flask db downgrade
```

---

## Troubleshooting

### Container won't start

```bash
# Check logs
docker-compose logs backend

# Rebuild from scratch
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### Database connection issues

```bash
# Check database is running
docker-compose ps db

# Check database logs
docker-compose logs db

# Test connection
docker-compose exec backend python -c "from app import db; print(db.engine.url)"
```

### Port conflicts

```bash
# Change ports in docker-compose.yml
ports:
  - "8080:80"  # Frontend
  - "5001:5000"  # Backend
```

### Permission issues (Linux)

```bash
# Fix permissions
sudo chown -R $USER:$USER .
```

### Clear everything and restart

```bash
# Nuclear option - removes all data
docker-compose down -v
docker system prune -a
docker-compose up -d --build
```

---

## Performance Optimization

### Production Best Practices

1. **Use environment-specific configs**
2. **Enable HTTPS with SSL certificates**
3. **Set up database backups**
4. **Configure logging and monitoring**
5. **Use secrets management (not .env files)**
6. **Implement rate limiting**
7. **Set up health checks**
8. **Use CDN for static assets**

### Scaling

**Horizontal Scaling:**
```yaml
# Scale backend instances
docker-compose up -d --scale backend=3
```

**Use Load Balancer:**
Add Nginx or HAProxy to distribute requests.

---

## Security Checklist

- [ ] Change all default passwords
- [ ] Use strong secret keys (min 32 characters)
- [ ] Enable HTTPS with valid SSL certificate
- [ ] Don't expose database port externally
- [ ] Set up firewall rules
- [ ] Regular security updates
- [ ] Use environment variables, not hardcoded secrets
- [ ] Enable database backups
- [ ] Monitor logs for suspicious activity
- [ ] Use Docker security scanning

---

## Support

For issues or questions:
- Check logs: `docker-compose logs`
- Review [README.md](README.md)
- Check [QUICK_REFERENCE.md](QUICK_REFERENCE.md)
