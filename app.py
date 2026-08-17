import streamlit as st
import pandas as pd
import numpy as np
from datetime import timedelta

from sklearn.ensemble import RandomForestRegressor

st.set_page_config(page_title="Price Intelligence System", layout="wide")
st.title("🌾 AI-Enabled Predictive Price Intelligence System")

st.sidebar.header("Control Panel")
commodity = st.sidebar.selectbox("Select Commodity", ["Onion", "Potato", "Tur", "Gram", "Masur"], index=0)
horizon = st.sidebar.slider("Forecast Horizon (Days)", 7, 30, 14)
use_sample = st.sidebar.checkbox("Use included sample data (data/prices.csv)", value=True)
upload = st.sidebar.file_uploader("Or upload your CSV (columns: date,commodity,price)", type=["csv"])

@st.cache_data
def load_data(use_sample, upload_file):
    if upload_file is not None:
        try:
            df = pd.read_csv(upload_file)
        except Exception as e:
            st.error(f"Failed to read uploaded file: {e}")
            return None
    else:
        if not use_sample:
            st.info("No data provided. Use the sample dataset or upload a CSV file.")
            return None
        df = pd.read_csv("data/prices.csv")

    # basic validation
    if 'date' not in df.columns or 'commodity' not in df.columns or 'price' not in df.columns:
        st.error("CSV must contain columns: date, commodity, price")
        return None

    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date')
    return df


def prepare_features(series):
    # series: DataFrame with date and price only for chosen commodity
    s = series.copy().set_index('date')
    s = s.asfreq('D')
    s['price'] = s['price'].interpolate()

    df = s.reset_index()
    df['dayofyear'] = df['date'].dt.dayofyear
    df['lag_1'] = df['price'].shift(1)
    df['lag_7'] = df['price'].shift(7)
    df['roll_mean_7'] = df['price'].rolling(7).mean()
    df = df.dropna().reset_index(drop=True)
    return df


def train_forecast(df_commodity, horizon_days=14):
    df_feat = prepare_features(df_commodity[['date','price']])
    if len(df_feat) < 30:
        st.warning("Not enough historical data for a robust model. Need at least ~30 days.")

    X = df_feat[['dayofyear','lag_1','lag_7','roll_mean_7']]
    y = df_feat['price']

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)

    # iterative forecasting
    last_known = df_feat.iloc[-1].copy()
    preds = []
    current_row = last_known.copy()
    for i in range(horizon_days):
        next_date = current_row['date'] + pd.Timedelta(days=1)
        next_dayofyear = int(next_date.timetuple().tm_yday)
        lag_1 = current_row['price'] if i==0 else preds[-1]
        lag_7 = df_feat['price'].iloc[-7 + i] if len(df_feat) > 7 and i < 7 else (preds[-7] if len(preds) >=7 else current_row['lag_7'])
        roll_mean_7 = np.mean(list(df_feat['price'].iloc[-6:]) + preds[-(min(len(preds),6)):]) if len(df_feat) >=6 or len(preds)>0 else current_row['roll_mean_7']

        X_next = np.array([[next_dayofyear, lag_1, lag_7, roll_mean_7]])
        p = model.predict(X_next)[0]
        preds.append(float(p))

        # append to current_row for next iteration
        current_row = current_row.copy()
        current_row['date'] = next_date
        current_row['price'] = p

    start_date = df_feat['date'].iloc[-1] + timedelta(days=1)
    pred_dates = pd.date_range(start=start_date, periods=horizon_days, freq='D')
    pred_df = pd.DataFrame({'date': pred_dates, 'predicted_price': preds})
    return model, pred_df


# ---- Main app flow ----
raw = load_data(use_sample and upload is None, upload)
if raw is None:
    st.stop()

st.subheader("Data preview")
st.write(raw.query("commodity == @commodity").tail(10))

# current avg price
latest = raw.query("commodity == @commodity").sort_values('date').tail(1)
if len(latest):
    last_price = float(latest['price'].iloc[0])
else:
    last_price = None

col1, col2 = st.columns(2)
with col1:
    st.metric(label=f"Current Avg Price ({commodity})", value=f"₹{last_price:.2f} / qtl" if last_price is not None else "N/A")

with col2:
    st.write("Forecast")

# Train and forecast
with st.spinner('Training model and forecasting...'):
    df_comm = raw.query("commodity == @commodity")[['date','price']].copy()
    if len(df_comm) < 7:
        st.error("Not enough data for forecasting. Need at least 7 days of history.")
        st.stop()
    model, predictions = train_forecast(df_comm, horizon_days=horizon)

pred_avg = predictions['predicted_price'].mean()
with col2:
    st.metric(label=f"{horizon}-Day Predicted Avg Price", value=f"₹{pred_avg:.2f} / qtl", delta=f"{(pred_avg-last_price)/last_price*100:+.1f}%" if last_price else "N/A")

st.subheader("Prediction chart")
plot_df = pd.concat([df_comm.set_index('date')['price'], predictions.set_index('date')['predicted_price']], axis=1)
plot_df.columns = ['historical_price','predicted_price']
st.line_chart(plot_df)

st.subheader("Predicted values")
st.write(predictions)

csv = predictions.to_csv(index=False).encode('utf-8')
st.download_button("Download predictions as CSV", data=csv, file_name=f"predictions_{commodity}.csv", mime='text/csv')

st.info("Model: RandomForestRegressor trained on lag features. This is a simple prototype — replace with your production model for better accuracy.")
