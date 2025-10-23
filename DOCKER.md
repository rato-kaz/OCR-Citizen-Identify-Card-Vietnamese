# 🐳 Docker Setup for Vietnamese OCR Service

Complete Docker setup for running the Vietnamese OCR Service without installing Node.js or Python dependencies locally.

## 🚀 Quick Start

### Prerequisites
- Docker Desktop installed and running
- At least 4GB RAM available for Docker

### Start the Application

**Windows:**
```bash
start-docker.bat
```

**Linux/Mac:**
```bash
chmod +x start-docker.sh
./start-docker.sh
```

**Manual:**
```bash
docker-compose up --build -d
```

## 📱 Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend       │    │   AI Models     │
│   (React + Nginx)│◄──►│   (FastAPI)     │◄──►│   (YOLO + OCR)   │
│   Port: 3000    │    │   Port: 8000    │    │   In Container   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🔧 Services

### Backend Service
- **Container**: `ocr-backend`
- **Port**: 8000
- **Health Check**: http://localhost:8000/api/v1/health
- **Features**: YOLO + VietOCR pipeline

### Frontend Service
- **Container**: `ocr-frontend`
- **Port**: 3000
- **Features**: React app with drag & drop upload

## 📋 Available Commands

### Start Services
```bash
# Start all services
docker-compose up -d

# Start with rebuild
docker-compose up --build -d

# Start specific service
docker-compose up backend
docker-compose up frontend
```

### Stop Services
```bash
# Stop all services
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

### View Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
```

### Debug Services
```bash
# Access backend container
docker exec -it ocr-backend bash

# Access frontend container
docker exec -it ocr-frontend sh

# Check service status
docker-compose ps
```

## 🛠️ Development

### Rebuild After Code Changes
```bash
# Rebuild and restart
docker-compose up --build -d

# Rebuild specific service
docker-compose build backend
docker-compose up -d backend
```

### Environment Variables
Create `.env` file for custom configuration:
```env
# Backend
LOG_LEVEL=INFO
DEVICE=cuda:0

# Frontend
REACT_APP_API_URL=http://localhost:8000
```

## 🚨 Troubleshooting

### Common Issues

1. **Port already in use**
   ```bash
   # Check what's using the port
   netstat -ano | findstr :8000
   netstat -ano | findstr :3000
   ```

2. **Docker not running**
   ```bash
   # Start Docker Desktop
   # Check Docker status
   docker info
   ```

3. **Out of memory**
   ```bash
   # Increase Docker memory limit in Docker Desktop settings
   # Recommended: 4GB+ RAM
   ```

4. **Models not loading**
   ```bash
   # Check if models directory exists
   ls -la models/
   
   # Check backend logs
   docker-compose logs backend
   ```

### Reset Everything
```bash
# Stop and remove everything
docker-compose down -v
docker system prune -a

# Start fresh
docker-compose up --build -d
```

## 📊 Monitoring

### Health Checks
- Backend: http://localhost:8000/api/v1/health
- Frontend: http://localhost:3000

### Resource Usage
```bash
# View resource usage
docker stats

# View container details
docker-compose ps
```

## 🔒 Production Deployment

For production, use the nginx reverse proxy:
```bash
# Start with nginx proxy
docker-compose --profile production up -d

# Access via port 80
http://localhost
```

## 📁 File Structure
```
├── docker-compose.yml          # Main compose file
├── Dockerfile.backend          # Backend Dockerfile
├── frontend/
│   ├── Dockerfile             # Frontend Dockerfile
│   └── nginx.conf             # Frontend nginx config
├── nginx/
│   └── nginx.conf             # Production nginx config
├── start-docker.sh            # Linux/Mac startup script
├── start-docker.bat            # Windows startup script
└── .dockerignore              # Docker ignore file
```

