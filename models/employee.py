from peewee import * 

db = SqliteDatabase('time_entries.db')

class Employee(Model):
    name = CharField(max_length=100, unique=True) #do I need unique setting here? Impact?

    class Meta:
        database = db

if __name__ == '__main__':
    pass
