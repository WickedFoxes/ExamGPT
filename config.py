import os

BASE_DIR = os.path.dirname(__file__)

db_config = {
    'user' : 'examgpt_admin',
    'password' : 'qwer12#$',
    'host': 'localhost',
    'port': 3306,
    'database': 'examgpt'
}

# SQLALCHEMY_DATABASE_URI = f"mysql+mysqlconnector://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}?charset=utf8"
# SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR, 'pybo.db'))
SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR, 'ept.db'))
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = "dev"
