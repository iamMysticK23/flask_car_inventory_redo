# Configuration for application
import os
from dotenv import load_dotenv
from datetime import timedelta


basedir = os.path.abspath(os.path.dirname(__file__)) #this is establishing our base directory or our root folder

load_dotenv(os.path.join(basedir, '.env')) #this is just pointing us to the direction of our environment variables (located in .env file)

# making this a separate class, we can have many Config classes (aka 1 for development)
# 1 for production
class Config():

    """
    Set config variables for our flask app.
    Using Environment variables where available otherwise
    Create config variables
    
    """

    FLASK_APP = os.environ.get('FLASK_APP') # looking for the key of Flask app in our .env file
    FLASK_ENV = os.environ.get('FLASK_ENV')
    FLASK_DEBUG = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or "You will never have the key to life" # just needs to be a string 
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False # hide update messages
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=365)
