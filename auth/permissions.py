from aiohttp import web
from sqlalchemy import select

from post.models import Post
from .models import Users
from .services import get_user_id


async def is_author(request, username):
    async with request.app['database'].acquire() as conn:
        post = select([Post.c.id, Post.c.author]).where(Post.c.id == int(request.match_info['id']))
        post = await conn.fetch(post)
        post_author = post[0]['author']
    if await get_user_id(request, username) == post_author:
        return True
    raise web.HTTPForbidden()


async def is_superuser(request, username):
    async with request.app['database'].acquire() as conn:
        user = select([Users.c.id, Users.c.login, Users.c.is_superuser]) \
                .where(Users.c.login == username)
        user = await conn.fetch(user)
    if user[0]['is_superuser']:
        return True
    raise web.HTTPForbidden()
