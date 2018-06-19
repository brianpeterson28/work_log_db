import csv


class Time_Entry():

    def __init__(self):
        """Initializes Time_Entry class.

        All fields are either an empty string or a 0.
        """

        self.date = ""
        self.title = ""
        self.time_spent = 0
        self.notes = ""

    def set_date(self, date):
        """Sets date field for time entry.

        date is a string that will be used as the date.
        """

        self.date = date

    def set_title(self, title):
        """Sets title field for time entry.

        title is a string that will be used as the title.
        """

        self.title = title

    def set_time_spent(self, time_spent):
        """Sets time_spent field for time entry.

        time_spent is an integer that will be used for time spent.
        """

        self.time_spent = time_spent

    def set_notes(self, notes):
        """Sets notes field for time entry.

        notes is a string that will be used for the notes.
        """

        self.notes = notes

    def create_time_entry(self):
        """Saves completed time entry object to csv file.

        Stores fields into list and then writes into a row of the designated
        csv file.
        """

        entry = [self.date, self.title, self.time_spent, self.notes]
        with open("time_entries.csv", "a", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(entry)
