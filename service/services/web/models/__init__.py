from flask_sqlalchemy import SQLAlchemy

from project import app
# from .encoder import AlchemyEncoder
# from .main import *

db = SQLAlchemy(app)

# __all__ = ["db", 'AlchemyEncoder', "Callback", "Config", "Task"]
