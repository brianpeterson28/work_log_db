from peewee import * 

from models.employee import Employee 
from models.time_entry import Time_Entry

db = SqliteDatabase('time_entries.db')
        
def initialize():
    db.connect()
    db.create_tables([Employee, Time_Entry], safe=True)

if __name__ == '__main__':
    initialize()
    ee1 = Employee.create(name="Brian Peterson")
    Time_Entry.create(name=ee1.name,title="test title",
        time_spent=50,
        notes="These are the notes")