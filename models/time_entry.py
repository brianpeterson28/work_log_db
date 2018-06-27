from peewee import *
import datetime

from employee import Employee 

db = SqliteDatabase('time_entries.db')

class Time_Entry(Model):
    #employee_name = ForeignKeyField(Employee, related_name='time_entries') #"TypeError: __init__() got an unexpected keyword argument backref"
    date = DateTimeField(default=datetime.datetime.now)
    title = TextField()
    time_spent = IntegerField()
    notes = TextField()

    class Meta:
        database = db

if __name__ == '__main__':
    pass