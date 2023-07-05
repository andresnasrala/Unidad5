import os

basedir = os.path.abspath(os.path.dirname(__file__))
database_path = os.path.join(basedir, 'database', 'datos.db')

SQLALCHEMY_DATABASE_URI = f'sqlite:///{database_path}'
SECRET_KEY = "POO2023SQLALCHEMYANDNAS"
SQLALCHEMY_TRACK_MODIFICATIONS = False
