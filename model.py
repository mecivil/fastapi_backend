import mongoengine
from pydantic import BaseModel
from mongoengine import Document , StringField
mongoengine.connect('TodoList', host="mongodb+srv://allaccess:monod.exe@cluster0.u7h8w6p.mongodb.net/?retryWrites=true&w=majority")
class Todo(BaseModel):
    title: str
    description: str

class User(Document):
    username = StringField()
    password = StringField()

class Admin(Document):
    username = StringField()
    password = StringField()

class NewUser(BaseModel):
    username:str
    password:str