from peewee import *

db = SqliteDatabase('time_entries.db')


class Employee(Model):
    name = CharField(max_length=100, unique=True)

    class Meta:
        database = db


if __name__ == '__main__':
    pass
