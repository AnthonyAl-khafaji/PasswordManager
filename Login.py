import tkinter as tk
from tkinter import messagebox, simpledialog
import bcrypt
import os
import sqlLiteDB as db


class LoginScreen:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Login Screen")
        self.pepper = b"CSI3460"     # b is used to define a bytes literal in Python.
        self.db = db.userDB()# Initialize the database connection
        self.db.createUserTable()
        self.buildGui()
        self.authenticated = False
        self.userID = None

    def buildGui(self):
        #Banner
        bannerFrame = tk.Frame(self.root, bg="#336699", height=50)  
        bannerFrame.pack(fill="x", side="top")
        bannerLabel = tk.Label(bannerFrame, text="Pass Keeper", font=("Helvetica", 16, "bold"), fg="white", bg="#336699")
        bannerLabel.pack(pady=10)

        #Window
        mainContentFrame = tk.Frame(self.root) 
        mainContentFrame.pack(expand=True, anchor="center")
        #username
        tk.Label(mainContentFrame, text="Username:", font=("Helvetica", 12)).pack(pady=(10, 0))
        self.userNameEntry = tk.Entry(mainContentFrame, width=30, relief="solid", bd=1) 
        self.userNameEntry.pack(padx=10, pady=(0, 10))
        self.userName = self.userNameEntry.get().strip()
        #password
        tk.Label(mainContentFrame, text="Password:", font=("Helvetica", 12)).pack()
        self.passwordEntry = tk.Entry(mainContentFrame, show="*", width=30, relief="solid", bd=1)  
        self.passwordEntry.pack(padx=10, pady=(0, 10))

        buttonFrame = tk.Frame(mainContentFrame)  
        buttonFrame.pack(pady=10)
        #login button
        loginButton = tk.Button(buttonFrame, text="Login", command=self.loginProcess, width=12, height=1, bg="#4CAF50", fg="white", relief="raised")
        loginButton.grid(row=0, column=0, padx=5)
        #new user button
        createButton = tk.Button(buttonFrame, text="Create New User", command=self.createNewUser, width=15, height=1, bg="#2196F3", fg="white", relief="raised")
        createButton.grid(row=0, column=1, padx=5)

    def loginProcess(self):
          
        username = self.userNameEntry.get().strip()
        password = self.passwordEntry.get()

        if not username or not password:
            missing = 'Username' if not username else 'Password'
            messagebox.showerror("Error", f"{missing} cannot be empty.")
            return False

        valid = self.db.userExists(username)
        if not valid:
            messagebox.showinfo("User Not Found", "No such user exists.")
            return False
        hashPW, self.userID = self.db.GetPassHash(username)
        if self.verifyPasswordWithSalt(password, hashPW):
            messagebox.showinfo("Success", "Logging in.")
            #self.userID = self.getuserID()
            self.authenticated = True
            self.root.destroy()  # Close the login window
        else:
            messagebox.showerror("Error", "Incorrect password.")
            return False
    
    def createNewUser(self):

        username = simpledialog.askstring("Create User", "Enter new username: ", parent=self.root)

        if username == None or username == "":

            messagebox.showerror("Error", "Username cannot be empty.")
            return
        username = username.strip()
        if self.db.userExists(username):
            messagebox.showerror("Error", "User already exists.")
            return

        password = simpledialog.askstring("Create User", "Enter password:", show="*", parent=self.root)
        if not password:
            messagebox.showerror("Error", "Password cannot be empty.")
            return

        confirm = simpledialog.askstring("Create User", "Re-enter password to confirm:", show="*", parent=self.root)
        if password != confirm:
            messagebox.showerror("Error", "Passwords do not match.")
            return
        newHash = self.hashPassword(password)
        added = self.db.AddUser(username, newHash)
        if added:
            messagebox.showinfo("Success", "User created successfully.")
        else:
            messagebox.showerror("Error", "Failed to create user.")

    def hashPassword(self, password):

        numRounds = 12 # Number of rounds for bcrypt hashing but can be adjusted for security vs performance trade-off

        PepperPW = password.encode('utf-8') + self.pepper
        hashed = bcrypt.hashpw(PepperPW, bcrypt.gensalt(rounds=numRounds))

        return hashed

    def verifyPasswordWithSalt(self, password, hashed_password):

        combined_password_to_check = (password + self.pepper.decode('utf-8')).encode('utf-8') 
        newValue = bcrypt.checkpw(combined_password_to_check, hashed_password)

        return newValue

    def getAuthenticated(self):
        return self.authenticated

    def getUser(self):
        return self.userID




