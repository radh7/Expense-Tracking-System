from fastapi import FastAPI, HTTPException
from datetime import date
from typing import List
import db_helper
from pydantic import BaseModel, Field
import os
from logger_setup import logger_setup

# 🎯 Initialize FastAPI
app = FastAPI()

# 🔹 Setup Logging
logger = logger_setup(os.path.basename(__file__))

# 🎯 Pydantic Models
class Expense(BaseModel):
    amount: float
    category: str
    notes: str

class DateRange(BaseModel):
    start_date: date
    end_date: date

class YearRequest(BaseModel):
    year_value: int = Field(..., ge=1000, le=9999, description="Valid year (1000-9999)")

# 🎯 Response Model
class ExpenseResponse(BaseModel):
    message: str

# 📌 **Handle Expense Fetching**
@app.get("/expenses/{expense_date}")
def get_expenses(expense_date: date):
    try:
        logger.info(f"Fetching expenses for date: {expense_date}")
        response = db_helper.fetch_expenses_for_date(expense_date)

        if not response:
            logger.warning(f"No expenses found for {expense_date}")
            return {"message": "No expenses available for the date"}
        
        logger.info(f"Returning {len(response)} expenses for {expense_date}")
        return response
    except Exception as e:
        logger.error(f"Error fetching expenses: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Server Error: {str(e)}")

# 📌 **Handle Expense Addition**
@app.post("/expenses/{expense_date}", response_model=ExpenseResponse)
def add_or_update_expenses(expense_date: date, expenses: List[Expense]):
    try:
        logger.info(f"Adding expenses for {expense_date}: {expenses}")
        
        # Remove existing expenses for the date
        db_helper.delete_expenses_for_date(expense_date)

        # Insert new expenses
        for expense in expenses:
            db_helper.insert_expenses_for_date(expense_date, expense.amount, expense.category, expense.notes)

        logger.info(f"Successfully added {len(expenses)} expenses for {expense_date}")
        return {"message": "Expenses added successfully"}
    except Exception as e:
        logger.error(f"Error adding expenses: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Server Error: {str(e)}")

# 📌 **Handle Date Range Analytics**
@app.post("/analytics")
def get_analytics(date_range: DateRange):
    try:
        logger.info(f"Fetching analytics for range: {date_range.start_date} to {date_range.end_date}")
        data = db_helper.fetch_expense_summary(date_range.start_date, date_range.end_date)

        if not data:
            logger.warning("No data available for the given period")
            return {"message": "No data available for this period."}

        logger.info(f"Returning {len(data)} records for date range analytics")
            
        return { row['category']:
                     {"total_expenses": row["total_expenses"]}
                for row in data
            }
    except Exception as e:
        logger.error(f"Error fetching date range analytics: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Server Error: {str(e)}")

# 📊 **Handle Monthly Analytics**
@app.post("/analytics/month")
def get_analytics_for_month(year: YearRequest):
    try:
        logger.info(f"Fetching monthly analytics for {year.year_value}")
        expense_summary = db_helper.fetch_monthly_expense_summary(year.year_value)

        if not expense_summary:
            logger.warning(f"No data found for {year.year_value}")
            return {"message": "No expense data available for this year."}

        total = sum(row['total_amount'] for row in expense_summary) or 1  # Avoid division by zero

        logger.info(f"Returning {len(expense_summary)} records for monthly analytics")
        return {
            row['month']: {
                "amount": row['total_amount'],
                "percentage": (row['total_amount'] / total * 100)
            }
            for row in expense_summary
        }
    except Exception as e:
        logger.error(f"Error fetching monthly analytics: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Server Error: {str(e)}")

# 📆 **Handle Annual Analytics**
@app.post("/analytics/annual")
def get_annual_analytics():
    try:
        logger.info(f"Fetching annual analytics")
        expense_summary = db_helper.fetch_annual_expense_summary()

        if not expense_summary:
            logger.warning(f"No data found")
            return {"message": "No expense data available for this year."}

        total = sum(row['total_amount'] for row in expense_summary) or 1  # Avoid division by zero

        analytics_data = {
            row['year']: {
                "amount": row['total_amount'],
                "percentage": (row['total_amount'] / total * 100)
            }
            for row in expense_summary
        }

        # ✅ Fix: Always include a message and structured data
        return {
            "message": "Annual analytics data fetched successfully",
            "data": analytics_data
        }

    except Exception as e:
        logger.error(f"Error fetching annual analytics: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Server Error: {str(e)}")
