from flask import Flask
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from flask_restless import *


import os

app = Flask(__name__)
#app.config.update(SERVER_NAME='localhost:5010')
DB_PATH = 'sqlite:///' + os.path.dirname(os.path.abspath(__file__)) + '/register.db'

app.config['SQLALCHEMY_DATABASE_URI'] = DB_PATH  # 'sqlite:////tmp/register.db'
db = SQLAlchemy(app)

authors = db.Table('authors',
                   db.Column('author_id', db.Integer, db.ForeignKey('author.id')),
                   db.Column('method_id', db.Integer, db.ForeignKey('method.id'))
                   )

class Method(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True)
    authors = db.relationship('Author', secondary=authors,
                              backref=db.backref('methods', lazy='dynamic')
                              )
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    creation_date = db.Column(db.Date)
    approval_date = db.Column(db.Date)


class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True)
    methods = db.relationship('Method',
                              backref='category',
                              lazy='dynamic')

@app.route('/')
def hello_world():
    return render_template('Index.html')


if __name__ == '__main__':

    mr_manager = APIManager(app, flask_sqlalchemy_db=db)
    mr_manager.create_api(Category, methods=['GET', 'POST'], exclude_columns=['methods'])
    mr_manager.create_api(Author, methods=['GET', 'POST'], include_columns=['id', 'name', 'methods', 'methods.name'])
    mr_manager.create_api(Method, methods=['GET', 'POST', 'PATCH', 'DELETE'],
                          include_columns=['id', 'name', 'authors', 'authors.name', 'category', 'category.name',
                                           'creation_date', 'approval_date'])
    app.run(host='127.0.0.1', port=5010)
    # print(DB_PATH)