import tkinter as tk
from tkinter import messagebox
import random
import string
import json
from cryptography.fernet import Fernet
import os

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

# Ensure data folder exists
os.makedirs(DATA_FOLDER, exist_ok=True)


# --- GUI Setup ---
root = tk.Tk()
root.title("Password Manager")
root.config(padx=20, pady=20)

# Labels
tk.Label(root, text="Website:").grid(row=0, column=0)
tk.Label(root, text="Username/Email:").grid(row=1, column=0)
tk.Label(root, text="Password:").grid(row=2, column=0)

# Entry fields
website_entry = tk.Entry(root, width=35)
website_entry.grid(row=0, column=1, columnspan=2)

username_entry = tk.Entry(root, width=35)
username_entry.grid(row=1, column=1, columnspan=2)

password_entry = tk.Entry(root, width=21)
password_entry.grid(row=2, column=1)


# Functions
def generate_password():
    chars = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(chars) for _ in range(12))
    password_entry.delete(0, tk.END)
    password_entry.insert(0, password)


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


def save_password():
    website = website_entry.get()
    username = username_entry.get()
    password = password_entry.get()

    if website and username and password:
        data = f"{website} | {username} | {password}\n"
        encrypted_data = cipher.encrypt(data.encode())

        # Save in data folder
        with open(PASSWORD_FILE, "ab") as file:
            file.write(encrypted_data + b"\n")

        website_entry.delete(0, tk.END)
        username_entry.delete(0, tk.END)
        password_entry.delete(0, tk.END)
        messagebox.showinfo("Success", "Password saved securely!")
    else:
        messagebox.showwarning("Error", "Please fill in all fields.")


# Buttons
generate_btn = tk.Button(root, text="Generate Password", command=generate_password)
generate_btn.grid(row=2, column=2)

save_btn = tk.Button(root, text="Save Password", width=36, command=save_password)
save_btn.grid(row=3, column=1, columnspan=2)

search_btn = tk.Button(root, text="Search Password", width=36, command=search_password)
search_btn.grid(row=4, column=1, columnspan=2)

root.mainloop()
