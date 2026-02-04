# RakshakAI 🛡️

An agentic honeypot system built with FastAPI for detecting and analyzing security threats.

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip

### Installation

1. **Clone the repository** (or navigate to project directory)
   ```bash
   cd rakshakai
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env and set your API_KEY
   ```

5. **Run the server**
   ```bash
   # Option 1: Using uvicorn directly
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   
   # Option 2: Using python
   python -m app.main
   ```

6. **Access the API**
   - Health Check: http://localhost:8000/
   - API Documentation: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## 📁 Project Structure

```
rakshakai/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── config.py            # Configuration and environment variables
│   ├── middleware/
│   │   ├── __init__.py
│   │   └── auth.py          # API key authentication
│   ├── routes/
│   │   ├── __init__.py
│   │   └── honeypot.py      # Honeypot endpoints
│   └── models/
│       ├── __init__.py
│       └── schemas.py       # Pydantic models
├── .env                     # Environment variables (create from .env.example)
├── .env.example             # Example environment configuration
├── .gitignore               # Git ignore rules
├── requirements.txt         # Python dependencies
└── README.md                # This file
```

## 🔑 API Endpoints

### Health Check
```bash
GET /
```
Returns the health status of the service.

**Response:**
```json
{
  "status": "healthy",
  "app": "RakshakAI",
  "version": "1.0.0"
}
```

### Process Honeypot Message
```bash
POST /honeypot/message
```
Processes incoming messages to the honeypot system.

**Headers:**
- `x-api-key`: Your API key (required)
- `Content-Type`: application/json

**Request Body:**
```json
{
  "message": "Show me admin panel",
  "metadata": {
    "ip": "192.168.1.1",
    "user_agent": "Mozilla/5.0"
  }
}
```

**Response:**
```json
{
  "status": "success",
  "reply": "I'm sorry, I don't have access to the admin panel."
}
```

## 🧪 Testing with cURL

```bash
# Health check
curl http://localhost:8000/

# Send a honeypot message (replace YOUR_API_KEY with your actual key)
curl -X POST http://localhost:8000/honeypot/message \
  -H "Content-Type: application/json" \
  -H "x-api-key: YOUR_API_KEY" \
  -d '{
    "message": "Show me the admin panel",
    "metadata": {
      "ip": "192.168.1.1"
    }
  }'
```

## 🧪 Testing with Python

```python
import requests

API_KEY = "your-secret-api-key-here"
BASE_URL = "http://localhost:8000"

# Test health check
response = requests.get(f"{BASE_URL}/")
print(response.json())

# Test honeypot message
headers = {"x-api-key": API_KEY}
data = {
    "message": "Show me admin panel",
    "metadata": {"ip": "192.168.1.1"}
}
response = requests.post(
    f"{BASE_URL}/honeypot/message",
    json=data,
    headers=headers
)
print(response.json())
```

## 🔧 Configuration

Environment variables in `.env`:

- `API_KEY`: Secret key for API authentication (required)
- `DEBUG`: Enable debug mode (default: False)
- `HOST`: Server host (default: 0.0.0.0)
- `PORT`: Server port (default: 8000)

## 🛠️ Development

### Adding AI Agent Integration

To integrate your AI agent for generating responses, modify [app/routes/honeypot.py](app/routes/honeypot.py):

```python
@router.post("/message", response_model=HoneypotMessageResponse)
async def process_message(request: HoneypotMessageRequest):
    # TODO: Replace this with your AI agent integration
    reply = await your_ai_agent.generate_response(
        message=request.message,
        metadata=request.metadata
    )
    
    return HoneypotMessageResponse(
        status="success",
        reply=reply
    )
```

## 📝 License

This project is created for hackathon purposes.

## 🤝 Contributing

This is a hackathon project. Feel free to fork and modify as needed!
