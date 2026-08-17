# 🌾 Price Predictor - Combined UI & Backend

## Overview
This project combines:
- **Frontend**: React-based Price Intelligence Dashboard (from jugraj26/SIH)
- **Backend**: Python Flask API with AI price prediction models
- **Optional**: Streamlit dashboard for quick data visualization

---

## 📂 Project Structure

```
price-predictor-prototype/
├── frontend/                    # React UI (Jugraj's SIH)
│   ├── price_intelligence_dashboard.jsx  # Main React component
│   ├── package.json
│   ├── public/
│   └── src/
│
├── backend/                     # Python Backend API
│   ├── app.py                   # Flask API server
│   ├── streamlit_app.py         # Streamlit dashboard (optional)
│   ├── requirements.txt
│   └── models/                  # ML models (to be added)
│
└── docker-compose.yml           # Docker setup (optional)
```

---

## 🚀 Quick Start

### Prerequisites
- Node.js & npm (for frontend)
- Python 3.8+ (for backend)

### Step 1: Frontend Setup
```bash
cd frontend
npm install
npm start
```
✨ Opens at: **http://localhost:3000**

### Step 2: Backend Setup (in a new terminal)
```bash
cd backend
pip install -r requirements.txt
python app.py
```
🔌 Runs at: **http://localhost:5000**

### Step 3 (Optional): Streamlit Dashboard
```bash
cd backend
streamlit run streamlit_app.py
```
📊 Opens at: **http://localhost:8501**

---

## 🎯 Features

### Frontend (React Dashboard)
- 📊 Price trend visualization
- 🌐 Interactive state-wise risk map
- 📈 Demand vs supply analysis
- 🚚 Transportation cost calculator
- ⚠️ Early warning alerts system
- 💾 Export reports (PDF, Excel)
- 🌙 Dark/Light mode toggle

### Backend API (Flask)
- `POST /api/predict` - Get price predictions
- `GET /api/price-history` - Historical price data
- `GET /api/commodities` - List available commodities
- `GET /api/buffer-stock` - Buffer stock recommendations
- `GET /api/health` - Health check

### Streamlit Dashboard (Optional)
- Real-time price forecasts
- Buffer stock tracking
- Weather impact analysis
- Custom price predictions

---

## 🔌 API Integration

The React UI (frontend) communicates with the Flask backend via REST API:

```javascript
// Example API call from React
fetch('http://localhost:5000/api/predict', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    commodity: 'Wheat',
    current_price: 2400,
    rainfall: 65,
    temperature: 28,
    demand: 550
  })
})
.then(res => res.json())
.then(data => console.log(data))
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| **Frontend** | React 18, Recharts, Lucide Icons, Tailwind CSS |
| **Backend** | Flask, Python, NumPy, Pandas |
| **Optional** | Streamlit for data visualization |
| **ML** | scikit-learn, TensorFlow (to be integrated) |
| **Database** | PostgreSQL (optional, add later) |
| **Deployment** | Docker, Docker Compose |

---

## 📋 Environment Variables

Create a `.env` file in the `backend/` directory:

```env
FLASK_ENV=development
FLASK_DEBUG=True
API_PORT=5000
DATABASE_URL=postgresql://user:password@localhost:5432/price_db
```

---

## 🐳 Docker Deployment (Optional)

```bash
docker-compose up --build
```

This will start:
- React frontend on port 3000
- Flask backend on port 5000
- Streamlit on port 8501

---

## 📊 Next Steps

1. ✅ **UI & API Integration** - Add backend endpoints to React
2. 🤖 **ML Models** - Integrate price prediction models
3. 🗄️ **Database** - Add PostgreSQL for data persistence
4. 📈 **Real Data** - Connect to actual commodity price APIs (e.g., NCDEX)
5. 🔐 **Authentication** - Add user authentication & authorization
6. 📱 **Mobile** - React Native mobile app
7. ☁️ **Cloud Deployment** - Deploy to AWS/GCP/Azure

---

## 🤝 Contributing

Contributions are welcome! Please:
1. Create a feature branch
2. Make your changes
3. Submit a pull request

---

## 📝 License

MIT License - see LICENSE file for details

---

## 💡 Support

For issues or questions, please open an issue on GitHub or contact the development team.

---

**Happy Coding! 🎉**
