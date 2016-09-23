import os

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
DB_PATH = os.path.join('sqlite:///'+ DIR_PATH, 'db', 'data.db')
