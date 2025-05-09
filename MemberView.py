import tkinter as tk
from tkinter import ttk
import mysql.connector

# List of views you want to allow
ALLOWED_VIEWS = ["Books", "Genres", "Locations"]

# Connect to MySQL
conn = mysql.connector.connect(
    host = "", # Add your host here
    user = "", # Add your username here
    password="", # Add your password here
    database = "" # Add your database name here
)
cursor = conn.cursor()

# Function to show contents of selected view
def show_view_contents(event):
    selected = listbox.curselection()
    if not selected:
        return
    view_name = listbox.get(selected[0])

    # Get column names
    cursor.execute(f"DESCRIBE {view_name}")
    columns = [col[0] for col in cursor.fetchall()]

    # Get view data
    cursor.execute(f"SELECT * FROM {view_name}")
    rows = cursor.fetchall()

    # Create new window to display the data
    win = tk.Toplevel(root)
    win.title(f"Contents of {view_name}")

    tree = ttk.Treeview(win, columns=columns, show="headings")
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor="w")
    for row in rows:
        tree.insert("", tk.END, values=row)
    tree.pack(expand=True, fill="both")

# Main GUI setup
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Library Data Viewer (Views)")

    label = tk.Label(root, text="Available Views:")
    label.pack()

    listbox = tk.Listbox(root, width=50, height=20)
    listbox.pack()

    # Add allowed views to the listbox
    for view in ALLOWED_VIEWS:
        listbox.insert(tk.END, view)

    listbox.bind("<<ListboxSelect>>", show_view_contents)

    root.mainloop()

    cursor.close()
    conn.close()