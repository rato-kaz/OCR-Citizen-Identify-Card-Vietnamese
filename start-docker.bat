@echo off
echo 🐳 Starting Vietnamese OCR Service with Docker
echo ==============================================

REM Check if Docker is running
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker is not running. Please start Docker Desktop.
    pause
    exit /b 1
)

REM Build and start services
echo 🔨 Building and starting services...
docker-compose up --build -d

REM Wait for services to be ready
echo ⏳ Waiting for services to be ready...
timeout /t 10 /nobreak >nul

REM Check service health
echo 🔍 Checking service health...

REM Check backend
curl -f http://localhost:8000/api/v1/health >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Backend is healthy
) else (
    echo ❌ Backend is not responding
)

REM Check frontend
curl -f http://localhost:3000 >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Frontend is healthy
) else (
    echo ❌ Frontend is not responding
)

echo.
echo 🚀 Services are running:
echo   📱 Frontend: http://localhost:3000
echo   🔧 Backend API: http://localhost:8000
echo   📖 API Docs: http://localhost:8000/docs
echo.
echo To stop services: docker-compose down
echo To view logs: docker-compose logs -f
pause

