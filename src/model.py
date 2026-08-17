import xgboost as xgb
import pandas as pd

def train_and_predict(df: pd.DataFrame, horizon_days: int = 14):
    feature_cols = ["price_lag_1", "price_lag_7", "price_lag_14", "rolling_mean_7", "rolling_std_7", "arrivals_qtl"]
    X = df[feature_cols]
    y = df["modal_price"]
    
    model = xgb.XGBRegressor(n_estimators=100, max_depth=4, learning_rate=0.05, random_state=42)
    model.fit(X, y)
    
    latest_features = X.iloc[[-1]]
    current_price = float(df["modal_price"].iloc[-1])
    predicted_price = float(model.predict(latest_features)[0])
    
    factors = [
        {"factor": col, "importance": round(float(imp), 3)}
        for col, imp in zip(feature_cols, model.feature_importances_)
    ]
    
    return current_price, round(predicted_price, 2), factors