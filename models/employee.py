from peewee import * 

db = SqliteDatabase('time_entries.db')

class Employee(Model):
    name = CharField(max_length=100, unique=True) #do I need unique setting here? Impact?

    class Meta:
        database = db

def add_name(employee_name):
    try:
        Employee.create(name=employee_name)
    except IntegrityError:
        pass
        #Need way to print error message to screen. 
        #Either person has same name as somone else or 

if __name__ == '__main__':

