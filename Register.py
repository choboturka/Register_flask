from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restless import *
import sqlite3

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://localhost/register'
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
    return 'Hello World!'


if __name__ == '__main__':

    db.create_all()
    # mr_manager = APIManager(app, flask_sqlalchemy_db=db)
    #
    # mr_manager.create_api(Category, methods=['GET', 'POST'])
    # mr_manager.create_api(Author,)
    app.run()