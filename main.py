import tkinter as tk
from tkinter import messagebox
import secrets
import string
import json
import os

# Color Theme
BG_COLOR = "#ffffff"
BTN_COLOR = "#ff9933"
FONT_COLOR = "#000000"

password_file = "passwords.json"

def check_strength(pwd):
    length = len(pwd)
    has_upper = any(c.isupper() for c in pwd)
    has_lower = any(c.islower() for c in pwd)
    has_digit = any(c.isdigit() for c in pwd)
    has_special = any(c in string.punctuation for c in pwd)
    score = sum([has_upper, has_lower, has_digit, has_special])

    if length >= 12 and score == 4:
        return "Strong"
    elif length >= 8 and score >= 3:
        return "Medium"
    else:
        return "Weak"

def generate_password():
    chars = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(chars) for _ in range(12))
    entry_pwd.delete(0, tk.END)
    entry_pwd.insert(0, password)
    lbl_strength.config(text=f"Strength: {check_strength(password)}")

def save_password():
    site = entry_site.get().strip()
    username = entry_user.get().strip()
    pwd = entry_pwd.get().strip()

    if not site or not username or not pwd:
        messagebox.showerror("Error", "Fill all fields.")
        return

    data = {site: {"username": username, "password": pwd}}

    if os.path.exists(password_file):
        with open(password_file, "r") as f:
            try:
                existing_data = json.load(f)
            except json.JSONDecodeError:
                existing_data = {}
    else:
        existing_data = {}

    existing_data.update(data)

    with open(password_file, "w") as f:
        json.dump(existing_data, f, indent=4)

    messagebox.showinfo("Saved", "Password saved successfully!")
    entry_site.delete(0, tk.END)
    entry_user.delete(0, tk.END)
    entry_pwd.delete(0, tk.END)
    lbl_strength.config(text="Strength:")

def check_password_strength():
    pwd = entry_pwd.get()
    strength = check_strength(pwd)
    lbl_strength.config(text=f"Strength: {strength}")

# GUI Setup
app = tk.Tk()
app.title("Password Tool")
app.geometry("400x350")
app.configure(bg=BG_COLOR)

tk.Label(app, text="Website", bg=BG_COLOR, fg=FONT_COLOR).pack()
entry_site = tk.Entry(app, width=40)
entry_site.pack(pady=5)

tk.Label(app, text="Username", bg=BG_COLOR, fg=FONT_COLOR).pack()
entry_user = tk.Entry(app, width=40)
entry_user.pack(pady=5)

tk.Label(app, text="Password", bg=BG_COLOR, fg=FONT_COLOR).pack()
entry_pwd = tk.Entry(app, width=40, show="*")
entry_pwd.pack(pady=5)

lbl_strength = tk.Label(app, text="Strength:", bg=BG_COLOR, fg=FONT_COLOR)
lbl_strength.pack()

btn_check = tk.Button(app, text="Check Strength", bg=BTN_COLOR, command=check_password_strength)
btn_check.pack(pady=5)

btn_generate = tk.Button(app, text="Generate Password", bg=BTN_COLOR, command=generate_password)
btn_generate.pack(pady=5)

btn_save = tk.Button(app, text="Save Password", bg=BTN_COLOR, command=save_password)
btn_save.pack(pady=10)

app.mainloop()
