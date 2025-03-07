import streamlit as st
from datetime import date, datetime
import requests
import plotly.express as px
import pandas as pd

API_url = "http://localhost:8000"

# 🎨 Ensure Theme is Initialized in Session State
if "color_scheme" not in st.session_state:
    st.session_state["color_scheme"] = "Pink"  # Default theme

# Function to switch theme
def switch_theme():
    st.session_state["color_scheme"] = "Mint" if st.session_state["color_scheme"] == "Pink" else "Pink"

# 📌 Date Range Analytics with Line Chart
def analytics_tab():
    st.header("📊 Date Range Expense Analytics")

    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date:", value=date.today())
    with col2:
        end_date = st.date_input("End Date:", value=date.today())

    if st.button("📈 Get Date Range Analytics"):
        if end_date < start_date:
            st.error("❌ End Date must be greater than Start Date.")
            return

        payload = {
            "start_date": start_date.strftime("%Y-%m-%d"),
            "end_date": end_date.strftime("%Y-%m-%d"),
        }
        response = requests.post(f"{API_url}/analytics/", json=payload)

        if response.status_code == 200:
            response_data = response.json()
            if "message" in response_data:
                st.warning("⚠️ No data available for this period.")
                return

            df = pd.DataFrame([
                {"category": key, "total_expenses": value["total_expenses"]}
                for key, value in response_data.items()
            ])

            if df.empty:
                st.warning("⚠️ No expenses recorded for this period.")
                return

            fig = px.bar(df, x="category", y="total_expenses",
                         title="📅 Expense Trend Over Time",
                         color="category",
                         text='total_expenses'
                         )

            st.plotly_chart(fig)

        elif response.status_code == 500:
            st.error("⚠️ Server Error: Please try again later.")
        else:
            st.error(f"❌ Unexpected Error {response.status_code}: {response.text}")

# 📊 Monthly Expense Analysis with Bar Chart
def monthly_analytics_tab():
    st.header("📆 Monthly Expense Analytics")

    month, year = st.columns(2)
    with month:
        month_selected = st.selectbox("Select Month:", list(range(1, 13)), index=(datetime.now().month - 1), key="montht_monthly_analytics")

    with year:
        year_selected = st.number_input("Select Year:", min_value=1900, max_value=2100, value=datetime.now().year, step=1, key="year_monthly_analytics")

    #if st.button("📊 Get Monthly Analytics"):
    payload = {"month_value": month_selected, "year_value": year_selected}
    response = requests.post(f"{API_url}/analytics/month", json=payload)

    if response.status_code == 200:
        response_data = response.json()
        if "message" in response_data:
            st.warning("⚠️ No expense data available for this month.")
            return

        df = pd.DataFrame([
            {"category": key, "total_expenses": value.get("total", 0)}
            for key, value in response_data.items()
            ])

        if df.empty:
            st.warning("⚠️ No expenses recorded for this month.")
            return

        fig = px.bar(df, x="category", y="total_expenses",
                         title="💰 Monthly Expense Breakdown",
                         color="category",
                         text="total_expenses")
        st.plotly_chart(fig)

    elif response.status_code == 500:
        st.error("⚠️ Server Error: Please try again later.")
    else:
        st.error(f"❌ Unexpected Error {response.status_code}: {response.text}")


# 🎨 Annual Expense Analysis with Theme Switching
def annual_analytics_tab():
    st.header("📅 Annual Expense Analytics")

    year_selected = st.slider("Select Year:", min_value=1900, max_value=2100, value=datetime.now().year, key="year_annual_analytics")

    color_scheme = px.colors.sequential.Mint if st.session_state["color_scheme"] == "Mint" else px.colors.sequential.Magenta

    # Initialize theme_choice with the current session theme
    theme_choice = st.session_state["color_scheme"]
    with st.spinner("Fetching annual analytics... ⏳"):
        response = requests.post(f"{API_url}/analytics/annual", json={"year_value": year_selected})

        if response.status_code == 200:
            response_data = response.json()

            if "message" in response_data and "data" in response_data:  # ✅ Ensure correct structure
                analytics_data = response_data["data"]
            else:
                st.error("⚠️ Unexpected API response format for annual analytics.")
                st.stop()

            # Extract the "data" part
            data = response_data.get("data", {})

            # Convert to DataFrame
            df = pd.DataFrame([
                {"category": key, "total": value["total"], "percentage": value["percentage"]}
                for key, value in data.items()
            ])
            if df.empty:
                st.warning("⚠️ No expenses recorded for this year.")
                return

            fig = px.pie(df, names="category", values="total", title="💰 Expense Distribution",
                         hole=0.2, color_discrete_sequence=color_scheme)

            st.plotly_chart(fig)

            if st.button("🎨 Change Color Theme"):
                switch_theme()
                st.rerun()

        elif response.status_code == 500:
            st.error("⚠️ Server Error: Please try again later.")

        else:
            st.error(f"❌ Unexpected Error {response.status_code}: {response.text}")
