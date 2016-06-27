# -*- coding: utf-8 -*-
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import shutil
import time
import hashlib

db_path = 'dbhomework.sqlite'

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = \
    'sqlite:///{}'.format(db_path)

db = SQLAlchemy(app)


def comver_to_hash(content):
    hash = hashlib.sha1(content.encode('utf-8')).hexdigest()
    return hash


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String())
    password = db.Column(db.String())
    role = db.Column(db.Integer, default=2)
    bloglist = db.relationship('Bloglist', backref='user')
    # 一对多,blog通过user来确定是谁发的博客




    def __init__(self, form):
        super(User, self).__init__()
        self.username = form.get('username', '')
        self.password = comver_to_hash((form.get('password', '')))
        # self.password = form.get('password', '')

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

    def valid_unique_existence(self):
        user = User.query.filter_by(username=self.username).first()
        if user == None:
            return True
        else:
            return False



class Bloglist(db.Model):
    __tablename__ = 'bloglists'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    content = db.Column(db.String())
    #comment = db.relationship('Comment', backref='poster')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, form):
        self.title = form.get('title', '')
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


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    blog_title = db.Column(db.Integer, db.ForeignKey('bloglists.title'))
    comment_content = db.Column(db.String())
    poster = db.Column(db.Integer)

    def __init__(self, form):
        self.comment_content = form.get('comment_content', '')

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
    # backup_db()
    db.drop_all()
    db.create_all()
    print('rebuild database')


if __name__ == '__main__':
    rebuild_db()