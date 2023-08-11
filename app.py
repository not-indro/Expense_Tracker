import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3

# Initialize SQLite database
conn = sqlite3.connect("finance.db")
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS transactions 
                (id INTEGER PRIMARY KEY, date TEXT, description TEXT, amount REAL)''')
conn.commit()

# Streamlit app
def main():
    st.set_page_config(page_title="Modern Expense Tracker", page_icon="💰")  # Adding page icon
    
    st.title("Modern Expense Tracker")
    
    # Sidebar
    st.sidebar.header("Options")
    selected_option = st.sidebar.radio("Select Option", ["Add Transaction", "View Transactions", "Expense Histogram"])
    
    if selected_option == "Add Transaction":
        add_transaction()
    elif selected_option == "View Transactions":
        view_transactions()
    elif selected_option == "Expense Histogram":
        show_histogram()

# Function to add a transaction
def add_transaction():
    st.header("Add Transaction")
    date = st.text_input("Date", "")
    description = st.text_input("Description", "")
    amount = st.number_input("Amount", 0.0)
    
    if st.button("Add"):
        if date and description and amount:
            cursor.execute("INSERT INTO transactions (date, description, amount) VALUES (?, ?, ?)", (date, description, amount))
            conn.commit()
            st.success("Transaction added successfully.")
        else:
            st.error("Please fill in all fields.")

# Function to view transactions
def view_transactions():
    st.header("View Transactions")
    
    cursor.execute("SELECT * FROM transactions")
    transactions = cursor.fetchall()
    
    if transactions:
        df = pd.DataFrame(transactions, columns=["ID", "Date", "Description", "Amount"])
        st.dataframe(df)
        
        # Delete button for each transaction
        for index, row in df.iterrows():
            if st.button(f"Delete {row['ID']}"):
                cursor.execute("DELETE FROM transactions WHERE id=?", (row['ID'],))
                conn.commit()
                st.success("Transaction deleted successfully.")
        
    else:
        st.warning("No transactions found.")

# Function to show expense histogram
def show_histogram():
    st.header("Expense Histogram")
    
    cursor.execute("SELECT amount FROM transactions")
    amounts = cursor.fetchall()
    
    if amounts:
        amounts = [amount[0] for amount in amounts]
        
        # Modernizing the histogram
        plt.figure(figsize=(10, 6))
        sns.histplot(data=amounts, bins=20, kde=True, color='skyblue')  # Added color and modified 'data' parameter
        plt.xlabel("Amount")
        plt.ylabel("Frequency")
        plt.title("Expense Distribution")
        st.pyplot(plt)
    else:
        st.warning("No transactions found.")

if __name__ == "__main__":
    main()
