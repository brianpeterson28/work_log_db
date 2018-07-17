import unittest

from worklog_db import *
from add_menu import Add_Menu
from main_menu import Main_Menu
from search_menu import Search_Menu
from models.time_entry import Time_Entry
from models.employee import Employee
from time_entriesdb import *

class MenuTests(unittest.TestCase):

    def test_main_menu(self):

        main_menu = Main_Menu()
        correct_title = "Work Log Program - Main Menu"
        correct_options = ["Add New Entry", "Search Existing", "Quit Program"]
        self.assertEqual(correct_title, main_menu.title)
        self.assertEqual(correct_options, main_menu.options)

    def test_search_menu(self):
        search_menu = Search_Menu()
        correct_title = "Work Log Program - Search Menu"
        correct_options = ["a) Browse by Employee Name",
                           "b) Search by Employee Name",
                           "c) Exact Date",
                           "d) Date Range",
                           "e) Time Spent",
                           "f) Keyword Search",
                           "g) Return to Main Menu"]
        self.assertEqual(correct_title, search_menu.title)
        self.assertEqual(correct_options, search_menu.options)



if __name__ == '__main__':
    unittest.main()