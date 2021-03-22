from passlib.handlers.sha2_crypt import sha256_crypt
from sqlalchemy import insert

from aiohttp_jinja2 import render_template

from . import forms
from .models import Users, UsersObj
from aiohttp import web

from aiohttp_security import remember, forget, check_authorized

from auth.auth import check_credentials


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
