import mysql.connector
from contextlib import contextmanager
from logger_setup import logger_setup
import os

logger = logger_setup(os.path.basename(__file__))

@contextmanager
def get_db_connection(my_host="localhost", my_user="root", my_database="expense_manager",my_password="SSRI9977",commit=False):
    # Establish connection to MySQL
    connection = mysql.connector.connect(
        host= my_host,
        user= my_user,
        password=my_password,
        database= my_database,
    )
    if connection.is_connected():
        cursor = connection.cursor(dictionary=True)
        yield cursor

    if commit:
        connection.commit()

    cursor.close()
    connection.close()
    return None
#Whole Data
def fetch_all():
    logger.info('fetch_all called')
    try:
        with get_db_connection() as cursor:
            if cursor is None:
                print("No Cursor Found")
                return

            cursor.execute("SELECT * FROM expenses;")

            # Fetch and print all rows
            expenses = cursor.fetchall()
            for expense in expenses:
                print(expense)

    except mysql.connector.Error as e:
        print("Error:", e)

#Specific Date data
def fetch_expenses_for_date(expense_date):
    logger.info(f'fetch_expenses_for_date called for {expense_date}')
    try :
        with get_db_connection() as cursor:
            if cursor is None:
                print("No Cursor Found")
                return

            cursor.execute("SELECT * FROM expenses WHERE expense_date = %s;" ,(expense_date,))
            # Fetch and print all rows
            expenses = cursor.fetchall()
            return expenses

    except mysql.connector.Error as e:
        print("Error:", e)

#Inserting New Expense
def insert_expenses_for_date(expense_date,amount,category,notes=None):
    logger.info(f'insert_expenses_for_date callled for date: {expense_date}, amount: {amount}, category: {category}')
    try :
        with get_db_connection(commit=True) as cursor:
            if cursor is None:
                print("No Cursor Found")
                return

            cursor.execute("INSERT INTO expenses (expense_date,amount,category,notes) VALUES (%s, %s, %s, %s)",
                           (expense_date,amount,category,notes)
                           )
    except mysql.connector.Error as e:
        print("Error:", e)

#Deleting the Expense for a particular date
def delete_expenses_for_date(expense_date):
    logger.info(f'delete_expenses_for_date callled for date: {expense_date}')
    try :
        with get_db_connection(commit=True) as cursor:
            if cursor is None:
                print("No Cursor Found")
                return

            cursor.execute("DELETE FROM expenses where expense_date = %s",
                           (expense_date,)
                           )

    except mysql.connector.Error as e:
        print("Error:", e)

#fetching summary in a range
def fetch_expense_summary(start_date, end_date):
    logger.info(f'fetch_expense_summary called for start_date: {start_date}, end_date: {end_date}')
    try :
        with get_db_connection() as cursor:
            if cursor is None:
                print("No Cursor Found")
                return

            cursor.execute('''
                                SELECT category, SUM(AMOUNT) as total_expenses
                                FROM expenses WHERE expense_date 
                                BETWEEN %s and %s
                                GROUP BY category;
                                ''',
                           (start_date,end_date)
                           )
            data = cursor.fetchall()
            return data
    except mysql.connector.Error as e:
        print("Error:", e)

#fetching summary for a specific month
def fetch_monthly_expense_summary(month=1, year=2025):
    logger.info(f'fetch_monthly_expense_summary called for month: {month}, year: {year}')
    try:
        with get_db_connection() as cursor:
            if cursor is None:
                print("No Cursor Found")
                return

            cursor.execute(
                '''
                SELECT category, SUM(AMOUNT) as total_expenses
                FROM expenses
                WHERE YEAR(expense_date) = %s AND MONTH(expense_date) = %s
                GROUP BY category;
                ''',
                (year, month) 
            )
            data = cursor.fetchall()
            return data
    except mysql.connector.Error as e:
        print("Error:", e)

#fetching the summary for the year
def fetch_annual_expense_summary(year):
    logger.info(f'fetch_annual_expense_summary called for year: {year}')
    try :
        with get_db_connection() as cursor:
            if cursor is None:
                print("No Cursor Found")
                return

            cursor.execute(
                            '''
                            SELECT category, SUM(AMOUNT) as total_expenses
                            FROM expenses
                            WHERE YEAR(expense_date) = %s
                            GROUP BY category;
                            ''',
                            (year,)
                        )
            data = cursor.fetchall()
            return data
    except mysql.connector.Error as e:
        print("Error:", e)

if __name__ == "__main__":
    expense_summary = fetch_expenses_for_date("2025-02-01")
    for summary in expense_summary:
        print(summary)
