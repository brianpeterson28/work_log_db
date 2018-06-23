from peewee import * 

db = SqliteDatabase('time_entries.db')

class Employee(Model):
    name = CharField(max_length=100, unique=True)

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
    db.connect()
    db.create_tables([Employee], safe=True)
    Employee.create(name="Brian Peterson")
    ee1 = Employee.create(name="Brian Peterson")
    Time_Entry.create(name=ee1.name,title="test title",
        time_spent=50,
        notes="These are the notes")
