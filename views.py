from passlib.handlers.sha2_crypt import sha256_crypt
from sqlalchemy import select, insert, update

from aiohttp_jinja2 import render_template

import forms
from models import Post, PostObj, Users, UsersObj
from permissions import is_author
from services import get_categories, get_user_id
from aiohttp import web

from aiohttp_security import (
    remember, forget, authorized_userid,
    check_permission, check_authorized,
)

from auth import check_credentials


async def index(request):
    username = await authorized_userid(request)
    return render_template('base.html', request, {'categories': await get_categories(request),
                                                  'logged': username
                                                  })


async def post_list(request):
    username = await authorized_userid(request)

    if request.match_info.get('category'):
        async with request.app['database'].acquire() as conn:
            posts = select([Post.c.id, Post.c.category, Post.c.name, Post.c.price])\
                .where(Post.c.category == int(request.match_info['category']))
            posts = await conn.fetch(posts)
    else:
        async with request.app['database'].acquire() as conn:
            posts = select([Post.c.id, Post.c.category, Post.c.name, Post.c.price])
            posts = await conn.fetch(posts)

    return render_template('post_list.html', request, {'categories': await get_categories(request),
                                                       'posts': posts,
                                                       'logged': username
                                                       })


async def user_post_list(request):
    username = await authorized_userid(request)

    if username:
        async with request.app['database'].acquire() as conn:
            posts = select([Post.c.id, Post.c.author, Post.c.category, Post.c.name, Post.c.price])\
                    .where(Post.c.author == await get_user_id(request, username))
            posts = await conn.fetch(posts)

    return render_template('post_list.html', request, {'categories': await get_categories(request),
                                                       'posts': posts,
                                                       'logged': username
                                                       })


async def post_create(request):
    username = await authorized_userid(request)
    if username:

        data = await request.post()
        form = forms.PostForm(data)

        categories = await get_categories(request)
        form.category.choices = [tuple(category) for category in categories]
        form.author.data = await get_user_id(request, username)

        if request.method == 'POST':
            if form.validate():
                author, category, name, description, price = int(data['author']), \
                                                             int(data['category']), \
                                                             data['name'], \
                                                             data['description'], \
                                                             int(data['price'])
                post_obj = PostObj(author, category, name, description, price)

                async with request.app['database'].acquire() as conn:
                    await conn.execute(
                        insert(Post).values(
                            author=post_obj.author,
                            category=post_obj.category,
                            name=post_obj.name,
                            description=post_obj.description,
                            price=post_obj.price,
                            available=True
                        )
                    )

                location = request.app.router['post_list'].url_for()
                raise web.HTTPFound(location=location)
    else:
        location = request.app.router['login'].url_for()
        raise web.HTTPFound(location=location)

    return render_template('post_create.html', request, {'form': form,
                                                         'categories': categories,
                                                         'logged': username
                                                         })


async def post_update(request):
    username = await authorized_userid(request)
    if username and await is_author(request, username):

        async with request.app['database'].acquire() as conn:
            post = select(
                [Post.c.id, Post.c.category, Post.c.name, Post.c.description, Post.c.price]) \
                .where(Post.c.id == int(request.match_info['id']))
            post = await conn.fetch(post)

        form = forms.PostForm(data=post[0])
        categories = await get_categories(request)
        form.category.choices = [tuple(category) for category in categories]

        if request.method == 'POST':
            data = await request.post()
            form = forms.PostForm(data)
            form.category.choices = [tuple(category) for category in categories]
            form.author.data = await get_user_id(request, username)

            if form.validate():
                category, name, description, price = int(data['category']), \
                                                     data['name'], \
                                                     data['description'], \
                                                     int(data['price'])
                post_obj = PostObj(form.author.data, category, name, description, price)

                async with request.app['database'].acquire() as conn:
                    await conn.execute(
                        insert(Post).values(
                            author=post_obj.author,
                            category=post_obj.category,
                            name=post_obj.name,
                            description=post_obj.description,
                            price=post_obj.price,
                            available=True
                        )
                    )

                location = request.app.router['post_list'].url_for()
                raise web.HTTPFound(location=location)
    else:
        location = request.app.router['login'].url_for()
        raise web.HTTPFound(location=location)

    return render_template('post_update.html', request, {'form': form,
                                                         'post': post[0],
                                                         'categories': categories,
                                                         'logged': username})


async def post_detail(request):
    username = await authorized_userid(request)

    async with request.app['database'].acquire() as conn:
        post = select([Post.c.id, Post.c.name, Post.c.description, Post.c.price]) \
            .where(Post.c.id == int(request.match_info['id']))
        post = await conn.fetch(post)

    return render_template('post_detail.html', request, {'categories': await get_categories(request),
                                                         'post': post[0],
                                                         'logged': username
                                                         })


async def search(request):
    username = await authorized_userid(request)

    async with request.app['database'].acquire() as conn:
        posts = select([Post.c.id, Post.c.name, Post.c.price]) \
            .where(Post.c.name.contains(request.query.get('q')))
        posts = await conn.fetch(posts)

    return render_template('post_list.html', request, {'categories': await get_categories(request),
                                                       'posts': posts,
                                                       'logged': username
                                                       })


async def login(request):
    form = forms.LoginForm()

    if request.method == 'POST':
        location = request.app.router['index'].url_for()
        response = web.HTTPFound(location=location)

        form = await request.post()

        login = form.get('login')
        password = form.get('passwd')

        try:
            if await check_credentials(request.app['database'], login, password):
                await remember(request, response, login)
                location = request.app.router['index'].url_for()
                return web.HTTPFound(location=location)
            raise web.HTTPUnauthorized()
        except web.HTTPUnauthorized:
            location = request.app.router['login'].url_for()
            return web.HTTPFound(location=location)

    return render_template('registration/login.html', request, {'form': form})


async def registration(request):
    form = forms.LoginForm()

    if request.method == 'POST':
        location = request.app.router['index'].url_for()
        response = web.HTTPFound(location=location)

        form = await request.post()

        login = form.get('login')
        password = form.get('passwd')

        login, passwd = login, sha256_crypt.hash(password)

        user_obj = UsersObj(login, passwd)

        async with request.app['database'].acquire() as conn:
            await conn.execute(
                insert(Users).values(
                    login=user_obj.login,
                    passwd=user_obj.passwd
                )
            )
        try:
            if await check_credentials(request.app['database'], login, password):
                await remember(request, response, login)
                location = request.app.router['index'].url_for()
                return web.HTTPFound(location=location)
            raise web.HTTPUnauthorized()
        except web.HTTPUnauthorized:
            location = request.app.router['login'].url_for()
            return web.HTTPFound(location=location)

    return render_template('registration/registration.html', request, {'form': form})


async def logout(request):
    await check_authorized(request)
    response = web.HTTPFound(location=request.app.router['index'].url_for())
    await forget(request, response)
    return response
