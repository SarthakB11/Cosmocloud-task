import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://sarthak:pwdd@cluster0.fdl9e.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
