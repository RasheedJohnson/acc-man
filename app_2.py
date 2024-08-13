"""
Customtkinter app for managing one's accounts.
"""

from tkinter import ttk, END
import tkinter as tk
import customtkinter
from PIL import Image
import pyperclip
import project
import database

# --------------------------- OPERATIONS --------------------------- #


def accounts_dict() -> dict:
    """
    Returns list of collected entries
    from fields as a dict
    """
    id = id_entry.get()
    account_type = account_type_entry.get()
    username = username_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    return {
        "id": id,
        "acc_type": account_type,
        "name": username,
        "email": email,
        "pass": password,
    }


def clear_input_fields(*clicked) -> None:
    """
    Clears all the information from the entry fields
    """
    if clicked:
        tree.selection_remove(tree.focus())
    id_entry.delete(0, customtkinter.END)
    account_type_entry.delete(0, customtkinter.END)
    username_entry.delete(0, customtkinter.END)
    email_entry.delete(0, customtkinter.END)
    password_entry.delete(0, customtkinter.END)


def display_accounts_from_db() -> None:
    """
    Fetches account information from the main database
    and inserts information into tree/table
    """
    accounts = database.fetch_accounts()
    tree.delete(*tree.get_children())
    for acc in accounts:
        tree.insert("", END, values=acc)


def display_accounts_from_backup() -> None:
    """
    Fetches account information from the backup.csv
    and inserts information into tree/table
    """
    accounts = project.read_from_backup()
    tree.delete(*tree.get_children())
    for acc in accounts:
        tree.insert("", END, values=acc)


def alternate_accounts(value) -> None:
    '''
    Displays either backup data or database data
    depending on the value it receives
    '''
    if value == "backup_list":
        display_accounts_from_backup()
        notice = "Backup data on display"
    else:
        display_accounts_from_db()
        notice = "Main database data on display"
    notification_info.configure(text=notice)


def insert_account() -> None:
    """
    Adds a new account to the database and
    the backup.csv file
    """
    info = accounts_dict()
    if not (
        info["id"]
        and info["acc_type"]
        and info["name"]
        and info["email"]
        and info["pass"]
    ):
        notice = "Fill all fields"
    elif database.id_exists(info["id"]):
        notice = "Error, ID exists"
    else:
        database.insert_account(
            info["id"], info["acc_type"], info["name"], info["email"], info["pass"]
        )
        project.store_in_backup(
            [info["id"], info["acc_type"], info["name"], info["email"], info["pass"]]
        )
        clear_input_fields()
        display_accounts_from_db()
        notice = "Account added"
    notification_info.configure(text=notice)


def display_data_within_entry_fields(event) -> None:
    """
    Fills entry fields with account details if
    an account is selected from the tree/table
    """
    selected_item = tree.focus()
    if selected_item:
        row = tree.item(selected_item)["values"]
        clear_input_fields()
        id_entry.insert(0, row[0])
        account_type_entry.insert(0, row[1])
        username_entry.insert(0, row[2])
        email_entry.insert(0, row[3])
        password_entry.insert(0, row[4])
    else:
        pass


def update_account() -> None:
    """
    Updates an existing account in the database with the
    modified information.
    """
    selected_item = tree.focus()
    if not selected_item:
        notice = "Choose Account to update"
    else:
        info = accounts_dict()
        project.store_in_backup(
            [info["id"], info["acc_type"], info["name"], info["email"], info["pass"]]
        )
        database.update_account(info["acc_type"], info["name"], info["email"], info["pass"], info["id"])
        display_accounts_from_db()
        clear_input_fields()
        notice = "Account Updated and re-added to backup"
    notification_info.configure(text=notice)


def delete_account() -> None:
    """
    Removes a selected account from the database.
    """
    selected_item = tree.focus()
    if not selected_item:
        notice = "Choose account first"
    else:
        id = id_entry.get()
        database.delete_account(id)
        display_accounts_from_db()
        clear_input_fields()
        notice = "Account deleted"
    notification_info.configure(text=notice)


def copy_to_clipboard() -> None:
    """
    Copies the password from the password entry field to your
    clipboard.
    """
    password = password_entry.get()
    pyperclip.copy(password)


def generate_pass() -> None:
    '''
    Generates 12 character password of
    letters, numbers, and symbols
    '''
    password_entry.delete(0, customtkinter.END)
    new_pass = project.generate_pass()
    password_entry.insert(0, new_pass)

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
font2 = ("Arial", 10, "normal")

ENTRY_COLOR = "#444"
ENTRY_TEXT = "#AAA"
BG_COLOR = "#050505"

message_info = "Welcome!"


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
    text_color=ENTRY_TEXT,
    fg_color=ENTRY_COLOR,
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
    text_color=ENTRY_TEXT,
    fg_color=ENTRY_COLOR,
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
    text_color=ENTRY_TEXT,
    fg_color=ENTRY_COLOR,
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
    text_color=ENTRY_TEXT,
    fg_color=ENTRY_COLOR,
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
    text_color=ENTRY_TEXT,
    fg_color=ENTRY_COLOR,
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
    command=insert_account,
)
add_button.place(x=20, y=270)

# Toggle backup or database display
seg_btn_label = customtkinter.CTkLabel(
    app, font=font1, text="display", text_color="#fff", bg_color=BG_COLOR
)
seg_btn_label.place(x=20, y=315)
toggle_values = ["backup_list", "database_list"]
toggle_btn = customtkinter.CTkSegmentedButton(
    app,
    font=font1,
    text_color="#fff",
    fg_color="#05638A",
    bg_color="#161C25",
    corner_radius=6,
    height=30,
    width=260,
    values=toggle_values,
    command=alternate_accounts,
)
toggle_btn.place(x=95, y=315)
# set default value
toggle_btn.set("database_list")

# Update Account
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
    command=update_account,
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
    command=lambda: clear_input_fields(True),
)
clear_button.place(x=940, y=315)

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
    command=delete_account,
    width=140,
)
delete_button.place(x=940, y=360)

# Copy Password
copy_button = customtkinter.CTkButton(
    app,
    font=font1,
    text_color="#fff",
    text="Copy Password",
    fg_color="#05638A",
    hover_color="#8888AA",
    bg_color="transparent",
    cursor="hand2",
    corner_radius=6,
    command=copy_to_clipboard,
    width=140,
)
copy_button.place(x=940, y=270)

# Generate Password
gen_button = customtkinter.CTkButton(
    password_entry,
    font=font1,
    text_color="#fff",
    text="Gen",
    fg_color="#05638A",
    hover_color="#8888AA",
    bg_color="transparent",
    cursor="hand2",
    corner_radius=6,
    command=generate_pass,
    height=23,
    width=45,
)
gen_button.place(x=133, y=3)



# ------------------------- ACCOUNTS SHEET ------------------------- #


style = ttk.Style(app)
style.theme_use("xpnative")
style.configure(
    "Treeview",
    font=font2,
    foreground="#bbb",
    background="#222",
    fieldbackground="#140b15",
)
style.map("Treeview", background=[("selected", "#555566")])

tree = ttk.Treeview(app, height=15)

tree["columns"] = ("ID", "Account", "Username", "Email", "Password")

tree.column("#0", width=0, stretch=tk.NO)  # Hide the default first Column
dict_of_widths = {1: 35, 2: 80, 3: 120, 4: 155, 5: 210}  # Dict of widths for each field
count = 1
for item in tree["columns"]:
    tree.column(item, anchor=tk.CENTER, width=dict_of_widths[count])
    count += 1

list = {1: "ID", 2: "Account", 3: "Username", 4: "Email", 5: "Password"}  # Titles/field
count = 1
for item in tree["columns"]:
    tree.heading(list[count], text=list[count])
    count += 1

tree.place(x=310, y=60)

tree.bind("<ButtonRelease>", display_data_within_entry_fields)

display_accounts_from_db()

app.mainloop()
