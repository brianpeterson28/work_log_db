from screen import Screen


class Add_Menu(Screen):

    def __init__(self):
        """Initializes the Add_Menu class."""

        self.title = "Work Log Program - Add Time Entry"
        self.options = None

    def show(self):
        """Displays content of the Add_Menu class."""

        print(self.title)
        print("")
