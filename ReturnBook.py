import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from datetime import date
import auth
import sys
import os

# DB Connection
conn = mysql.connector.connect(
    host="localhost",
    user="your_username",         # ← Replace with your MySQL username
    password="your_password",     # ← Replace with your MySQL password
    database="your_database"      # ← Replace with your DB name
)
cursor = conn.cursor()

def get_auth_path():
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, 'auth.py')
    else:
        return os.path.join(os.getcwd(), 'auth.py')

def read_auth():
    auth_path = get_auth_path()
    with open(auth_path, 'r') as f:
        lines = f.readlines()
        user_id = lines[0].strip().split('=')[1].strip()
        is_admin = lines[1].strip().split('=')[1].strip()
    return user_id




# Hardcoded user
USER_ID = read_auth()
book_map = {}  # Maps listbox index to (book_id, transaction_id)

def return_book():
    selection = listbox.curselection()
    if not selection:
        messagebox.showwarning("No selection", "Please select a book to return.")
        return

    index = selection[0]
    book_id, _ = book_map[index]  # We don't reuse the checkout's transaction_id
    today = date.today()

    # Update book_status to available (status_id = 1)
    cursor.execute("""
        UPDATE book_status
        SET status_effective_date = %s, status_availability_indicator = TRUE
        WHERE status_id = 1 AND book_id = %s
    """, (today, book_id))

    # Create a new transaction for the return
    cursor.execute("""
        INSERT INTO transaction (user_id, transaction_date)
        VALUES (%s, %s)
    """, (USER_ID, today))
    return_transaction_id = cursor.lastrowid

    # Add 'RT' transaction_detail for the return
    cursor.execute("""
        INSERT INTO transaction_detail (transaction_id, transaction_type_code, transaction_detail_due_date, book_id)
        VALUES (%s, 'RT', %s, %s)
    """, (return_transaction_id, today, book_id))

    conn.commit()

    messagebox.showinfo("Success", "Book returned successfully!")
    root.destroy()

# GUI setup
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Return a Book")

    tk.Label(root, text=f"User ID: {USER_ID} — Select a Book to Return:").pack(pady=5)

    listbox = tk.Listbox(root, width=70, height=20)
    listbox.pack(padx=10, pady=5)

    # Query books currently checked out by user
    cursor.execute("""
        SELECT b.book_id, b.book_title, td.transaction_id
        FROM book b
        JOIN transaction_detail td ON b.book_id = td.book_id
        JOIN transaction t ON td.transaction_id = t.transaction_id
        WHERE t.user_id = %s
          AND td.transaction_type_code = 'CO'
          AND NOT EXISTS (
              SELECT 1 FROM transaction_detail td2
              WHERE td2.book_id = b.book_id
                AND td2.transaction_type_code = 'RT'
                AND td2.transaction_id > td.transaction_id
          )
    """, (USER_ID,))
    books = cursor.fetchall()

    for i, (book_id, title, transaction_id) in enumerate(books):
        listbox.insert(tk.END, title)
        book_map[i] = (book_id, transaction_id)

    tk.Button(root, text="Return", command=return_book).pack(pady=10)

    root.mainloop()

    cursor.close()
    conn.close()
