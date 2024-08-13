import random
import csv
import sys

def main():
    '''
    Helper module for main app.
    Responsible for storing user accounts,
    generating passwords,
    '''
    print(read_from_backup())
    
    # 

def store_in_backup(arr):
    '''
    receive backups of all saved accounts
    in backups.csv
    '''
    with open("backup.csv", "a") as file:
        writer = csv.DictWriter(file, fieldnames=["id", "account_type", "username", "email", "password"])
        writer.writerow({"id": arr[0], "account_type": arr[1], "username": arr[2], "email": arr[3], "password": arr[4]})
        

def parse_dict(list) -> tuple:
    '''
    Converts incoming list of dicts
    and returns it as a list of tuples
    '''
    tuples_list = []
    for acc in list:
        tuples_list.append((acc["id"], acc["account_type"], acc["username"], acc["email"], acc["password"]))
    return tuples_list


def read_from_backup() -> list:
    '''
    Reads from backups.csv and returns
    list of tuples as account data
    '''
    list_of_accounts = []
    with open("backup.csv", "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            list_of_accounts.append(row)
    return parse_dict(list_of_accounts)


def generate_pass():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    random_option = [letters, numbers, letters, symbols]
    password = ""
    for i in range(12):
        type_char = random.choice(random_option)
        password += random.choice(type_char)
    return password

if __name__ == "__main__":
    main()