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

# Maps tree item ids to full (unmasked) account rows
tree_records = {}

WINDOW_W = 780
WINDOW_H = 460


def mask_email(email) -> str:
    """
    Hides local-part characters after the first letter
    and before "@" when present. e.g. j***@mail.com
    """
    email = "" if email is None else str(email)
    if "@" in email:
        local, domain = email.split("@", 1)
        if len(local) <= 1:
            return f"{local}@{domain}"
        return f"{local[0]}{'*' * (len(local) - 1)}@{domain}"
    if len(email) <= 1:
        return email
    return email[0] + "*" * (len(email) - 1)


def mask_password(password) -> str:
    """Hides every password character with '*'."""
    password = "" if password is None else str(password)
    return "*" * len(password)


def masked_account_row(acc) -> tuple:
    """Display values for the tree: email and password masked."""
    return (acc[0], acc[1], acc[2], mask_email(acc[3]), mask_password(acc[4]))


def populate_tree(accounts) -> None:
    """
    Fills the tree with masked rows while keeping
    the real account details available for selection/copy.
    """
    tree_records.clear()
    tree.delete(*tree.get_children())
    for acc in accounts:
        item_id = tree.insert("", END, values=masked_account_row(acc))
        tree_records[item_id] = tuple(acc)


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
    populate_tree(database.fetch_accounts())
    notice = "Data from main\ndatabase on display"
    notification_info.configure(text=notice)


def display_accounts_from_backup() -> None:
    """
    Fetches account information from the backup.csv
    and inserts information into tree/table
    """
    populate_tree(project.read_from_backup())
    notice = "Data from backup\ndatabase on display"
    notification_info.configure(text=notice)


def alternate_accounts(value) -> None:
    """
    Displays either backup data or database data
    depending on the value it receives
    """
    if value == "backup_list":
        display_accounts_from_backup()
    else:
        display_accounts_from_db()


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
    Fills entry fields with the real (unmasked) account
    details if an account is selected from the tree/table.
    """
    selected_item = tree.focus()
    row = tree_records.get(selected_item)
    if selected_item and row:
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
        database.update_account(
            info["acc_type"], info["name"], info["email"], info["pass"], info["id"]
        )
        display_accounts_from_db()
        clear_input_fields()
        notice = "Account Updated\nlog added to\nbackup"
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
    """
    Generates 12 character password of
    letters, numbers, and symbols
    """
    password_entry.delete(0, customtkinter.END)
    new_pass = project.generate_pass()
    password_entry.insert(0, new_pass)


# ---------------------------- UI SETUP ---------------------------- #

app = customtkinter.CTk()
app.title("Account Manager")
app.geometry(f"{WINDOW_W}x{WINDOW_H}")
app.config(bg="#161c25")
app.resizable(False, False)

image = Image.open("bg.png")
background_image = customtkinter.CTkImage(image, size=(WINDOW_W, WINDOW_H))
bg_lbl = customtkinter.CTkLabel(app, text="", image=background_image)
bg_lbl.place(x=0, y=0)

font0 = ("Arial", 16, "bold")
font1 = ("Lexend", 13, "normal")
font1i = ("Lexend", 12, "italic")
font2 = ("Arial", 9, "normal")

ENTRY_COLOR = "#444"
ENTRY_TEXT = "#AAA"
BG_COLOR = "#050505"

LEFT_X = 18
ENTRY_X = 95
ENTRY_W = 155
FORM_BTN_W = 232
TREE_X = 275
RIGHT_X = 655
RIGHT_BTN_W = 108

message_info = "Welcome!"


# ----------------------- LABELS AND ENTRIES ----------------------- #

# Title
title_label = customtkinter.CTkLabel(
    app, font=font0, text="Accounts Manager", bg_color=BG_COLOR
)
title_label.pack(padx=40, pady=14)

# ID Setup
id_label = customtkinter.CTkLabel(
    app, font=font1, text="ID:", text_color="#fff", bg_color=BG_COLOR
)
id_label.place(x=LEFT_X, y=52)
id_entry = customtkinter.CTkEntry(
    app,
    font=font1,
    text_color=ENTRY_TEXT,
    fg_color=ENTRY_COLOR,
    border_color="#0C9295",
    border_width=1,
    width=ENTRY_W,
)
id_entry.place(x=ENTRY_X, y=52)

# Account Type Setup
account_type_label = customtkinter.CTkLabel(
    app, font=font1, text="Account", text_color="#fff", bg_color=BG_COLOR
)
account_type_label.place(x=LEFT_X, y=90)
account_type_entry = customtkinter.CTkEntry(
    app,
    font=font1,
    text_color=ENTRY_TEXT,
    fg_color=ENTRY_COLOR,
    border_color="#0C9295",
    border_width=1,
    width=ENTRY_W,
)
account_type_entry.place(x=ENTRY_X, y=90)

# Username Setup
username_label = customtkinter.CTkLabel(
    app, font=font1, text="Username", text_color="#fff", bg_color=BG_COLOR
)
username_label.place(x=LEFT_X, y=128)
username_entry = customtkinter.CTkEntry(
    app,
    font=font1,
    text_color=ENTRY_TEXT,
    fg_color=ENTRY_COLOR,
    border_color="#0C9295",
    border_width=1,
    width=ENTRY_W,
)
username_entry.place(x=ENTRY_X, y=128)

# Email Address Setup
email_label = customtkinter.CTkLabel(
    app, font=font1, text="Email", text_color="#fff", bg_color=BG_COLOR
)
email_label.place(x=LEFT_X, y=166)
email_entry = customtkinter.CTkEntry(
    app,
    font=font1,
    text_color=ENTRY_TEXT,
    fg_color=ENTRY_COLOR,
    border_color="#0C9295",
    border_width=1,
    width=ENTRY_W,
)
email_entry.place(x=ENTRY_X, y=166)

# Password (characters hidden in the field; real value still stored)
password_label = customtkinter.CTkLabel(
    app, font=font1, text="Password", text_color="#fff", bg_color=BG_COLOR
)
password_label.place(x=LEFT_X, y=204)
password_entry = customtkinter.CTkEntry(
    app,
    font=font1,
    text_color=ENTRY_TEXT,
    fg_color=ENTRY_COLOR,
    border_color="#0C9295",
    border_width=1,
    width=ENTRY_W,
    show="*",
)
password_entry.place(x=ENTRY_X, y=204)

# Notifications
notification_heading = customtkinter.CTkLabel(
    app, font=font1i, text="Notifications:", text_color="#5A5", bg_color=BG_COLOR
)
notification_heading.place(x=RIGHT_X, y=52)
notification_info = customtkinter.CTkLabel(
    app,
    font=font1i,
    text=message_info,
    text_color="#5A5",
    bg_color=BG_COLOR,
    width=RIGHT_BTN_W,
    anchor="w",
    justify="left",
)
notification_info.place(x=RIGHT_X, y=74)


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
    width=FORM_BTN_W,
    command=insert_account,
)
add_button.place(x=LEFT_X, y=255)

# Toggle backup or database display
seg_btn_label = customtkinter.CTkLabel(
    app, font=font1, text="display", text_color="#fff", bg_color=BG_COLOR
)
seg_btn_label.place(x=LEFT_X, y=302)
toggle_values = ["backup_list", "database_list"]
toggle_btn = customtkinter.CTkSegmentedButton(
    app,
    font=font1,
    text_color="#fff",
    fg_color="#05638A",
    bg_color="#161C25",
    corner_radius=6,
    height=28,
    width=FORM_BTN_W,
    values=toggle_values,
    command=alternate_accounts,
)
toggle_btn.place(x=88, y=302)
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
    width=FORM_BTN_W,
    command=update_account,
)
update_button.place(x=LEFT_X, y=348)

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
    width=RIGHT_BTN_W,
)
copy_button.place(x=RIGHT_X, y=255)

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
    width=RIGHT_BTN_W,
    command=lambda: clear_input_fields(True),
)
clear_button.place(x=RIGHT_X, y=302)

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
    width=RIGHT_BTN_W,
)
delete_button.place(x=RIGHT_X, y=348)

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
    height=22,
    width=42,
)
gen_button.place(x=110, y=3)


# ------------------------- ACCOUNTS SHEET ------------------------- #


style = ttk.Style(app)
style.theme_use("xpnative")
style.configure(
    "Treeview",
    font=font2,
    foreground="#bbb",
    background="#222",
    fieldbackground="#140b15",
    rowheight=20,
)
style.map("Treeview", background=[("selected", "#555566")])

tree = ttk.Treeview(app, height=14)

tree["columns"] = ("ID", "Account", "Username", "Email", "Password")

tree.column("#0", width=0, stretch=tk.NO)  # Hide the default first Column
dict_of_widths = {1: 28, 2: 58, 3: 72, 4: 110, 5: 90}
count = 1
for item in tree["columns"]:
    tree.column(item, anchor=tk.CENTER, width=dict_of_widths[count])
    count += 1

list = {1: "ID", 2: "Account", 3: "Username", 4: "Email", 5: "Password"}
count = 1
for item in tree["columns"]:
    tree.heading(list[count], text=list[count])
    count += 1

tree.place(x=TREE_X, y=52)

tree.bind("<ButtonRelease>", display_data_within_entry_fields)

display_accounts_from_db()

app.mainloop()
