import datetime
import sqlalchemy as sa
from sqlalchemy import Column, ForeignKey, Boolean, Integer, DateTime, Text, VARCHAR
from sqlalchemy import MetaData, Table


__all__ = ('category', 'post', 'users', 'permissions')

from sqlalchemy.orm import mapper

meta = MetaData()


Users = sa.Table(
    'users', meta,
    Column('id', sa.Integer, nullable=False),
    Column('login', sa.String(256), nullable=False),
    Column('passwd', sa.String(256), nullable=False),
    Column('is_superuser', sa.Boolean, nullable=False,
              server_default='FALSE'),
    Column('disabled', sa.Boolean, nullable=False,
              server_default='FALSE'),

    sa.PrimaryKeyConstraint('id', name='user_pkey'),
    sa.UniqueConstraint('login', name='user_login_key'),
)


Permissions = sa.Table(
    'permissions', meta,
    Column('id', sa.Integer, nullable=False),
    Column('user_id', sa.Integer, nullable=False),
    Column('perm_name', sa.String(64), nullable=False),

    sa.PrimaryKeyConstraint('id', name='permission_pkey'),
    sa.ForeignKeyConstraint(['user_id'], [Users.c.id],
                            name='user_permission_fkey',
                            ondelete='CASCADE'),
)

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
        self.created = datetime.datetime.now()


class UsersObj(object):
    def __init__(self, login, passwd):
        self.id = id
        self.login = login
        self.passwd = passwd
        self.is_superuser = False
        self.disabled = False


category_mapper = mapper(CategoryObj, Category)
post_mapper = mapper(PostObj, Post)
users_mapper = mapper(UsersObj, Users)

