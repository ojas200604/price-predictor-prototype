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
    # load either uploaded CSV or the included sample
    if upload_file is not None:
        try:
            # Try a robust CSV load and basic automatic fix for rows with too many columns
            raw_text = upload_file.read().decode('utf-8')
            lines = [ln for ln in raw_text.splitlines() if ln.strip()]
            cleaned_lines = []
            for ln in lines:
                parts = ln.split(',')
                # keep only first three columns if extra commas accidentally merged rows
                if len(parts) > 3:
                    cleaned_lines.append(','.join(parts[:3]))
                else:
                    cleaned_lines.append(ln)
            from io import StringIO
            df = pd.read_csv(StringIO('\n'.join(cleaned_lines)))
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

    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df = df.dropna(subset=['date'])
    df = df.sort_values('date')
    # ensure price numeric
    df['price'] = pd.to_numeric(df['price'], errors='coerce')
    df = df.dropna(subset=['price'])
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
    if len(df_feat) < 10:
        st.warning("Not enough historical data for a robust model. Need at least ~10 days for sensible lag features.")

    X = df_feat[['dayofyear','lag_1','lag_7','roll_mean_7']]
    y = df_feat['price']

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)

    # iterative forecasting using a simple history buffer
    history = list(df_feat['price'].values)
    last_date = df_feat['date'].iloc[-1]
    preds = []

    for i in range(horizon_days):
        next_date = last_date + timedelta(days=i+1)
        next_dayofyear = int(next_date.timetuple().tm_yday)

        lag_1 = history[-1]
        lag_7 = history[-7] if len(history) >= 7 else history[-1]
        roll_mean_7 = np.mean(history[-7:]) if len(history) >= 1 else history[-1]

        X_next = np.array([[next_dayofyear, lag_1, lag_7, roll_mean_7]])
        p = model.predict(X_next)[0]
        preds.append(float(p))
        history.append(p)

    start_date = df_feat['date'].iloc[-1] + timedelta(days=1)
    pred_dates = pd.date_range(start=start_date, periods=horizon_days, freq='D')
    pred_df = pd.DataFrame({'date': pred_dates, 'predicted_price': preds})
    return model, pred_df


# ---- Main app flow ----
raw = load_data(use_sample and upload is None, upload)
if raw is None:
    st.stop()

# Data preview and filters
st.subheader("Data preview")
st.write(raw.head())

# Filter by commodity
df_comm_full = raw.query("commodity == @commodity").sort_values('date')
if df_comm_full.empty:
    st.error(f"No data for commodity: {commodity}. Please upload or enable sample data.")
    st.stop()

# Add a date range selector (timeline) so users can select the training window
min_date = df_comm_full['date'].min().date()
max_date = df_comm_full['date'].max().date()

date_range = st.sidebar.date_input("Select historical date range (timeline)", value=(min_date, max_date), min_value=min_date, max_value=max_date)

# Ensure valid range
if isinstance(date_range, tuple) and len(date_range) == 2:
    start_sel, end_sel = date_range
else:
    start_sel, end_sel = min_date, max_date

# Subset historical data based on chosen timeline
df_comm = df_comm_full[(df_comm_full['date'].dt.date >= start_sel) & (df_comm_full['date'].dt.date <= end_sel)].copy()

if df_comm.empty:
    st.error("No data in the selected date range. Choose a wider range.")
    st.stop()

st.write(df_comm.tail(10))

# current avg price (from selected dataset)
latest = df_comm.sort_values('date').tail(1)
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
    if len(df_comm) < 7:
        st.error("Not enough data for forecasting. Need at least 7 days of history.")
        st.stop()

    model, predictions = train_forecast(df_comm[['date','price']].copy(), horizon_days=horizon)

pred_avg = predictions['predicted_price'].mean()
with col2:
    st.metric(label=f"{horizon}-Day Predicted Avg Price", value=f"₹{pred_avg:.2f} / qtl", delta=(f"{(pred_avg-last_price)/last_price*100:+.1f}%" if last_price else "N/A"))

st.subheader("Prediction chart")
plot_hist = df_comm.set_index('date')['price']
plot_pred = predictions.set_index('date')['predicted_price']
plot_df = pd.concat([plot_hist, plot_pred], axis=1)
plot_df.columns = ['historical_price','predicted_price']
st.line_chart(plot_df)

st.subheader("Predicted values")
st.write(predictions)

csv = predictions.to_csv(index=False).encode('utf-8')
st.download_button("Download predictions as CSV", data=csv, file_name=f"predictions_{commodity}.csv", mime='text/csv')

st.info("Model: RandomForestRegressor trained on lag features. This is a simple prototype — replace with your production model for better accuracy.")
