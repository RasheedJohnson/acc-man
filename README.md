# Accounts Manager

#### **Video Demo:** [<URL HERE>](https://www.youtube.com/watch?v=yQvBZjovJ_w)

#### **Description:**

The app allows users to store passwords and account details similar to a password manager, however, it's intended to be run from an encrypted storage device. The app will store data in an SQLite database and within a csv backup file.

The backup file can have duplicated IDs, and these IDs will only be duplicated when updates were made to the original account (with that ID). In this way, the **_backup.csv_** file stores “logs” of changes made to passwords. Individual accounts can be deleted. The **_Accounts.db_** file can be deleted as well, **HOWEVER**, this will delete all accounts. And the only record of any accounts can be found in **_backup.csv_**.

### **Launching the app:**

Users can run `python app.py` with the terminal opened in the root folder.

### **Usage:**

The `_Add_` button will add the account to both the database (Accounts.db) file and the backup.csv file

The `_update_` button will only function once an item is selected. Selecting an item from the main database will allow users to adjust information within the entry fields and update that item by clicking the _update_ button.

Selecting an item:
If an item has been selected, and the ID is not changed, users will be prohibited from “adding” the account to the database. Only the _update_ button will work in this case if changes to fields other than the ID entry field have been made. Changing the ID entry field will allow users to add a new account to the database, not update an existing one unless the newly entered ID already exists within the database. In this case, the changes will apply to that account. Please be careful when handling your accounts. If accidental changes are made, users can toggle the button labeled “display”.

The button labeled “display” will allow users to switch between viewing the main database and the backup/log database. The backup/log database exists for when mistakes are made or accounts are edited. It also allows users to keep track of changes.

The `_Copy_` button allows users to copy passwords they’ve generated or passwords of a selected account to the clipboard.

The `_clear_` button will clear the entry fields and the selected item, thus preventing users from accidentally changing anything.

The `_delete_` button will only allow users to delete an item if selected - as the notification will likely inform users.

The `_Gen_` button within the password entry field allows for automatic password generating. A 12 character password will be added into the entry field. 12 is the default number of characters.
Changing the length of the password can be done by changing the **PASS_CHAR_LENGTH** constant located on line 12 within the **“project.py”** file.

### **Tests:**

At the moment, only the project.py file has been tested. Restructuring of app.py will be made on a later date.

Current tests include:
Tests for returning lists of tuples from lists of dicts,
Type tests,
Length and type of returned password tests,
Backup list type tests

Additional tests and adjustments will be made on a later date

### **Restrictions:**

Other than adding accounts and updated info to **_backup.csv_**, adjustments of any kind can be made to the **_backup.csv_** file.

The app will not allow users to delete from the **_backup.csv_** file.
The **_backup.csv_** has to be deleted manually or amendments need to be made by directly accessing the file.

### **Detailed explanation of files:**

**_*app.py*_**
This is the main GUI (graphical user interface) of the app and handles much of the operations for displaying and modifying the data.

**_*bg.png*_**
This is just the background of the app. It can be replaced with a background image of your choice also named **“bg.png”**.

**_*character.py*_**
Contains a list of letters, numbers, and symbols used by the password generator (“pass\*gen”) function within the **project.py** file.

**_*project.py*_**
Helper file for main **_*app.py*_** which allows for storing accounts to and reading accounts from the _*backup.csv*_ file.

#### **_*backup.csv*_**

Stores accounts in rows when new accounts are added or old accounts are updated. New accounts in this context are described as accounts with IDs that don’t yet exist within the database.

Both **_*backup.csv*_** and **_*Accounts.db*_** files contain dummy data for fake accounts. The **_*backup.csv*_** file can be emptied without removing the top row, and leaving one row blank. The **_*Accounts.db*_** file can be deleted entirely upon initial download of the project.

#### **_*Accounts.db*_**

Stores user’s accounts, (id, account type/domain, username, email, and password).

#### **_*test_project.py*_**

A test file for **_*project.py*_**

#### **Layout and design:**

I chose to keep the _delete_ button separate from the less “destructive” buttons

github: https://github.com/RasheedJohnson/

edX: Rasheed_J

Date: 14 - 08 - 2024
