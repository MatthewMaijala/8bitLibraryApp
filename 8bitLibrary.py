import mysql.connector
import tkinter as tk
from tkinter import messagebox, ttk
import hashlib
import datetime, os

# Code for the 8bitLibrary application
# Basic GUI test setup
window = tk.Tk()
window.title("8bitLibrary Test")
window.geometry("300x200")
label = tk.Label(window, text="Welcome to 8bitLibrary!")
label.pack(pady=50)

window.mainloop()