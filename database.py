import sqlite3


def create_table() -> None:
    """
    Creates table if table for database doesn't
    already exist
    """
    conn = sqlite3.connect("Accounts.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS Accounts (
            id TEXT PRIMARY KEY,
            account_type TEXT,
            username TEXT,
            email_addr TEXT,
            password TEXT)
        """
    )
    print("Table created successfully...")
    conn.commit()
    conn.close()


def fetch_accounts() -> list:
    """
    Fetches accounts and returns accounts as list
    """
    conn = sqlite3.connect("Accounts.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Accounts")
    accounts = cursor.fetchall()
    conn.close()
    return accounts


def insert_account(id, account_type, username, email_addr, password) -> None:
    """
    Adds account to database
    """
    conn = sqlite3.connect("Accounts.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO Accounts (id, account_type, username, email_addr, password) VALUES (?, ?, ?, ?, ?)",
        (id, account_type, username, email_addr, password),
    )
    conn.commit()
    conn.close()


def delete_account(id) -> None:
    """
    Deletes account from databse by ID
    """
    conn = sqlite3.connect("Accounts.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Accounts WHERE id = ?", (id,))
    conn.commit()
    conn.close()


def update_account(
    new_account_type, new_username, new_email_addr, new_password, id
) -> None:
    """
    Updates account
    """
    conn = sqlite3.connect("Accounts.db")
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE Accounts SET account_type = ?, username = ?, email_addr = ?, password = ? WHERE id = ?",
        (new_account_type, new_username, new_email_addr, new_password, id),
    )
    conn.commit()
    conn.close()


def id_exists(id) -> bool:
    """
    Checks if account ID already exisits in database,
    If account ID exists, returns True, else, returns False
    """
    conn = sqlite3.connect("Accounts.db")
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM Accounts WHERE id = ?", (id,))
    result = cursor.fetchone()
    return result[0] > 0


create_table()
