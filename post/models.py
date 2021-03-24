import datetime
from sqlalchemy import Column, ForeignKey, Boolean, Integer, DateTime, Text, VARCHAR
from sqlalchemy import MetaData, Table


__all__ = ('category', 'post')

from sqlalchemy.orm import mapper

meta = MetaData()

Category = Table(
    'category', meta,
    Column('id', Integer, primary_key=True, index=True, unique=True, autoincrement=True),
    Column('name', VARCHAR, nullable=True),
)

Post = Table(
    'post', meta,
    Column('id', Integer, primary_key=True, index=True, unique=True, autoincrement=True),
    Column('author', Integer, ForeignKey('users.id')),
    Column('category', Integer, ForeignKey('category.id')),
    Column('name', VARCHAR),
    Column('description', Text),
    Column('price', Integer),
    Column('available', Boolean, default=True),
    Column('created', DateTime),
)

Comment = Table(
    'comment', meta,
    Column('id', Integer, primary_key=True, index=True, unique=True, autoincrement=True),
    Column('author', Integer, ForeignKey('users.id')),
    Column('post', Integer, ForeignKey('post.id')),
    Column('text', Text),
    Column('available', Boolean, default=True),
    Column('created', DateTime),
)


class CategoryObj(object):
    def __init__(self, name):
        self.name = name


class PostObj(object):
    def __init__(self, author, category, name, description, price):
        self.id = id
        self.author = author
        self.category = category
        self.name = name
        self.description = description
        self.price = price
        self.available = True
        self.created = None


class CommentObj(object):
    def __init__(self, post, author, text):
        self.id = id
        self.post = post
        self.author = author
        self.text = text
        self.available = True
        self.created = None


category_mapper = mapper(CategoryObj, Category)
post_mapper = mapper(PostObj, Post)
comment_mapper = mapper(CommentObj, Comment)

