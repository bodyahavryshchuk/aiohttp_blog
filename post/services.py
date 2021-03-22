from sqlalchemy import select

from .models import Category


async def get_categories(request):
    async with request.app['database'].acquire() as conn:
        categories = select([Category.c.id, Category.c.name])
        categories = await conn.fetch(categories)
        return categories
