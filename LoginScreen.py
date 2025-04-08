
import tkinter as tink
from tkinter import messagebox

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
window = tink.Tk()
window.title("Login Screen")
window.geometry("350x200")

#User storage
users = {} #need to add preset admin account

#login method
def login():
    username = username_entry.get()
    password = password_entry.get()

    if username in users and users[username] == password:
        messagebox.showinfo("Login Success",f"Welcome, {username}!")
        #will add a call to start main program
    else:
        messagebox.showerror("Login Failed", "Invalid username or password.")

#Account creation
def create_user():
    username = username_entry.get()
    password = password_entry.get()

    if username in users:
        messagebox.showwarning("Username already in use.", "Please use another username")
    elif not username or not password:
        messagebox.showwarning("Invalid Input", "Username and Password must both have entries")
    else:
        users[username] = password
        messagebox.showinfo("Account Created", "Account successfully created!")

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



