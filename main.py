import tkinter as tk
from tkinter import messagebox
import random
import string
import json
from cryptography.fernet import Fernet
import os
import Login

# --- Login Setup ---
loginScreen = Login.LoginScreen()  # Initialize the login screen
loginScreen.root.mainloop()  # Run the login screen
run = False 
while not run:
  run = loginScreen.getAuthenticated()# Initialize the login screen
# proceed with the password manager

# --- Encryption Setup ---
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


# --- GUI Setup ---
root = tk.Tk()
root.title("Password Manager")
root.geometry("500x400")
root.configure(bg="#1f2c34")  # Dark background

# Title
title_label = tk.Label(root, text="Password Manager", font=("Arial", 20, "bold"), fg="white", bg="#1f2c34", pady=10)
title_label.pack()

# Frame
frame = tk.Frame(root, bg="#ffffff", padx=20, pady=20, bd=0, relief="flat")
frame.place(relx=0.5, rely=0.5, anchor="center")

# Labels
label_font = ("Segoe UI", 11, "bold")
tk.Label(frame, text="Website:", font=label_font, bg="#ffffff").grid(row=0, column=0, sticky="w", pady=8)
tk.Label(frame, text="Username/Email:", font=label_font, bg="#ffffff").grid(row=1, column=0, sticky="w", pady=8)
tk.Label(frame, text="Password:", font=label_font, bg="#ffffff").grid(row=2, column=0, sticky="w", pady=8)

# Entry fields
entry_font = ("Segoe UI", 11)
website_entry = tk.Entry(frame, width=30, font=entry_font, bd=1, relief="flat", highlightbackground="#3498db", highlightthickness=1)
website_entry.grid(row=0, column=1, pady=8)

username_entry = tk.Entry(frame, width=30, font=entry_font, bd=1, relief="flat", highlightbackground="#3498db", highlightthickness=1)
username_entry.grid(row=1, column=1, pady=8)

password_entry = tk.Entry(frame, width=30, font=entry_font, bd=1, relief="flat", highlightbackground="#3498db", highlightthickness=1)
password_entry.grid(row=2, column=1, pady=8)


# Functions
def generate_password():
    chars = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(chars) for _ in range(14))
    password_entry.delete(0, tk.END)
    password_entry.insert(0, password)


def save_password():
    website = website_entry.get()
    username = username_entry.get()
    password = password_entry.get()

    if website and username and password:
        data = f"{website} | {username} | {password}\n"
        encrypted_data = cipher.encrypt(data.encode())

        with open(PASSWORD_FILE, "ab") as file:
            file.write(encrypted_data + b"\n")

        website_entry.delete(0, tk.END)
        username_entry.delete(0, tk.END)
        password_entry.delete(0, tk.END)
        messagebox.showinfo("Success", "Password saved securely!")
    else:
        messagebox.showwarning("Error", "Please fill in all fields.")


def search_password():
    website = website_entry.get()
    if not website:
        messagebox.showwarning("Error", "Please enter a website to search.")
        return

    if not os.path.exists(PASSWORD_FILE):
        messagebox.showerror("Error", "No saved passwords found.")
        return

    try:
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
        messagebox.showerror("Error", f"An error occurred: {e}")


# Buttons
button_style = {"font": ("Segoe UI", 11, "bold"), "bd": 0, "fg": "white", "width": 25, "height": 2}
generate_btn = tk.Button(frame, text="Generate Password", bg="#f39c12", activebackground="#e67e22", command=generate_password, **button_style)
generate_btn.grid(row=3, column=1, pady=10)

save_btn = tk.Button(frame, text="Save Password", bg="#27ae60", activebackground="#2ecc71", command=save_password, **button_style)
save_btn.grid(row=4, column=1, pady=5)

search_btn = tk.Button(frame, text="Search Password", bg="#2980b9", activebackground="#3498db", command=search_password, **button_style)
search_btn.grid(row=5, column=1, pady=5)

root.mainloop()
