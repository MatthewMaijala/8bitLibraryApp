
import tkinter as tk
from tkinter import ttk
import mysql.connector

# Connect to MySQL
conn = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password="Rbs6^5%9(5%2@8*2@!@",
    database = "library_db"
)
cursor = conn.cursor()

# Function to show table contents
def show_table_contents(event):
    selected = listbox.curselection()
    if not selected:
        return
    table_name = listbox.get(selected[0])

    # Get column names
    cursor.execute(f"DESCRIBE {table_name}")
    columns = [col[0] for col in cursor.fetchall()]

    # Get table data
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()

    # Create new window
    win = tk.Toplevel(root)
    win.title(f"Contents of {table_name}")

    tree = ttk.Treeview(win, columns=columns, show="headings")
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor="w")
    for row in rows:
        tree.insert("", tk.END, values=row)
    tree.pack(expand=True, fill="both")


if __name__ == "__main__":
    # GUI setup
    root = tk.Tk()
    root.title("MySQL Tables")

    label = tk.Label(root, text="Tables in Database:")
    label.pack()

    listbox = tk.Listbox(root, width=50, height=20)
    listbox.pack()

    # Populate listbox with table names
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    for table in tables:
        listbox.insert(tk.END, table[0])

    # Bind click event
    listbox.bind("<<ListboxSelect>>", show_table_contents)

    root.mainloop()
    # Cleanup
    cursor.close()
    conn.close()