@echo off
echo Starting Dronzer AI Gateway...

echo [1/2] Starting Backend API in a new window...
start "Dronzer Backend" cmd /k "cd backend && call venv\Scripts\activate.bat && uvicorn dronzer.presentation.api.server:create_app --factory --reload --port 8000"

echo [2/2] Starting Frontend Dashboard in a new window...
start "Dronzer Frontend" cmd /k "cd frontend && npm run dev"

echo.
echo Both servers are starting up!
echo You can access the dashboard at: http://localhost:3000
echo You can access the API docs at:  http://localhost:8000/docs
echo.
pause
