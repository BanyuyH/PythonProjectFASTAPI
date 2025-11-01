import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv  # load environment variables

load_dotenv()  # To load the variables from the .env file


class Database:
    def __init__(self):
        # These will hold the mongodb connection client and reference to a specific database
        self.client = None
        self.database = None

    async def connect(self):  # ✅ FIXED: Added self parameter
        """Here is where the connection to the MongoDB occurs. Am actually using MongoDB atlas"""
        try:
            # MONGODB ATLAS CONNECTION STRING
            connection = os.getenv("MONGODB_URL")

            # Recommended for atlas
            self.client = AsyncIOMotorClient(  # ✅ FIXED: Store in self.client
                connection,
                maxPoolSize=100,
                minPoolSize=10  # ✅ FIXED: Changed from 100 to 10 (min should be smaller)
            )

            '''Test The connection'''
            await self.client.admin.command('ping')

            '''Get the database'''
            self.database = self.client[os.getenv("DATABASE_NAME")]  # ✅ FIXED: Store in self.database
            print(f"Connected to database MongoDB Successfully: {self.database.name}")

        except Exception as error:
            print(f"Failed to connect to database: {error}")
            print("Check your environment variables and try again")
            raise error

    async def close(self):
        """Close the connection to the database"""
        if self.client:
            self.client.close()
            print("MongoDB connection closed")

    def get_collection(self, collection_name: str):
        """Get a collection from the database for review"""
        if self.database is None:
            raise Exception("Database not connected. Call connect() first")
        return self.database[collection_name]


# Create an instance
mongodb = Database()