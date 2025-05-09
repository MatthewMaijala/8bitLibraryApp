
import tkinter as tink
from tkinter import messagebox
from tkinter import ttk
import auth
import subprocess
import sys
import os
import importlib
import ViewTables
import SearchBooks
import CheckoutBook
import ReturnBook
import MemberView
import mysql.connector
import logging
import ManageBooks

#----------------------------------------- Button test
# #def update_label():
    #text = entry.get()
    #title.config(text=f"Hello, {text}!")
#makes the title/label for the sample button
#title = tink.Label(window, text = "Enter name: ")
#title.pack(pady = 10)

#input widget sample
#entry = tink.Entry(window)
#entry.pack()

#makes the button for greeting
#button = tink.Button(window, text = "greet me", command = update_label)
#button.pack(pady = 10)



#makes the window
logging.basicConfig(
    filename=os.path.join(os.getcwd(), 'user_activity.log'),  # Adjusted to use the correct path
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)

usersFile = "DatabaseAccounts.txt"
usernameGreeter = "Hello"

window = tink.Tk()
window.title("Login Screen")
window.geometry("350x200")

#loads accounts from file
def load_accounts():
    users = {}
    with open(usersFile, "r") as file:
        for line in file:
            parts = line.strip().split(",")
            if len(parts) == 3:
                username, password, is_admin = parts
                users[username] = {"password": password, "is_admin": is_admin}
    return users

#adds new user to file
def save_user(username, password, is_admin=False):
    with open(usersFile, "a") as file:
        file.write(f"{username},{password},{is_admin}\n")

#login method
def login():
    username = username_entry.get()
    password = password_entry.get()

    conn = mysql.connector.connect(
        host = "", # Add your host here
        user = "", # Add your username here
        password="", # Add your password here
        database = "" # Add your database name here
    )
    cursor = conn.cursor()

    cursor.execute("SELECT user_id, is_admin FROM Sign_In_Information WHERE username = %s AND password = %s",
                   (username, password))
    result = cursor.fetchone()

    if result:
        user_id = result[0]  # Extract the user_id from the result
        is_admin = result[1]  # Extract the is_admin value
        override_Auth(user_id, is_admin)  # Store the user_id instead of username
        messagebox.showinfo("Login Success", f"Welcome, {username}!")
        global usernameGreeter
        usernameGreeter = username
        window.destroy()
        HomeScreen()
    else:
        messagebox.showerror("Login Failed", "Invalid username or password.")

    cursor.close()
    conn.close()

#Account creation
def create_user():
    username = username_entry.get()
    password = password_entry.get()

    if not username or not password:
        messagebox.showwarning("Invalid Input", "Username and Password must both have entries")
        return
    users = load_accounts()
    if username in users:
        messagebox.showwarning("Username already in use.", "Please use another username")
    else:
       save_user(username, password, is_admin = False)
       messagebox.showinfo("Account Created", "Account successfully created!")

def override_Auth(user_id, is_admin):
    with open("auth.py", "w") as f:
        f.write(f"user_id = {repr(user_id)}\n")
        f.write(f"is_admin = {is_admin}\n")

    logging.info(f"User Logged In: {user_id} (Admin: {is_admin})")

def closeCommand(current_window):
    with open("auth.py", "w") as f:
        f.write(f"user_id = None\n")
        f.write(f"is_admin = False\n")

    if current_window.winfo_exists():
        current_window.destroy()

def adminCommand():
    #messagebox.showinfo("Admin Option", "Wow you're cool, you have admin privileges!")
    subprocess.Popen([sys.executable, get_script_path("ViewTables.py")])

def MemberView():
    subprocess.Popen([sys.executable, get_script_path("MemberView.py")])

def BookSearch():
    subprocess.Popen([sys.executable, get_script_path("SearchBooks.py")])

def CheckoutBook():
    subprocess.Popen([sys.executable, get_script_path("CheckoutBook.py")])

def ReturnBook():
    subprocess.Popen([sys.executable, get_script_path("ReturnBook.py")])

def greeting():
    init_greeting = f"Welcome, {usernameGreeter}"
    if auth.is_admin:
        init_greeting += " (Admin)"

    tink.Label(window, text=init_greeting, font=("Times New Roman", 14)).pack(pady=20)

def ManageBooks():
    subprocess.Popen([sys.executable, get_script_path("ManageBooks.py")])

def HomeScreen():
    # Frame For buttons example

    window = tink.Tk()
    window.title("8bitLibrary Test")
    window.geometry("500x300")

    importlib.reload(auth)

    init_greeting = f"Welcome to the 8-bit-Library! {usernameGreeter}"
    if auth.is_admin:
        init_greeting += " (Admin)"

    tink.Label(window, text=init_greeting, font=("Times New Roman", 14)).pack(pady=20)

    b_frame = tink.Frame(window)
    b_frame.pack(expand=True)



    # makes buttons
    b1 = tink.Button(b_frame, text='View Library', width=15, height=3, command = MemberView)
    b2 = tink.Button(b_frame, text='Search By Name', width=15, height=3, command = BookSearch)
    b3 = tink.Button(b_frame, text='Checkout Book', width=15, height=3, command = CheckoutBook)
    b4 = tink.Button(b_frame, text='Book Return', width=15, height=3, command = ReturnBook)

    # aligns buttons
    b1.grid(row=0, column=0, padx=10, pady=10)
    b2.grid(row=0, column=1, padx=10, pady=10)
    b3.grid(row=1, column=0, padx=10, pady=10)
    b4.grid(row=1, column=1, padx=10, pady=10)

    # exit button resets auth.py
    exit_button = tink.Button(window, text='Exit', command= lambda: closeCommand(window))
    exit_button.pack(side="left", anchor="sw", padx=10, pady=10)

    # admin button
    if auth.is_admin:
        admin_button = tink.Button(window, text='View All Tables', command=adminCommand)
        admin_button.pack(side="right", anchor='se', padx=10, pady=10)

        book_manage_button = tink.Button(window, text='Manage Books', command=ManageBooks)
        book_manage_button.pack(side="bottom", padx=10, pady=10)

def ViewTable():
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()

    root = tink.Tk()
    root.title("MySQL Tables")

    label = tink.Label(root, text="Tables in Database:")
    label.pack()

    listbox = tink.Listbox(root, width=50, height=20)
    listbox.pack()

    for table in tables:
        listbox.insert(tink.END, table[0])
    root.mainloop()

def get_script_path(script_name):
    """Returns the correct path for bundled or source code files."""
    if hasattr(sys, '_MEIPASS'):
        # If running as a bundled executable
        return os.path.join(sys._MEIPASS, script_name)
    else:
        # If running from source
        return os.path.join(os.getcwd(), script_name)

conn = mysql.connector.connect(
    host = "", # Add your host here
    user = "", # Add your username here
    password="", # Add your password here
    database = "" # Add your database name here
)
cursor = conn.cursor()

#Username entry and label
tink.Label(window, text = "Username:").pack(pady = 5)
username_entry = tink.Entry(window)
username_entry.pack()

#Password entry and label
tink.Label(window, text = "Password:").pack(pady = 5)
password_entry = tink.Entry(window)
password_entry.pack()

#makes the buttons for login and create account
tink.Button(window, text = "Login", command = login).pack(pady = 5)
tink.Button(window, text = "Create Account", command = create_user).pack()

#Starts the GUI
window.mainloop()