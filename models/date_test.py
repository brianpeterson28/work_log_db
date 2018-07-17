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
    date = DateField(formats='%d/%m/%Y')

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
    date1 = datetime.datetime.strptime("02/05/2017", '%d/%m/%Y')
    Time_Entry.create(employee_name=ee1, title="test title",
                      time_spent='50', notes="These are the notes",
                      date=date1)

    ee2 = Employee.create(employee_name="Alan Peterson")
    date2 = datetime.datetime.strptime("01/06/2018", '%d/%m/%Y')
    Time_Entry.create(employee_name=ee2, title="Dream Theater",
                      time_spent='120', notes="The Astonishing!!!!!",
                      date=date2)

    date3 = datetime.datetime.strptime("01/12/2018", '%d/%m/%Y')
    Time_Entry.create(employee_name=ee2, title="Another Dream Theater",
                      time_spent='120', notes="Unexpected Turn of Events!",
                      date=date3)

    ee_list = Employee.select()
    count = len(ee_list)
    entries = Time_Entry.select().order_by(Time_Entry.date.desc())

    start_date = datetime.datetime.strptime("02/05/2018", '%d/%m/%Y')
    end_date = datetime.datetime.strptime("30/12/2018", '%d/%m/%Y')
    test = ((Time_Entry.date >= start_date) & (Time_Entry.date <= end_date))
    matching_entries = (Time_Entry.select()
                                  .where(test))

    print(start_date)
    print("These are the query dates:")
    for entry in matching_entries:
        dt = datetime.datetime.strptime(entry.date, '%Y-%m-%d')
        print("Date: ", end="")
        print("{:%d/%m/%Y}".format(dt))
    print("These are all the dates.")
    for entry in entries:
        print("{}".format(entry.date))