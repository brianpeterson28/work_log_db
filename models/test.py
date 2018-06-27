from peewee import * 
import datetime

db = SqliteDatabase('time_entries.db')

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

if __name__ == '__main__':
    initialize()
    ee1 = Employee.create(employee_name="Brian Peterson")
    Time_Entry.create(employee_name=ee1, title="test title", 
        time_spent=50, notes="These are the notes")
    ee2 = Employee.create(employee_name="Alan Peterson")
    Time_Entry.create(employee_name=ee2, title="test title 2", 
        time_spent=30, notes="More notes")
    entry = Time_Entry.select().join(Employee).where(Employee.employee_name=="Brian Peterson")
    for entry in query:
        print(entry.title)
        print(entry.employee_name.employee_name)


