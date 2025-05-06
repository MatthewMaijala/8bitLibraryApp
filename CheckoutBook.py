import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from datetime import date, timedelta
import auth

# Database connection
conn = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password="Rbs6^5%9(5%2@8*2@!@",
    database = "library_db"
)
cursor = conn.cursor()

# Simulated logged-in user
USER_ID = auth.user_id  # ← Replace with the actual user ID if needed

book_map = {}  # Maps listbox index to book_id

def checkout_book():
    selection = listbox.curselection()
    if not selection:
        messagebox.showwarning("No selection", "Please select a book to check out.")
        return

    index = selection[0]
    book_id = book_map[index]

    # Check if book is available
    cursor.execute("""
        SELECT status_id FROM book_status
        WHERE book_id = %s
        ORDER BY status_effective_date DESC LIMIT 1
    """, (book_id,))
    result = cursor.fetchone()

    if not result or result[0] != 1:
        messagebox.showinfo("Unavailable", "Book is not available for checkout.")
        return

    today = date.today()

    # Update book status
    cursor.execute("""
        INSERT INTO book_status (status_id, book_id, status_effective_date, status_availability_indicator)
        VALUES (0, %s, %s, FALSE)
    """, (book_id, today))

    # Record transaction
    cursor.execute("""
        INSERT INTO transaction (user_id, transaction_date)
        VALUES (%s, %s)
    """, (USER_ID, today))
    transaction_id = cursor.lastrowid

    # Record transaction detail
    due_date = today + timedelta(days=7)
    cursor.execute("""
        INSERT INTO transaction_detail (transaction_id, transaction_type_code, transaction_detail_due_date, book_id)
        VALUES (%s, %s, %s, %s)
    """, (transaction_id, 'CO', due_date, book_id))

    conn.commit()

    messagebox.showinfo("Success", f"Book checked out successfully!")

# GUI setup
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Check Out a Book")

    tk.Label(root, text=f"User ID: {USER_ID} — Select a Book to Check Out:").pack(pady=5)

    listbox = tk.Listbox(root, width=70, height=20)
    listbox.pack(padx=10, pady=5)

    # Get available books
    cursor.execute("""
        SELECT DISTINCT b.book_id, b.book_title
        FROM book b
        JOIN (
            SELECT book_id, MAX(status_effective_date) as latest_date
            FROM book_status
            GROUP BY book_id
        ) latest ON b.book_id = latest.book_id
        JOIN book_status bs ON bs.book_id = latest.book_id AND bs.status_effective_date = latest.latest_date
        WHERE bs.status_id = 1
    """)
    books = cursor.fetchall()

    for i, (book_id, title) in enumerate(books):
        listbox.insert(tk.END, title)
        book_map[i] = book_id

    tk.Button(root, text="Check Out", command=checkout_book).pack(pady=10)

    root.mainloop()

    cursor.close()
    conn.close()
