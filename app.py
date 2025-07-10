from flask import Flask
from routes import pages
import os
from pymongo import MongoClient
from dotenv import load_dotenv
import certifi
from pymongo.server_api import ServerApi

                                                                                                                                                                       

load_dotenv()

def create_app():
    app = Flask(__name__)
    client = MongoClient(os.environ.get("MONGODB_URI"), tlsCAFile=certifi.where(), server_api=ServerApi('1'))
    app.db = client["HabitTracker"]
    try:
        client.admin.command('ping')
        print("✅ MongoDB connection successful")
    except Exception as e:
        print("❌ MongoDB connection failed:", e)
        
    app.register_blueprint(pages)
    return app