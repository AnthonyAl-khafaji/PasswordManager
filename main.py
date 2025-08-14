import tkinter as tk
from tkinter import messagebox
import random
import string
import json
from unittest import result
from wsgiref import headers
from cryptography.fernet import Fernet
import os
import Login
#import time was for testing purpose
import sqlLiteDB 
import PassGen

userID = None
# --- Login Setup ---
loginScreen = Login.LoginScreen()  # Initialize the login screen
loginScreen.root.mainloop()  # Run the login screen

#flag to exit while statement
run = False 
while not run:
  run = loginScreen.getAuthenticated()# Initialize the login screen
  userID = loginScreen.getUser() #userID to pass along for sql calls
  #time.sleep(5) used for testing, making sure the loop isn't going crazy in  the background
# proceed with the password manager
#print (userID)
#database setup
db = sqlLiteDB.userDB()
#db.DropTable("sites")
db.siteTable()
db.getallSites(userID)

# Encryption Setup
KEY_FILE = "key.key"
DATA_FOLDER = "data"
PASSWORD_FILE = os.path.join(DATA_FOLDER, "passwords.enc")

def generate_key():
    """Generate and save a new encryption key."""
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as key_file:
            key_file.write(key)


def load_key():
    """Load the saved encryption key."""
    return open(KEY_FILE, "rb").read()


# Ensure key and data folder exist
generate_key()
key = load_key()
cipher = Fernet(key)
os.makedirs(DATA_FOLDER, exist_ok=True)


# GUI Setup 
root = tk.Tk()
root.title("Pass Keeper")
root.geometry("500x400")
root.configure(bg="#1f2c34")  # Dark background

itemsToCopy = {"user": "", "passWord": ""}

# Title
title_label = tk.Label(root, text="Pass Keeper", font=("Arial", 20, "bold"), fg="white", bg="#1f2c34", pady=10)
title_label.pack()

# Frame
frame = tk.Frame(root, bg="white", padx=20, pady=0, bd=0, relief="flat")
frame.place(relx=0.5, rely=0.5, anchor="center")

# Labels
label_font = ("Segoe UI", 11, "bold")
tk.Label(frame, text="Website:", font=label_font, bg="white").grid(row=0, column=0, sticky="w", pady=8)
tk.Label(frame, text="Username/Email:", font=label_font, bg="white").grid(row=1, column=0, sticky="w", pady=8)
tk.Label(frame, text="Password:", font=label_font, bg="white").grid(row=2, column=0, sticky="w", pady=8)

# Entry fields
entry_font = ("Segoe UI", 11)
website_entry = tk.Entry(frame, width=30, font=entry_font, bd=1, relief="flat", highlightbackground="dodgerblue", highlightthickness=1)
website_entry.grid(row=0, column=1, pady=8)

username_entry = tk.Entry(frame, width=30, font=entry_font, bd=1, relief="flat", highlightbackground="dodgerblue", highlightthickness=1)
username_entry.grid(row=1, column=1, pady=8)

password_entry = tk.Entry(frame, width=30, font=entry_font, bd=1, relief="flat", highlightbackground="dodgerblue", highlightthickness=1)
password_entry.grid(row=2, column=1, pady=8)

#Default Values
lenPassword = tk.IntVar(value=16)
sectionNum = tk.IntVar(value=3)
excludeChar = tk.StringVar(value="")

controls = tk.Frame(frame, bg="white")
controls.grid(row=3, column=0, rowspan=3, sticky="nw", padx=(0, 10))

lenLabel = tk.Label(controls, text="Length:",  font=label_font, bg="white").grid(row=0, column=0, sticky="w", pady=4)
lenLabel = tk.Entry(controls, width=8, font=entry_font, textvariable=lenPassword,bd=1, relief="flat", highlightbackground="dodgerblue", highlightthickness=1)
lenLabel.grid(row=0, column=1, sticky="w", pady=4, padx=(6,0))

sectionLabel = tk.Label(controls, text="Sections:", font=label_font, bg="white").grid(row=1, column=0, sticky="w", pady=4)
sectionLabel = tk.Entry(controls, width=8, font=entry_font, textvariable=sectionNum, bd=1, relief="flat", highlightbackground="dodgerblue", highlightthickness=1)
sectionLabel.grid(row=1, column=1, sticky="w", pady=4, padx=(6,0))

excludeWordLabel = tk.Label(controls, text="Exclude:", font=label_font, bg="white").grid(row=2, column=0, sticky="w", pady=4)
excludeWordLabel = tk.Entry(controls, width=12, font=entry_font, textvariable=excludeChar, bd=1, relief="flat", highlightbackground="dodgerblue", highlightthickness=1)
excludeWordLabel.grid(row=2, column=1, sticky="w", pady=4, padx=(6,0))

showAllSitesButt = tk.Button(controls, text="Show all sites", bg="slateblue", activebackground="orange",command=lambda: showAllSites(userID))
showAllSitesButt.grid(row=3, column=1, pady=4, padx=(10,0))

# Functions
def generate_password():
    #chars = string.ascii_letters + string.digits + string.punctuation
    #password = ''.join(random.choice(chars) for _ in range(14))
    pw = PassGen.GenPassWord(int(sectionNum.get()), excludeChar.get())
    password = pw.makePassword(int(lenPassword.get()))
    password_entry.delete(0, tk.END)
    password_entry.insert(0, password)

def copyToClipboard(info: str):
    if info == "":
        messagebox.showerror("Copy Error", "Nothing to copy")
        return
    else:
        root.clipboard_clear()
        root.clipboard_append(info)
        root.update()

def copyPassword(event=None):
    text = password_entry.get().strip() or itemsToCopy["passWord"]
    copyToClipboard(text)

def copyUserName(event=None):
    text = password_entry.get().strip() or itemsToCopy["user"]
    copyToClipboard(text)

def save_password():
    website = website_entry.get()
    username = username_entry.get()
    password = password_entry.get()

    if website and username and password:
        data = f"{website} | {username} | {password}\n"
        encrypted_data = cipher.encrypt(data.encode())

        
        #with open(PASSWORD_FILE, "ab") as file:
        #    file.write(encrypted_data + b"\n")
        savedname = db.retrieveInfoFull(website, userID, username)
        if savedname == None:
            pass
        elif savedname.lower().strip() == username.lower().strip():
            ans = messagebox.askyesno("Confirm Action", "User Already exists for that website. Would you like to update the password?")
            if not ans:
                messagebox.showwarning("Confrimation", "Password not saved")
                resetBoxes()
                return
            else:
                db.updatePW(encrypted_data, website, username, userID)
                resetBoxes()
                messagebox.showinfo("Success", "Password updated securely!")
                return

        db.createEntrySites(website, username, encrypted_data, userID)
        resetBoxes()
        messagebox.showinfo("Success", "Password saved securely!")
    else:
        messagebox.showwarning("Error", "Please fill in all fields.")

def resetBoxes():
            website_entry.delete(0, tk.END)
            username_entry.delete(0, tk.END)
            password_entry.delete(0, tk.END)

def search_password():
    website = website_entry.get()
    if not website:
        messagebox.showwarning("Error", "Please enter a website to search.")
        return

    if not os.path.exists(PASSWORD_FILE):
        messagebox.showerror("Error", "No saved passwords found.")
        return

    #saved_username,encPassword = db.retrieveInfo(website, userID)
    #saved_password = cipher.decrypt(encPassword).decode()
    #print(f'{saved_username}, {saved_password}')
    """try:
        with open(PASSWORD_FILE, "rb") as file:
            for line in file:
                decrypted_data = cipher.decrypt(line.strip()).decode()
                saved_website, saved_username, saved_password = decrypted_data.split(" | ")
                if saved_website == website:
                    messagebox.showinfo(
                        f"Details for {website}",
                        f"Username: {saved_username}\nPassword: {saved_password}"
                    )
                    return
        messagebox.showinfo("Not Found", f"No details found for {website}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")"""
    try:
        result = db.retrieveInfo(website, userID)
        if result is None:
            messagebox.showinfo("Not Found", f"No details found for {website}")
            return
        saved_username, encPassword = result
        if saved_username:
            encPassword = cipher.decrypt(encPassword).decode()
            saved_website, saved_username, saved_password = encPassword.split(" | ")
            itemsToCopy["user"] = saved_username
            itemsToCopy["passWord"] = saved_password
            #messagebox.showinfo(f"Details for {website}", f"Username: {saved_username}\nPassword: {saved_password}")
            showTextBoxForCopy(website, saved_username, saved_password)
            return
        elif saved_username is None:
            messagebox.showinfo("Not Found", f"No details found for {website}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
            
def showTextBoxForCopy(site: str, user: str, pw: str):
    top = tk.Toplevel(root)
    top.title(f'Details for {site}')
    top.config(bg="white")
    for i, (label, value) in enumerate([("Username", user), ("Password", pw)]):
        userNamelabel = tk.Label(top, text=label + ":", bg="white").grid(row=i, column=0, sticky="e", padx=8, pady=6)
        e = tk.Entry(top, width=40)
        e.grid(row=i, column=1, padx=8, pady=6)
        e.insert(0, value)
        e.configure(state="readonly")
        copyButt = tk.Button(top, text="Copy", command=lambda v=value: copyToClipboard(v)).grid(row=i, column=2, padx=8)

    closeButt = tk.Button(top, text="Close", command=top.destroy).grid(row=3, column=1, pady=10)

def showAllSites(userId: int):
    headers = []
    rows = []
    headers, rows = db.getallSites(userId)
    logUser = db.getUser(userID)
    showTable(f'All Sites For User: {logUser}', headers, rows)

def showTable(title, headers, rows):
    win = tk.Toplevel(root)
    win.title(title)
    win.config(bg="white")

    # Create header labels
    for col, header in enumerate(headers):
        tk.Label(win, text=header, bg="lightgray", font=("Segoe UI", 10, "bold"), padx=15, pady=15)\
          .grid(row=0, column=col, sticky="nsew")

    # Fill in the data rows
    for r, row_data in enumerate(rows, start=1):
        for c, value in enumerate(row_data):
            e = tk.Entry(win, width=40)
            e.grid(row=r, column=c, sticky="nsew")
            e.insert(0, str(value))
            e.configure(state="readonly")

    # Make columns stretch evenly
    for col in range(len(headers)):
        win.grid_columnconfigure(col, weight=1)

    # Close button
    closeButt = tk.Button(win, text="Close", command=win.destroy)
    closeButt.grid(row=len(rows)+1, column=0, columnspan=len(headers), pady=10)


#hotkeystoshortcut
saved_password = ""
saved_username = ""
root.bind("<Control-p>", copyPassword)
root.bind("<Control-P>", copyPassword)
root.bind("<Control-u>", copyUserName)
root.bind("<Control-U>", copyUserName)

# Buttons
button_style = {"font": ("Segoe UI", 11, "bold"), "bd": 0, "fg": "white", "width": 25, "height": 2}
generate_btn = tk.Button(frame, text="Generate Password", bg="orange", activebackground="darkorange", command=generate_password, **button_style)
generate_btn.grid(row=3, column=1, pady=10)

save_btn = tk.Button(frame, text="Save Password", bg="green", activebackground="lightgreen", command=save_password, **button_style)
save_btn.grid(row=4, column=1, pady=5)

search_btn = tk.Button(frame, text="Search Password", bg="steelblue", activebackground="dodgerblue", command=search_password, **button_style)
search_btn.grid(row=5, column=1, pady=5)

root.mainloop()
