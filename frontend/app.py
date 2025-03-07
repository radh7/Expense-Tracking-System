import streamlit as st
from datetime import date
import requests
from add_update_ui import add_update_tab
from analytics_ui import analytics_tab, monthly_analytics_tab, annual_analytics_tab

API_url = "http://localhost:8000"

# Custom Styling
st.markdown(
    """
    <style>
    /* Full Page Pink Background */
    body {
        background: ##FADADD;
        color: white;
    }

   </style>
   """,
    unsafe_allow_html=True,
)

st.title('💰 Expense Tracking System')

# 🔹 Main Tabs with Different Styles
tab1, tab2 = st.tabs(["💰 Add/Update Expense", "📊 Analytics"])

# ➕ Add/Update Expense Tab
with tab1:

    add_update_tab()

# 📊 Analytics Tab with Subtabs
with tab2:
    
    # ✅ Horizontal Subtabs with Unique Styles
    subtab1, subtab2, subtab3 = st.tabs(["📅 Custom Date Analysis ", "📆 Monthly", "📊 Annual"])
    
    with subtab1:
        analytics_tab()
    
    with subtab2:
        monthly_analytics_tab()
    
    with subtab3:
        annual_analytics_tab()
