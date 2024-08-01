from peewee import *

db = SqliteDatabase('database.db')


class Category(Model):
    name = CharField()
    url = CharField()

    def __str__(self):
        return f"Category - {self.id}"
    
    class Meta:
        database = db
        
class Book(Model):
    name = CharField()
    description = CharField()
    price = FloatField()
    rating = IntegerField()
    category = ForeignKeyField(Category)

    def __str__(self):
        return f"Book - {self.id}"
    
    class Meta:
        database = db
db.connect()
db.create_tables([Book, Category])

