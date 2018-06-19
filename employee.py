from peewee import * 

db = SqliteDatabase('employee.db')

class Employee(Model):
    employeeid = AutoField()
    name = CharField(max_length=100, unique=True)

    class Meta:
        database = db


def add_name(employee_name):
    try:
        Employee.create(name=employee_name)
    except IntegrityError:
        #Need way to print error message to screen. 
        #Either person has same name as somone else or 
        #