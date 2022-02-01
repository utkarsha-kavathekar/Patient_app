from flask import Flask
from flask_sqlalchemy import SQLAlchemy
#from sqlalchemy import create_engine,MetaData,Table,Column,Integer,String

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:root@localhost/patient_db'
app.config['SECRET_KEY']='patient_key'
db = SQLAlchemy(app)


