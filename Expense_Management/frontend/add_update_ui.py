import streamlit as st
from datetime import datetime
import requests

API_url = "http://localhost:8000"

def add_update_tab():
    st.header("💰 Expense Tracker")

    # 📅 Date Input
    selected_date = st.date_input("Enter Date:", value=datetime.now().date(), label_visibility="collapsed")

    response = requests.get(f"{API_url}/expenses/{selected_date.isoformat()}")
    if response.status_code == 200:
        response_data = response.json()
        if "message" in response_data:
            response_data = []

        total_expenses = sum([ row['amount'] for row in response_data] ) if response_data else 0

        # 🏷️ Expense Categories
        categories = ["Grocery", "Rent", "Utilities", "Entertainment", "Food", "Shopping", "Travel", "Health"]
        categories.sort()
        categories.append("Other")

        # 🔹 Store row count in session state to prevent auto-reset
        if "required_rows" not in st.session_state:
            st.session_state["required_rows"] = max(len(response_data), 1)

        required_rows = st.number_input("Required Rows", value=st.session_state["required_rows"], min_value=0, step=1,
                                        key="rows")

        # 🛠️ Auto-update UI when row count changes
        if required_rows != st.session_state["required_rows"]:
            st.session_state["required_rows"] = required_rows
            st.rerun()
        with st.form(key="expense_form"):
            col1, col2, col3 = st.columns(3)
            with col1:
                st.text("💵 Amount")
            with col2:
                st.text("📂 Category")
            with col3:
                st.text("📝 Notes")

            expenses = []
            for i in range(required_rows):
                if i < len(response_data):
                    amount = response_data[i]["amount"]
                    category = response_data[i]["category"]
                    notes= response_data[i]['notes']
                else:
                    amount = 0.0
                    category = categories[-1]
                    notes = ""
                if category not in categories:
                    category = categories[-1]
                col1, col2, col3 = st.columns(3)

                with col1:
                    amount_input = st.number_input("Amount", min_value=0.0, step=10.0, value=amount, key=f"amount_{i}", label_visibility="collapsed")

                with col2:
                    category_input = st.selectbox("Category", options=categories, key=f"category_{i}", index = categories.index(category),label_visibility="collapsed")

                with col3:
                    notes_input = st.text_input("Notes", value=notes, key=f"notes_{i}",label_visibility="collapsed")

                expenses.append(
                    {
                        'amount' : amount_input,
                        'category': category_input,
                        'notes': notes_input
                    }
                )
            # ✅ Submit button should be inside the form block
            submit_button = st.form_submit_button(label="💰 Submit Expenses")

        if submit_button:
            filtered_expenses = [expense for expense in expenses if expense['amount'] > 0.0]

            response = requests.post(f"{API_url}/expenses/{selected_date.isoformat()}", json = filtered_expenses)
            if response.status_code == 200:
                st.success("💵Expenses submitted successfully!")  # ✅ Debugging message
            else:
                st.error("❌Failed to update expenses.")

                # 💰 **Total Expenses Display**
        st.markdown(f"""
                    <div style="
                        background-color: rgba(0, 100, 200, 0.2); 
                        padding: 15px; 
                        border-radius: 10px; 
                        color: black; 
                        text-align: center; 
                        font-size: 20px; 
                        margin-top: 20px;">
                        💰 Total Expenses : ₹{total_expenses:.2f}
                    </div>
                    """,
                    unsafe_allow_html=True
                    )

    elif response.status_code == 500:
        st.error("⚠️ Server Error: Please try again later.")
    else:
        st.error(f"❌ Unexpected Error {response.status_code}: {response.text}")