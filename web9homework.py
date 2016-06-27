from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import sql

import time
import shutil

db_path = 'db.sqlite'

app = Flask(__name__)

app.secret_key = 'random string'

app.config['SQLALCHEMY_DATABASE_URI'] = \
    'sqlite:///{}'.format(db_path)

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String())
    password = db.Column(db.String())
    role = db.Column(db.Integer, default=2)
    # todolist = db.relationship('Todolist', backref='user')
    todolist = db.relationship('Todolist', backref='user')

    def __init__(self, form):
        super(User, self).__init__()
        self.username = form.get('username', '')
        self.password = form.get('password', '')

    def __repr__(self):
        class_name = self.__class__.__name__
        return u'<{}: {}>'.format(class_name, self.id)

    def is_admin(self):
        return self.role == 1

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delect(self)
        db.session.commit()

    def valid(self):
        username_len = len(self.username) >= 3
        password_len = len(self.password) >= 3
        return username_len and password_len

    def validate(self, user):
        if isinstance(user, User):
            username_equals = self.username == user.username
            password_equals = self.password == user.password
            return username_equals and password_equals
        else:
            return False


class Todolist(db.Model):
    __tablename__ = 'todolists'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String())
    # created_time = db.Column(db.DateTime(timezone=True), default=sql.func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, form):
        self.content = form.get('content', '')

    def __repr__(self):
        class_name = self.__class__.__name__
        return u'<{}: {}>'.format(class_name, self.id)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


def backup_db():
    backup_path = '{}.{}'.format(time.time(), db_path)
    shutil.copyfile(db_path, backup_path)


def rebuild_db():
    backup_db()
    db.drop_all()
    #db.create_all()
    print('rebuild database')


if __name__ == '__main__':
    rebuild_db()
