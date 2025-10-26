import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="PhonePe Transaction Insights", layout="wide")

st.title("📊 PhonePe Transaction Insights Dashboard")
st.markdown("Analyze payment trends, user growth, and insurance insights across Indian states.")

@st.cache_data
def load_data():
    trans = pd.read_csv("data/aggregated_transaction.csv")
    user = pd.read_csv("data/aggregated_user.csv")
    ins = pd.read_csv("data/aggregated_insurance.csv")
    return trans, user, ins

trans, user, ins = load_data()

st.sidebar.header("🔍 Filter Data")
year = st.sidebar.selectbox("Select Year", sorted(trans['Year'].unique()))
quarter = st.sidebar.selectbox("Select Quarter", sorted(trans['Quarter'].unique()))

filtered_trans = trans[(trans['Year'] == year) & (trans['Quarter'] == quarter)]

st.subheader(f"📍 Transaction Insights for {year} Q{quarter}")
fig1 = px.bar(
    filtered_trans,
    x="State",
    y="Total_Transaction_Value",
    color="Transaction_Type",
    title="State-wise Transaction Value by Type"
)
st.plotly_chart(fig1, use_container_width=True)

st.subheader("🏆 Top 5 States by Transaction Value")
top_states = filtered_trans.groupby("State")["Total_Transaction_Value"].sum().nlargest(5).reset_index()
fig2 = px.bar(top_states, x="State", y="Total_Transaction_Value", color="Total_Transaction_Value")
st.plotly_chart(fig2, use_container_width=True)

st.subheader("👥 User Registration Trends")
fig3 = px.line(user, x="Quarter", y="Registered_Users", color="State", markers=True, title="User Growth by State")
st.plotly_chart(fig3, use_container_width=True)

st.subheader("🛡️ Insurance Transaction Overview")
fig4 = px.bar(ins, x="State", y="Total_Insurance_Value", color="State", title="Total Insurance Value by State")
st.plotly_chart(fig4, use_container_width=True)

st.success("✅ Dashboard Loaded Successfully!")
