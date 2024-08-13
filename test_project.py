import pytest
from project import generate_pass, parse_dict, read_from_backup



def main():
    test_pass_gen()
    test_parse_dict()
    test_read_from_backup()

def test_read_from_backup():
    assert type(read_from_backup()) == list

def test_parse_dict():
    mock_list = [
        {"id": 1, "account_type":"site_a", "username":"john harvard", "email":"john@harvard.edu", "password": "pass123"},
        {"id": 2, "account_type":"site_b", "username":"Grace Hopper", "email":"grace@harvard.edu", "password": "pass12356"}
        ]
    result = [
        (1, "site_a", "john harvard", "john@harvard.edu", "pass123"),
        (2, "site_b", "Grace Hopper", "grace@harvard.edu",  "pass12356")
        ]
    assert type(parse_dict(mock_list)) == list
    assert parse_dict(mock_list) == result

def test_pass_gen():
    assert type(generate_pass()) == str
    assert len(generate_pass()) == 12


if __name__ == "__main__":
    main()