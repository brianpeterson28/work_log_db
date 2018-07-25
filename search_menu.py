from screen import Screen


class Search_Menu(Screen):

    def __init__(self):
        """Initializes Search_Menu class."""

        self.title = "Work Log Program - Search Menu"
        self.options = ["a) Browse by Employee Name",
                        "b) Search by Employee Name",
                        "c) Exact Date",
                        "d) Date Range",
                        "e) Time Spent",
                        "f) Keyword Search",
                        "g) Return to Main Menu"]

    def show(self):
        """Displays the content of the Search_Menu class."""

        print(self.title)
        print("")
        print("Available Search Types:")
        for item in self.options:
            print("{}".format(item))
        print("")
        return 0

if __name__ == '__main__':
    self.show()