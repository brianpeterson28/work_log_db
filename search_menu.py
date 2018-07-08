from screen import Screen


class Search_Menu(Screen):

    def __init__(self):
        """Initializes Search_Menu class."""

        self.title = "Work Log Program - Search Menu"
        self.options = ["a) Employee Name",
                        "b) Exact Date",
                        "c) Date Range",
                        "d) Time Spent",
                        "e) Search Term",
                        "f) Return to Main Menu"]

    def show(self):
        """Displays the content of the Search_Menu class."""

        print(self.title)
        print("")
        print("Available Search Types:")
        for item in self.options:
            print("{}".format(item))
        print("")
