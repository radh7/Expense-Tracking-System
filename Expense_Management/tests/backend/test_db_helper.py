from backend import db_helper

#fetch data
def test_fetch_expenses_for_date():
    expenses = db_helper.fetch_expenses_for_date("2024-08-15")

    assert len(expenses) == 1
    assert expenses[0]['amount'] == 10.0
    assert expenses[0]['category'] == "Shopping"
    assert expenses[0]['notes'] == "Bought potatoes"

#invalid date
def test_fetch_expenses_for_invalid_date():
    expenses = db_helper.fetch_expenses_for_date("9999-08-15")

    assert len(expenses) == 0

#summary
def test_fetch_expense_summary_invlaid_data_range():
    summary = db_helper.fetch_expense_summary("2099-01-2025", "2099-12-2025")
    assert len(summary) == 0

#insert_date
def test_insert_expenses_for_date():
    db_helper.delete_expenses_for_date("2025-03-01")
    db_helper.insert_expenses_for_date("2025-03-01","45","food", "Tea")
    expense = db_helper.fetch_expenses_for_date("2025-03-01")

    assert len(expense) == 1
    assert str(expense[0]['expense_date']) == "2025-03-01"
    assert expense[0]['amount'] == 45

#delete date
def test_delete_expenses_for_date():
    db_helper.insert_expenses_for_date("2099-03-01", "45", "food", "Tea")
    db_helper.delete_expenses_for_date("2099-03-01")
    expense = db_helper.fetch_expenses_for_date("2099-03-01")
    assert len(expense) == 0

#monthly summary
def test_fetch_monthly_expense_summary_for_invlid_month():
    summary = db_helper.fetch_monthly_expense_summary("13")
    assert len(summary) == 0

#annualsummary
def test_fetch_annual_expense_summary_for_invlid_year():
    summary = db_helper.fetch_annual_expense_summary("0000")
    assert len(summary) == 0
