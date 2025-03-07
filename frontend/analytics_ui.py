import streamlit as st
from datetime import date, datetime
import requests
import plotly.express as px
import pandas as pd

API_url = "http://localhost:8000"

# Initialize session state key if it doesn't exist
if "color_scheme" not in st.session_state:
    st.session_state["color_scheme"] = "Mint"  # Default value

# Now safely access session state
color_scheme = (
    px.colors.sequential.Mint
    if st.session_state["color_scheme"] == "Mint"
    else px.colors.sequential.Magenta
)
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

    year_selected = st.number_input("Select Year:", min_value=1900, max_value=2100, value=datetime.now().year, step=1, key="year_monthly_analytics")

    #if st.button("📊 Get Monthly Analytics"):
    payload = {"year_value": year_selected}
    response = requests.post(f"{API_url}/analytics/month", json=payload)

    if response.status_code == 200:
        response_data = response.json()
        if "message" in response_data:
            st.warning("⚠️ No expense data available for this year.")
            return

        df = pd.DataFrame([
            {"month": key, "total_expenses": value.get("amount", 0)}
            for key, value in response_data.items()
            ])

        if df.empty:
            st.warning("⚠️ No expenses recorded for this month.")
            return

        fig = px.bar(df, x="month", y="total_expenses",
                     title="💰 Monthly Expense Breakdown",
                     color="month",  # Use an actual column from df
                     text="total_expenses")
        st.plotly_chart(fig)

    elif response.status_code == 500:
        st.error("⚠️ Server Error: Please try again later.")
    else:
        st.error(f"❌ Unexpected Error {response.status_code}: {response.text}")


# 🎨 Annual Expense Analysis with Year Grouping
def annual_analytics_tab():
    st.header("📅 Annual Expense Analytics")

    with st.spinner("Fetching annual analytics... ⏳"):
        response = requests.post(f"{API_url}/analytics/annual", json={})

        if response.status_code == 200:
            response_data = response.json()

            if "data" not in response_data:
                st.error("⚠️ Unexpected API response format for annual analytics.")
                return

            # Convert to DataFrame
            df = pd.DataFrame([
                {"year": int(key), "amount": value["amount"]}
                for key, value in response_data["data"].items()
            ])

            if df.empty:
                st.warning("⚠️ No expenses recorded for this year.")
                return



            # **Step 3: Create Bar Chart**
            fig = px.bar(df, x="year", y="amount",
                         title=f"💰Annual Expense Breakdown",
                         color="year",
                         text="amount")

            # **Step 4: Label Bars with Year Ranges**
            fig.update_xaxes(
                tickmode="array",
                tickvals=df["year"],
                ticktext=[f"{y}" for y in df["year"]]
            )

            st.plotly_chart(fig)

            # Theme switcher
            if st.button("🎨 Change Color Theme"):
                switch_theme()
                st.rerun()

        elif response.status_code == 500:
            st.error("⚠️ Server Error: Please try again later.")
        else:
            st.error(f"❌ Unexpected Error {response.status_code}: {response.text}")
