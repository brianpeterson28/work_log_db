from peewee import * 
import datetime

db = SqliteDatabase('time_entries.db')


class Time_Entry(Model):
    #employee_name = ForeignKeyField(Employee, related_name='time_entries') #"TypeError: __init__() got an unexpected keyword argument backref"
    date = DateTimeField(default=datetime.datetime.now)
    title = TextField()
    time_spent = IntegerField()
    notes = TextField()

    class meta:
        database = db

class Employee(Model):
    name = CharField(max_length=100, unique=True)

    class Meta:
        database = db
        
def initialize():
    db.connect()
    db.create_tables([Employee, Time_Entry], safe=True)

if __name__ == '__main__':
    initialize()
    Time_Entry.create(title="test title", time_spent=50,
        notes="These are the notes")
    Employee.create(name="Brian Peterson")

