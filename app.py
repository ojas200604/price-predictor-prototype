import streamlit as st

st.set_page_config(page_title="Price Intelligence System", layout="wide")
st.title("🌾 AI-Enabled Predictive Price Intelligence System")

st.sidebar.header("Control Panel")
commodity = st.sidebar.selectbox("Select Commodity", ["Onion", "Potato", "Tur", "Gram", "Masur"])
horizon = st.sidebar.slider("Forecast Horizon (Days)", 7, 30, 14)

col1, col2 = st.columns(2)
with col1:
    st.metric(label=f"Current Avg Price ({commodity})", value="₹3,450 / qtl", delta="-2.1%")
with col2:
    st.metric(label=f"{horizon}-Day Predicted Price", value="₹3,820 / qtl", delta="+10.7% (Warning)")

st.info("System initialized successfully.")
