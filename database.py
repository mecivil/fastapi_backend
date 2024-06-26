from model import Todo
from fastapi import HTTPException 
#MongoDB driver
import motor.motor_asyncio

client = motor.motor_asyncio.AsyncIOMotorClient("mongodb+srv://allaccess:monod.exe@cluster0.u7h8w6p.mongodb.net/?retryWrites=true&w=majority")

database = client.TodoList
collection = database.todo


async def fetch_one_todo(title):
    if (document := await collection.find_one({"title": title})) is not None:
        return document
    return 0


async def fetch_all_todos():
    todos = []
    cursor = collection.find({})
    async for document in cursor :
        todos.append(Todo(**document))
    return todos

async def create_todo(todo):
    document = todo
    result = await collection.insert_one(document)
    if result:
        return document
    return 0


async def update_todo(title,desc):
    await collection.update_one({"title":title},{"$set":{"description":desc}})
    if (document := await collection.find_one({"title": title})) is not None:
        return document
    return 0

async def remove_todo(title):
    result=await collection.delete_one({"title":title})
    if result.deleted_count == 1:
        return True
    return False
