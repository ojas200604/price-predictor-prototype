import pandas as pd
import numpy as np

def generate_mock_data(commodity: str = "Onion", days: int = 365) -> pd.DataFrame:
    dates = pd.date_range(end=pd.Timestamp.today(), periods=days)
    np.random.seed(42)
    
    base_price = 3000
    seasonal = 500 * np.sin(np.linspace(0, 3 * np.pi, days))
    noise = np.random.normal(0, 100, days)
    prices = base_price + seasonal + noise
    arrivals = 10000 - (prices * 1.5) + np.random.normal(0, 300, days)
    
    return pd.DataFrame({
        "date": dates,
        "commodity": commodity,
        "modal_price": np.round(prices, 2),
        "arrivals_qtl": np.round(arrivals, 2)
    })

def build_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.sort_values("date").copy()
    df["price_lag_1"] = df["modal_price"].shift(1)
    df["price_lag_7"] = df["modal_price"].shift(7)
    df["price_lag_14"] = df["modal_price"].shift(14)
    df["rolling_mean_7"] = df["modal_price"].shift(1).rolling(window=7).mean()
    df["rolling_std_7"] = df["modal_price"].shift(1).rolling(window=7).std()
    return df.dropna()