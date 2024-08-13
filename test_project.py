import pytest
from project import generate_pass



def main():
    test_pass_gen()

def test_pass_gen():
    assert type(generate_pass()) == str
    assert len(generate_pass()) == 12

# import pyperclip
# import unittest
# import pytest
# from unittest.mock import MagicMock
# import customtkinter
# from project import clear_input_fields, accounts_dict
# import tkinter as tk






# def main(entry_list):
#     test_accounts_dict()
    

# def test_accounts_dict():
#     assert type(accounts_dict()) == dict

# # def test_clear_input_fields():
# #   entries = [MagicMock(), MagicMock(), MagicMock()]
# #   clear_input_fields(entries)
  
# #   for entry in entries:
# #     entry.delete.assert_called_once_with(0, customtkinter.END)
# # class TestApp(unittest.TestCase):
# #     def test_copy_to_clipboard(self):
# #         result = copy_to_clipboard()
# #         self.assertEqual(result, None)



if __name__ == "__main__":
    main()