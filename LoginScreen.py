
import tkinter as tink
from tkinter import messagebox
import auth
import importlib
import subprocess
import sys
import os

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
usersFile = "DatabaseAccounts.txt"


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

#User storage
#users = {} #need to add preset admin account

#login method
def login():
    username = username_entry.get()
    password = password_entry.get()

    users = load_accounts()

    if username in users and users[username]["password"] == password:
        override_Auth(username, users[username]["is_admin"])
        messagebox.showinfo("Login Success",f"Welcome, {username}!")

        window.destroy()

        subprocess.Popen([sys.executable, "8bitLibrary.py"])

    #will add a call to start main program
    else:
        messagebox.showerror("Login Failed", "Invalid username or password.")

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



def override_Auth(username, is_admin):
    with open("auth.py", "w") as f:
        f.write(f"username ={repr(username)}\n")
        f.write(f"is_admin = {is_admin}\n")



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



