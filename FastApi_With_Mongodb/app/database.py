from motor.motor.asyncio import AsyncIOMotorClient

client : AsyncIOMotorClient = None
database = None

async def connect_db():
    global client,database

    client = AsyncIOMotorClient("mongodb://localhost:27017")
    database = client["my_database"]

    print("Connected to database")


async def close_db():
    global client

    if client:
        client.close()
        print("Database Closed")


async def get_database():
    return database