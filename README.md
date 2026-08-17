# Price Predictor - Combined Frontend & Backend

## Project Structure

```
.
├── frontend/              # React/JavaScript UI (from SIH)
│   └── price-dashboard-organized/
├── backend/               # Python backend
└── docker-compose.yml     # (optional) For containerized deployment
```

## Setup Instructions

### Frontend
1. Navigate to `frontend/`
2. Install dependencies: `npm install`
3. Start dev server: `npm start`

### Backend
1. Navigate to `backend/`
2. Install dependencies: `pip install -r requirements.txt`
3. Run server: `python app.py` or `flask run`

## Integration
The frontend communicates with the backend via REST API at `http://localhost:5000` (or your configured backend URL).
