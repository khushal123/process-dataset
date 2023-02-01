from configparser import SafeConfigParser
import os
from flask_sqlalchemy import SQLAlchemy
parser = SafeConfigParser()

print(os.path.join(os.getcwd(), "../config.ini"))
parser.read(os.path.join(os.getcwd(), "config.ini"))

DATABASE_URL=parser["DATABASE"]['DATABASE_URL']





