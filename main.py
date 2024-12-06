
#Python Libs
import uvicorn, logging, tomllib, os, json
from tortoise import Tortoise
from decouple import config as env

# To by pass https of OAuth 2
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

#Internal Class
from config.database import Database

#Routes
from routes.api import API  # Import the API class from api.py

app = API().app  # Create an instance of the routes/api.py class

if __name__ == "__main__":
    uvicorn.run("main:app", host=env("APP_HOST"), port=int(env("APP_PORT")), reload=env("APP_RELOAD", True))  # Run the FastAPI
