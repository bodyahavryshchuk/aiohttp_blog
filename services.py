from sqlalchemy import select

from models import Category, Users


async def get_categories(request):
    async with request.app['database'].acquire() as conn:
        categories = select([Category.c.id, Category.c.name])
        categories = await conn.fetch(categories)
        return categories


async def get_user_id(request, username):
    async with request.app['database'].acquire() as conn:
        user = select([Users.c.id, Users.c.login]) \
                .where(Users.c.login == username)
        user = await conn.fetch(user)
    return user[0]['id']

