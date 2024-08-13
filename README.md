# Accounts Manager

#### **Video Demo:** <URL HERE>

#### **Description:**

The app allows users to store passwords and account details similar to a password manager, however, it's intended to be run from an encrypted storage device. The app will store data in an SQLite database and within a csv backup file.

The backup file can have duplicated IDs, and these IDs will only be duplicated when updates were made to the original account (with that ID). In this way, the **_backup.csv_** file stores “logs” of changes made to passwords. Individual accounts can be deleted. The **_Accounts.db_** file can be deleted as well, **HOWEVER**, this will delete all accounts. And the only record of any accounts can be found in **_backup.csv_**.

### **Launching the app:**

Users can run `python app.py` with the terminal opened in the root folder.

### **Usage:**

The _Add_ button will add the account to both the database (Accounts.db) file and the backup.csv file

The _update_ button will only function once an item is selected. Selecting an item from the main database will allow users to adjust information within the entry fields and update that item by clicking the _update_ button.

Selecting an item:
If an item has been selected, and the ID is not changed, users will be prohibited from “adding” the account to the database. Only the _update_ button will work in this case if changes to fields other than the ID entry field have been made. Changing the ID entry field will allow users to add a new account to the database, not update an existing one unless the newly entered ID already exists within the database. In this case, the changes will apply to that account. Please be careful when handling your accounts. If accidental changes are made, users can toggle the button labeled “display”.

The button labeled “display” will allow users to switch between viewing the main database and the backup/log database. The backup/log database exists for when mistakes are made or accounts are edited. It also allows users to keep track of changes.

The _clear_ button will clear the entry fields and the selected item, thus preventing users from accidentally changing anything.

The _delete_ button will only allow users to delete an item if selected - as the notification will likely inform users.

The _Gen_ button within the password entry field allows for automatic password generating. A 12 character password will be added into the entry field. 12 is the default number of characters.
Changing the length of the password can be done by changing the **PASS_CHAR_LENGTH** constant located on line 12 within the “project.py” file.

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
