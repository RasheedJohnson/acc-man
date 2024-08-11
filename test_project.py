import pyperclip
import unittest
import pytest
from unittest.mock import MagicMock
import customtkinter
from project import clear_input_fields

def main(entry_list):
    test_clear_input_fields()
  # ... function body

def test_clear_input_fields():
  entries = [MagicMock(), MagicMock(), MagicMock()]
  clear_input_fields(entries)
  
  for entry in entries:
    entry.delete.assert_called_once_with(0, customtkinter.END)
# class TestApp(unittest.TestCase):
#     def test_copy_to_clipboard(self):
#         result = copy_to_clipboard()
#         self.assertEqual(result, None)



if __name__ == "__main__":
    main()