import mysql.connector
import tkinter as tk
import auth
from tkinter import messagebox, ttk
import hashlib
import datetime, os

# opens new window
window = tk.Tk()
window.title("8bitLibrary Test")
window.geometry("500x300")

#closes the window and resets auth.py
def closeCommand():
    with open("auth.py", "w") as f:
        f.write(f"username = None\n")
        f.write(f"is_admin = False\n")

    window.destroy()

#placeholder admin command
def adminCommand():
    messagebox.showinfo("Admin Option", "Wow you're cool, you have admin privileges!")


#greeting
greeting = f"Welcome, {auth.username}"
if auth.is_admin:
    greeting += " (Admin)"

tk.Label(window, text=greeting, font=("Times New Roman", 14)).pack(pady=20)

#Frame For buttons example
b_frame = tk.Frame(window)
b_frame.pack(expand=True)

#makes buttons
b1 = tk.Button(b_frame, text = 'Button 1', width = 15, height = 3)
b2 = tk.Button(b_frame, text = 'Button 2', width = 15, height = 3)
b3 = tk.Button(b_frame, text = 'Button 3', width = 15, height = 3)
b4 = tk.Button(b_frame, text = 'Button 4', width = 15, height = 3)

#aligns buttons
b1.grid(row = 0, column = 0, padx = 10, pady = 10)
b2.grid(row = 0, column = 1, padx = 10, pady = 10)
b3.grid(row = 1, column = 0, padx = 10, pady = 10)
b4.grid(row = 1, column = 1, padx = 10, pady = 10)

#exit button
exit_button = tk.Button(window, text = 'Exit', command = closeCommand)
exit_button.pack(side ="left", anchor = "sw", padx=10, pady=10)

#admin button
if auth.is_admin:
    admin_button = tk.Button(window, text = 'Super Secret Admin Button', command = adminCommand)
    admin_button.pack(side ="right", anchor = 'se', padx = 10, pady=10)

window.mainloop()