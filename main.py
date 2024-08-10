import customtkinter
from tkinter import *
from tkinter import ttk
import tkinter as tk
from tkinter import messagebox
import database
from PIL import Image

# ----------------------- PASSWORD GENERATOR ----------------------- #

# --------------------------- OPERATIONS --------------------------- #


def clear_input_fields(*clicked):
    if clicked:
        tree.selection_remove(tree.focus())
    id_entry.delete(0,customtkinter.END)
    account_type_entry.delete(0,customtkinter.END)
    username_entry.delete(0,customtkinter.END)
    email_entry.delete(0,customtkinter.END)
    password_entry.delete(0,customtkinter.END)
    
    
def display_accounts():
    accounts = database.fetch_accounts()
    tree.delete(*tree.get_children())
    for account in accounts:
        tree.insert("", END, values=account)


def insert_account():
    id = id_entry.get()
    account_type = account_type_entry.get()
    username = username_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    
    if not (id and account_type and username and email and password):
        messagebox.showerror("Error", "Enter all fields...")
    elif database.id_exists(id):
        message_info = "Error, ID exists"
    else:
        database.insert_account(id, account_type, username, email, password)
        clear_input_fields()
        display_accounts()
        message_info = "Account added"
    notification_info.configure(text=message_info)


def display_data_within_entry_fields(event):
    selected_item = tree.focus()
    if selected_item:
        row = tree.item(selected_item)["values"]
        clear_input_fields()
        id_entry.insert(0,row[0])
        account_type_entry.insert(0,row[1])
        username_entry.insert(0,row[2])
        email_entry.insert(0,row[3])
        password_entry.insert(0,row[4])
    else:
        pass
        
    
def update_account():
    id = id_entry.get()
    account_type = account_type_entry.get()
    username = username_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    
    if not (id and account_type and username and email and password):
        messagebox.showerror("Error", "Enter all fields...")
    elif not database.id_exists(id):
        messagebox.showerror("Error", "Account does not exist to be updated")
    else:
        database.insert_account(id, account_type, username, email, password)
        clear_input_fields()
        display_accounts()
        messagebox.showinfo("Success", "Account added successfully")




# ---------------------------- UI SETUP ---------------------------- #

app = customtkinter.CTk()
app.title("Account Manager")
app.geometry("1100x420")
app.config(bg="#161c25")
app.resizable(False, False)

image = Image.open("bg.png")
background_image = customtkinter.CTkImage(image, size=(1100, 420))
bg_lbl = customtkinter.CTkLabel(app, text="", image=background_image)
bg_lbl.place(x=0, y=0)

font0 = ("Arial", 17, "bold")
font1 = ("Lexend", 14, "normal")
font1i = ("Lexend", 14, "italic")
font2 = ("Arial", 8, "normal")
BG_COLOR = "#050505"

message_info = ""


# ----------------------- LABELS AND ENTRIES ----------------------- #

# Title
title_label = customtkinter.CTkLabel(
    app, font=font0, text="Accounts Manager", bg_color=BG_COLOR
)
title_label.pack(padx=50, pady=20)

# ID Setup
id_label = customtkinter.CTkLabel(
    app, font=font1, text="ID:", text_color="#fff", bg_color=BG_COLOR
)
id_label.place(x=20, y=60)
id_entry = customtkinter.CTkEntry(
    app,
    font=font1,
    text_color="#333",
    fg_color="#ddd",
    border_color="#0C9295",
    border_width=1,
    width=180,
)
id_entry.place(x=100, y=60)

# Account Type Setup
account_type_label = customtkinter.CTkLabel(
    app, font=font1, text="Account", text_color="#fff", bg_color=BG_COLOR
)
account_type_label.place(x=20, y=100)
account_type_entry = customtkinter.CTkEntry(
    app,
    font=font1,
    text_color="#333",
    fg_color="#ddd",
    border_color="#0C9295",
    border_width=1,
    width=180,
)
account_type_entry.place(x=100, y=100)

# Username Setup
username_label = customtkinter.CTkLabel(
    app, font=font1, text="Username", text_color="#fff", bg_color=BG_COLOR
)
username_label.place(x=20, y=140)
username_entry = customtkinter.CTkEntry(
    app,
    font=font1,
    text_color="#333",
    fg_color="#ddd",
    border_color="#0C9295",
    border_width=1,
    width=180,
)
username_entry.place(x=100, y=140)

# Email Address Setup
email_label = customtkinter.CTkLabel(
    app, font=font1, text="Email", text_color="#fff", bg_color=BG_COLOR
)
email_label.place(x=20, y=180)
email_entry = customtkinter.CTkEntry(
    app,
    font=font1,
    text_color="#333",
    fg_color="#ddd",
    border_color="#0C9295",
    border_width=1,
    width=180,
)
email_entry.place(x=100, y=180)

# Password
password_label = customtkinter.CTkLabel(
    app, font=font1, text="Password", text_color="#fff", bg_color=BG_COLOR
)
password_label.place(x=20, y=220)
password_entry = customtkinter.CTkEntry(
    app,
    font=font1,
    text_color="#333",
    fg_color="#ddd",
    border_color="#0C9295",
    border_width=1,
    width=180,
)
password_entry.place(x=100, y=220)

# Notifications
notification_heading = customtkinter.CTkLabel(
    app, font=font1i, text="Notifications:", text_color="#5A5", bg_color=BG_COLOR
)
notification_heading.place(x=940, y=80)

# Notifications
notification_info = customtkinter.CTkLabel(
    app, font=font1i, text=message_info, text_color="#5A5", bg_color=BG_COLOR
)
notification_info.place(x=940, y=100)


# ----------------------------- BUTTONS ---------------------------- #

# Add
add_button = customtkinter.CTkButton(
    app,
    font=font1,
    text_color="#fff",
    text="Add Account",
    fg_color="#05638A",
    hover_color="#8888AA",
    bg_color="#161C25",
    cursor="hand2",
    corner_radius=6,
    width=260,
    command=insert_account
)
add_button.place(x=20, y=310)

# Update
update_button = customtkinter.CTkButton(
    app,
    font=font1,
    text_color="#fff",
    text="Update Account",
    fg_color="#05638A",
    hover_color="#8888AA",
    bg_color="#161C25",
    cursor="hand2",
    corner_radius=6,
    width=260,
)
update_button.place(x=20, y=360)

# Clear selection
clear_button = customtkinter.CTkButton(
    app,
    font=font1,
    text_color="#fff",
    text="Clear",
    fg_color="#05638A",
    hover_color="#8888AA",
    bg_color="#161C25",
    cursor="hand2",
    corner_radius=6,
    width=140,
    command=lambda:clear_input_fields(True)
)
clear_button.place(x=940, y=310)

# Delete
delete_button = customtkinter.CTkButton(
    app,
    font=font1,
    text_color="#fff",
    text="Delete Account",
    fg_color="#882233",
    hover_color="#A8435A",
    bg_color="#161C25",
    cursor="hand2",
    corner_radius=6,
    width=140,
)
delete_button.place(x=940, y=360)


# ------------------------- ACCOUNTS SHEET ------------------------- #


style = ttk.Style(app)
style.theme_use("xpnative")
style.configure("Treeview", font=font2, foreground="#bbb", background="#222", fieldbackground="#140b15")
style.map("Treeview", background=[("selected", "#555566")])

tree = ttk.Treeview(app, height=15)

tree["columns"] = ("ID", "Account", "Username", "Email", "Password")

tree.column("#0", width=0, stretch=tk.NO)  # Hide the default first Column
list = {1:40, 2:80, 3:120, 4:160, 5:220}   # Dict of widths for each field
count = 1
for item in tree["columns"]:
    tree.column(item, anchor=tk.CENTER, width=list[count])
    count += 1

list = {1:"ID", 2:"Account", 3:"Username", 4:"Email", 5:"Password"}   # Titles/field
count = 1
for item in tree["columns"]:
    tree.heading(list[count], text=list[count])
    count += 1


tree.place(x=300, y=60)

tree.bind("<ButtonRelease>", display_data_within_entry_fields)

display_accounts()

app.mainloop()
