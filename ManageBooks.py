import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

def manage_books():
    # Database connection
    conn = mysql.connector.connect(
        host = "", # Add your host here
        user = "", # Add your username here
        password="", # Add your password here
        database = "" # Add your database name here
    )
    cursor = conn.cursor()

    def refresh_books():
        listbox.delete(0, tk.END)
        cursor.execute("SELECT book_id, book_title FROM book ORDER BY book_id")
        for book_id, title in cursor.fetchall():
            listbox.insert(tk.END, f"{book_id}: {title}")

    def add_book():
        try:
            cursor.execute("""
                INSERT INTO book (location_id, book_title, book_author_last_name,
                                  book_author_first_name, book_publication_year, genre_id)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                int(entry_location.get()),
                entry_title.get(),
                entry_last.get(),
                entry_first.get() or None,
                entry_year.get() or None,
                int(entry_genre.get())
            ))
            conn.commit()
            messagebox.showinfo("Success", "Book added successfully.")
            refresh_books()
        except Exception as e:
            conn.rollback()
            messagebox.showerror("Error", str(e))

    def delete_book():
        selection = listbox.curselection()
        if not selection:
            messagebox.showwarning("No selection", "Select a book to delete.")
            return
        book_text = listbox.get(selection[0])
        book_id = int(book_text.split(":")[0])
        try:
            cursor.execute("DELETE FROM book WHERE book_id = %s", (book_id,))
            conn.commit()
            messagebox.showinfo("Success", "Book deleted.")
            refresh_books()
        except Exception as e:
            conn.rollback()
            messagebox.showerror("Error", str(e))

    # GUI setup
    root = tk.Tk()
    root.title("Add / Delete Books")

    form_frame = tk.Frame(root)
    form_frame.pack(pady=10)

    tk.Label(form_frame, text="Title:").grid(row=0, column=0, sticky="e")
    entry_title = tk.Entry(form_frame, width=30)
    entry_title.grid(row=0, column=1)

    tk.Label(form_frame, text="Author Last:").grid(row=1, column=0, sticky="e")
    entry_last = tk.Entry(form_frame)
    entry_last.grid(row=1, column=1)

    tk.Label(form_frame, text="Author First:").grid(row=2, column=0, sticky="e")
    entry_first = tk.Entry(form_frame)
    entry_first.grid(row=2, column=1)

    tk.Label(form_frame, text="Year:").grid(row=3, column=0, sticky="e")
    entry_year = tk.Entry(form_frame)
    entry_year.grid(row=3, column=1)

    tk.Label(form_frame, text="Location ID:").grid(row=4, column=0, sticky="e")
    entry_location = tk.Entry(form_frame)
    entry_location.grid(row=4, column=1)

    tk.Label(form_frame, text="Genre ID:").grid(row=5, column=0, sticky="e")
    entry_genre = tk.Entry(form_frame)
    entry_genre.grid(row=5, column=1)

    tk.Button(form_frame, text="Add Book", command=add_book).grid(row=6, column=0, pady=10)
    tk.Button(form_frame, text="Delete Selected Book", command=delete_book).grid(row=6, column=1, pady=10)

    listbox = tk.Listbox(root, width=60)
    listbox.pack(padx=10, pady=10)

    refresh_books()
    root.mainloop()

    cursor.close()
    conn.close()

if __name__ == "__main__":
    manage_books()
