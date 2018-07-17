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
    date = DateTimeField(formats='%Y-%m-%d')

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
                      time_spent='50', notes="These are the notes",
                      date="2018-01-01")
    ee2 = Employee.create(employee_name="Alan Peterson")
    Time_Entry.create(employee_name=ee2, title="Dream Theater",
                      time_spent='120', notes="The Astonishing!!!!!",
                      date="2018-06-01")
    Time_Entry.create(employee_name=ee2, title="Another Dream Theater",
                      time_spent='120', notes="Unexpected Turn of Events!",
                      date="2018-12-01")
    ee_list = Employee.select()
    count = len(ee_list)
    entries = Time_Entry.select().order_by(Time_Entry.date.desc())

    start_date = datetime.datetime.strptime("2017-05-02", '%Y-%m-%d')
    end_date = datetime.datetime.strptime("2018-06-02", '%Y-%m-%d')
    test = ((Time_Entry.date >= start_date) & (Time_Entry.date <= end_date))
    matching_entries = (Time_Entry.select()
                                  .where(test))


    print("These are the query dates:")
    for entry in matching_entries:
        print("{}".format(entry.date))
    print("These are all the dates.")
    for entry in entries:
        print("{}".format(entry.date))
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
    print("Name: {}".format(entries[2]
                        .employee_name
                        .employee_name))
    print("Title: " + entries[2].title)
    print("Time Spent: {}".format(entries[2].time_spent))
    print("Notes: " + entries[2].notes)
    print("")
    entries[1].notes = "This is still astonishing . . . but a little cheesy!"
    entries[1].save()
    print("New Notes: {}".format(entries[1].notes))
    names = (Employee.select().where(Employee.employee_name.contains("Peterson")))
    print("")
    new_count = len(names)
    print("There are {} employees.".format(new_count))
    for employee in names:
        print("{}".format(employee.employee_name))
    #ee2.delete_instance(recursive=True)


    """
    THIS WORKS

    entries[1].delete_instance()
    print("{}".format(Time_Entry
                      .select()
                      .join(Employee)
                      .where(Employee.employee_name == "Alan Peterson")
                      .count()))
    test = (Time_Entry.select()
                      .join(Employee)
                      .where(Employee.employee_name == "Alan Peterson")
                      .count())
    if test == 0:
        ee2.delete_instance()
    else:
        pass
    """
    #You need to check to see if an employee name has any entries left then 
    #delete the employee name then. 

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


