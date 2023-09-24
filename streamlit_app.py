import streamlit as st
import pandas as pd
import psycopg2

# Define the function for Page 1
def page1():
    st.title("Expense Tracker - Page 1")
    st.write("Select your name:")
    selected_username = st.selectbox("Select the Name", ["Abdulreman", "Ahmed", "Khalilurrehman", "Zakera"])
    
    if st.button("Next"):
        # Store selected username in session state
        st.session_state.username = selected_username
        # Navigate to the next page
        st.session_state.page_number = 2  # Set the page number for next page

def page2():
    st.title("Expense Tracker - Page 2")
    selected_username = st.session_state.username
    
    if not selected_username:
        st.error("Invalid access. Please go back and select your name.")
        return
    
    # Retrieve the expense_df from session state
    expense_df = st.session_state.get('expense_df', pd.DataFrame(columns=["Username", "Date", "Category", "Item", "Quantity", "Amount", "Mode of payment"]))

    st.write(f"Your username from Page 1: {selected_username}")

    # Get expense details
    date = st.date_input("Select date of the Expense:")
    spent_on_category = st.selectbox("Spent On Category:", ["Grocery", "Fruits", "Vegetables", "Maintenance", "Fees", "Travelling", "Others"])
    spent_on_item = st.text_input("Spent On Item:")
    qty = st.number_input("Quantity (QTY):", min_value=0)
    amount = st.number_input("Amount (in Rupees):", min_value=0)
    options = st.selectbox("Mode of payment", ["Credit", "Debit Card", "Bank transfer", "Cash"], index=3)

    if st.button("Add Expense"):
    # Create a new row as a dictionary
        new_expense = {
            "Username": [selected_username],
            "Date": [date],
            "Category": [spent_on_category],
            "Item": [spent_on_item],
            "Quantity": [qty],
            "Amount": [amount],
            "Mode of payment": [options]
        }

        # Convert the new expense to a DataFrame and append it to expense_df
        new_expense_df = pd.DataFrame(new_expense)
        expense_df = pd.concat([expense_df, new_expense_df], ignore_index=True)


        # Update the expense_df in session state
        st.session_state.expense_df = expense_df
        st.success("Expense added successfully!")

        # Display a preview of entered expenses
        st.write("Preview of Expenses:")
        st.write(expense_df)

        # Insert the data into PostgreSQL
        insert_into_postgres(expense_df)

# Function to insert DataFrame data into PostgreSQL
def insert_into_postgres(df):
    try:
        conn = psycopg2.connect(
            database="jbwbxpex",
            user="jbwbxpex",
            password="NHnZbQ8GwX8JoKHokHGif1l5nsmBeWDA",
            host="drona.db.elephantsql.com",
            port="5432"
        )
        cursor = conn.cursor()

        for index, row in df.iterrows():
            cursor.execute("INSERT INTO your_table (username, date, category, item, quantity, amount, mode_of_payment) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                           (row['Username'], row['Date'], row['Category'], row['Item'], row['Quantity'], row['Amount'], row['Mode of payment']))

        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        st.error(f"An error occurred while inserting into PostgreSQL: {str(e)}")



# Define the main Streamlit app
def main():
    st.set_page_config(page_title="Expense Tracker", page_icon=":money_with_wings:")
    
    # Check the page number to determine which page to show
    page_number = st.session_state.get('page_number', 1)

    if page_number == 1:
        page1()
    elif page_number == 2:
        page2()
    else:
        st.error("Invalid page number.")

# Call the main function to run the app
if __name__ == "__main__":
    main()
