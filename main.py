from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.data_loader import generate_mock_data, build_features
from src.model import train_and_predict
from src.logic import evaluate_decision_support

app = FastAPI(title="AI Price Intelligence Backend")

class ForecastRequest(BaseModel):
    commodity: str = "Onion"
    horizon_days: int = 14

@app.get("/")
def health_check():
    return {"status": "online", "system": "AI Price Intelligence Backend"}

@app.post("/api/v1/forecast")
def get_commodity_forecast(request: ForecastRequest):
    try:
        raw_df = generate_mock_data(commodity=request.commodity)
        processed_df = build_features(raw_df)
        curr_price, pred_price, factors = train_and_predict(processed_df, request.horizon_days)
        pct_change, risk_level, action = evaluate_decision_support(curr_price, pred_price)
        
        return {
            "status": "success",
            "commodity": request.commodity,
            "horizon_days": request.horizon_days,
            "metrics": {
                "current_price_per_qtl": curr_price,
                "predicted_price_per_qtl": pred_price,
                "price_change_pct": pct_change,
                "risk_level": risk_level
            },
            "influencing_factors": factors,
            "decision_support": action
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))