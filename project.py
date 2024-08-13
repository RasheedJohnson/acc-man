"""
Helper module for main app.
Responsible for writing and reading accounts
to and from backup.csv.
generating passwords,
"""

import random
import csv
from characters import letters, numbers, symbols

PASS_CHAR_LENGTH = 12


def main():
    """
    Welcome messages
    """
    print("Welcome to the app")
    print("Running the 'app.py' file will trigger the GUI")


def store_in_backup(arr: list) -> list:
    """
    receive backups of all saved accounts in backups.csv

    :param arr: account items
    :type arr: list
    """

    with open("backup.csv", "a") as file:
        writer = csv.DictWriter(
            file, fieldnames=["id", "account_type", "username", "email", "password"]
        )
        writer.writerow(
            {
                "id": arr[0],
                "account_type": arr[1],
                "username": arr[2],
                "email": arr[3],
                "password": arr[4],
            }
        )


def parse_dict(list) -> tuple:
    """
    Converts incoming list of dicts
    and returns it as a list of tuples

    :param list: list of accounts as dictionary items
    :type list: list
    :return: A list of tuples to be stored in db
    :rtype: list
    """

    tuples_list = []
    for acc in list:
        tuples_list.append(
            (
                acc["id"],
                acc["account_type"],
                acc["username"],
                acc["email"],
                acc["password"],
            )
        )
    return tuples_list


def read_from_backup() -> list:
    """
    Reads from backups.csv and returns
    list of tuples as account data

    :return: list of tuples (accounts)
    :rtype: list
    """

    list_of_accounts = []
    with open("backup.csv", "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            list_of_accounts.append(row)
    return parse_dict(list_of_accounts)


def generate_pass() -> str:
    """
    generates 12 character password of random
    letters (uppercase and lowercase), numbers,
    and symbols

    :return: A string of characters as password
    :rtype: str
    """

    random_option = [letters, numbers, letters, symbols]
    password = ""
    for _ in range(PASS_CHAR_LENGTH):
        type_char = random.choice(random_option)
        password += random.choice(type_char)
    return password


if __name__ == "__main__":
    main()
