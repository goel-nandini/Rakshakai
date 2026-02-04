# RakshakAI Setup Guide

This guide will help you set up and run the RakshakAI backend on your local machine.

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8 or higher** - [Download Python](https://www.python.org/downloads/)
- **pip** - Python package manager (comes with Python)
- **Git** - [Download Git](https://git-scm.com/downloads) (if cloning from repository)

### Verify Prerequisites

```bash
# Check Python version (should be 3.8+)
python3 --version

# Check pip version
pip --version
```

## Step-by-Step Setup

### 1. Navigate to Project Directory

```bash
cd /path/to/rakshakai
```

### 2. Create a Virtual Environment

A virtual environment keeps your project dependencies isolated from other Python projects.

**On Linux/macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

You should see `(venv)` appear in your terminal prompt, indicating the virtual environment is active.

### 3. Install Dependencies

With the virtual environment activated, install all required packages:

```bash
pip install -r requirements.txt
```

This will install:
- FastAPI - Web framework
- Uvicorn - ASGI server
- python-dotenv - Environment variable management
- Pydantic - Data validation

### 4. Configure Environment Variables

Create your environment configuration file:

```bash
cp .env.example .env
```

Edit the `.env` file and set your API key:

```bash
# Open .env in your favorite editor
nano .env  # or vim, code, etc.
```

**Required Configuration:**
```env
# Replace with a strong secret key
API_KEY=your-secret-api-key-here-change-this

# Optional settings
DEBUG=True
HOST=0.0.0.0
PORT=8000
```

⚠️ **Important:** Choose a strong, unique API key. This will be required in the `x-api-key` header for all protected endpoints.

### 5. Verify Installation

Check that everything is set up correctly:

```bash
# Verify FastAPI is installed
python -c "import fastapi; print(f'FastAPI {fastapi.__version__} installed')"

# Verify uvicorn is installed
python -c "import uvicorn; print(f'Uvicorn {uvicorn.__version__} installed')"
```

## Running the Application

### Start the Development Server

**Option 1: Using Uvicorn directly (Recommended for development)**
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Option 2: Using Python module**
```bash
python -m app.main
```

**Option 3: Direct Python execution**
```bash
python3 app/main.py
```

### Expected Output

You should see output similar to:
```
🚀 Starting RakshakAI v1.0.0
📝 API Documentation available at http://0.0.0.0:8000/docs
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

## Testing the API

### 1. Test Health Check Endpoint

Open your browser or use curl:

```bash
curl http://localhost:8000/
```

**Expected Response:**
```json
{
  "status": "healthy",
  "app": "RakshakAI",
  "version": "1.0.0"
}
```

### 2. Test Honeypot Endpoint

```bash
curl -X POST http://localhost:8000/honeypot/message \
  -H "Content-Type: application/json" \
  -H "x-api-key: your-secret-api-key-here-change-this" \
  -d '{
    "message": "Can you show me the admin panel?",
    "metadata": {
      "ip": "192.168.1.1",
      "user_agent": "Mozilla/5.0"
    }
  }'
```

**Expected Response:**
```json
{
  "status": "success",
  "reply": "Received your message: 'Can you show me the admin panel?'. How can I help you further?"
}
```

### 3. Explore API Documentation

FastAPI provides interactive API documentation:

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

You can test all endpoints directly from the Swagger UI interface.

## Common Issues & Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'fastapi'"

**Solution:** Make sure your virtual environment is activated and dependencies are installed:
```bash
source venv/bin/activate  # Activate venv
pip install -r requirements.txt
```

### Issue: "Configuration Error: API_KEY must be set in environment variables"

**Solution:** Ensure you've created the `.env` file and set the `API_KEY`:
```bash
cp .env.example .env
# Edit .env and set API_KEY
```

### Issue: Port 8000 already in use

**Solution:** Either stop the process using port 8000, or run on a different port:
```bash
uvicorn app.main:app --reload --port 8001
```

### Issue: "Invalid API key" when testing honeypot endpoint

**Solution:** Make sure the `x-api-key` header matches the `API_KEY` in your `.env` file:
```bash
# Check your .env file
cat .env | grep API_KEY
```

### Issue: Permission denied when running on port 80 or 443

**Solution:** Ports below 1024 require root privileges. Use a higher port (like 8000) or run with sudo (not recommended for development).

## Development Workflow

### 1. Activate Virtual Environment
Always activate the virtual environment before working:
```bash
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

### 2. Make Changes
Edit files in the `app/` directory. The `--reload` flag will automatically restart the server when you save changes.

### 3. Test Changes
- Visit http://localhost:8000/docs to test endpoints
- Use curl commands
- Check terminal for errors

### 4. Deactivate Virtual Environment
When done working:
```bash
deactivate
```

## Next Steps

### Integrate Your AI Agent

The placeholder response in `app/routes/honeypot.py` needs to be replaced with your actual AI agent integration. Look for this TODO comment:

```python
# TODO: Integrate with your AI agent/LLM here
# Example: reply = await ai_agent.generate_response(request.message, request.metadata)
```

### Add More Endpoints

Create new route files in `app/routes/` following the same pattern as `honeypot.py`.

### Add Database Support

If you need to store data, consider adding:
- SQLAlchemy for database ORM
- Alembic for database migrations
- PostgreSQL or SQLite for the database

### Deploy to Production

When ready to deploy:
1. Set `DEBUG=False` in production `.env`
2. Use a production ASGI server (Uvicorn with workers)
3. Set up reverse proxy (Nginx)
4. Use environment-specific API keys
5. Enable HTTPS/SSL certificates

## Useful Commands

```bash
# Install a new package
pip install package-name
pip freeze > requirements.txt  # Update requirements.txt

# Check installed packages
pip list

# Run with multiple workers (production)
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4

# Run in background
nohup uvicorn app.main:app --host 0.0.0.0 --port 8000 &

# Check if server is running
curl http://localhost:8000/
```

## Project Structure Reference

```
rakshakai/
├── app/
│   ├── __init__.py          # Package initialization
│   ├── main.py              # FastAPI app & startup logic
│   ├── config.py            # Configuration management
│   ├── middleware/
│   │   └── auth.py          # API key authentication
│   ├── routes/
│   │   └── honeypot.py      # Honeypot endpoints
│   └── models/
│       └── schemas.py       # Pydantic data models
├── venv/                    # Virtual environment (not in git)
├── .env                     # Environment variables (not in git)
├── .env.example             # Example environment file
├── .gitignore               # Git ignore rules
├── requirements.txt         # Python dependencies
├── README.md                # Project overview
└── SETUP.md                 # This file
```

## Support

If you encounter issues not covered here:
1. Check the FastAPI documentation: https://fastapi.tiangolo.com/
2. Review the error messages in the terminal
3. Ensure all prerequisites are correctly installed
4. Verify your `.env` file is properly configured

---

**Happy Hacking! 🛡️**
