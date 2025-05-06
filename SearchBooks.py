import tkinter as tk
from tkinter import ttk
import mysql.connector

# Database connection
conn = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password="Rbs6^5%9(5%2@8*2@!@",
    database = "library_db"
)
cursor = conn.cursor()

# Function to perform search across all columns
def search_books():
    search_term = entry.get()
    if not search_term:
        return

    # Clear previous results
    for row in tree.get_children():
        tree.delete(row)

    # Build SQL query: search across all relevant columns
    query = """
    SELECT * FROM book
    WHERE
        CAST(book_id AS CHAR) LIKE %s OR
        CAST(location_id AS CHAR) LIKE %s OR
        book_title LIKE %s OR
        book_author_last_name LIKE %s OR
        book_author_first_name LIKE %s OR
        CAST(book_publication_year AS CHAR) LIKE %s OR
        CAST(genre_id AS CHAR) LIKE %s
    """
    like_term = f"%{search_term}%"
    values = [like_term] * 7
    cursor.execute(query, values)
    results = cursor.fetchall()

    for row in results:
        tree.insert("", tk.END, values=row)
# GUI setup
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Search All Book Fields")
    # Search field
    tk.Label(root, text="Search in All Book Columns:").pack(pady=5)
    entry = tk.Entry(root, width=50)
    entry.pack(pady=5)
    # Search button
    search_button = tk.Button(root, text="Search", command=search_books)
    search_button.pack(pady=5)
    # Treeview for results
    # Get column names
    cursor.execute("DESCRIBE book")
    columns = [col[0] for col in cursor.fetchall()]
    tree = ttk.Treeview(root, columns=columns, show="headings", height=15)
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor="w")
    tree.pack(padx=10, pady=10, fill="both", expand=True)
    root.mainloop()
    cursor.close()
    conn.close()