from peewee import *
import datetime

from employee import Employee 

db = SqliteDatabase('time_entries.db')

class Time_Entry(Model):
    employee_name = ForeignKeyField(Employee, backref='time_entries')
    date = DateTimeField(formats='%d/%m/%Y')#may need to switch to '%Y-%m-%d'
    title = TextField()
    time_spent = IntegerField()
    notes = TextField()

    class Meta:
        database = db

if __name__ == '__main__':
    pass