from peewee import * 
import datetime

db = SqliteDatabase('time_entries.db', pragmas={'foreign_keys': 1})

class Employee(Model):
    employee_name = CharField(max_length=100, unique=True)

    class Meta:
        database = db


class Time_Entry(Model):
    employee_name = ForeignKeyField(Employee, backref='time_entries') 
    title = TextField()
    time_spent = IntegerField()
    notes = TextField()

    class Meta:
        database = db

        
def initialize():
    db.connect()
    db.create_tables([Employee, Time_Entry], safe=True)

def run_regex_process():
    print("This will search for matches in the title and notes fields.")
    regex_pattern = input("Enter a valid regex pattern: ")
    time_entries = recall_time_entries()

if __name__ == '__main__':
    initialize()
    ee1 = Employee.create(employee_name="Brian Peterson")
    Time_Entry.create(employee_name=ee1, title="test title",
                      time_spent='50', notes="These are the notes")
    ee2 = Employee.create(employee_name="Alan Peterson")
    Time_Entry.create(employee_name=ee2, title="Dream Theater",
                      time_spent='120', notes="The Astonishing!!!!!")
    ee_list = Employee.select()
    count = len(ee_list)
    entries = Time_Entry.select()

    print("There are {} employees with time entries.".format(count))
    print(ee_list[0].employee_name)
    print(ee_list[1].employee_name)
    print("")
    print("Name: {}".format(entries[1]
                            .employee_name
                            .employee_name))
    print("Title: " + entries[1].title)
    print("Time Spent: {}".format(entries[1].time_spent))
    print("Notes: " + entries[1].notes)
    print("")
    entries[1].notes = "This is still astonishing . . . but a little cheesy!"
    entries[1].save()
    print("New Notes: {}".format(entries[1].notes))
    entries[1].delete_instance(recursive=True)
    #You need to check to see if an employee name has any entries left

    """

    WORKS! 
    try:
        employee = Employee.get(Employee.employee_name == "Jordan Asker")
    except DoesNotExist:
        employee = Employee.create(employee_name="Jordan Asker")


    WORKS! 
    #initialize()
    #ee1 = Employee.create(employee_name="Brian Peterson")
    #Time_Entry.create(employee_name=ee1, title="test title", 
    #    time_spent='50', notes="These are the notes")
   # ee2 = Employee.create(employee_name="Alan Peterson")
    #Time_Entry.create(employee_name=ee2, title="test title 2", 
   #     time_spent=30, notes="More notes")
    #query = Time_Entry.select().join(Employee).where(Employee.employee_name=="Brian Peterson")
    #for entry in query:
    #    print(entry.title)
     #   print(entry.employee_name.employee_name)
    """


