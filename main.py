import aiohttp_jinja2
import jinja2
from aiohttp import web
from aiohttp_session import setup as setup_session
from aiohttp_session.redis_storage import RedisStorage
from aiohttp_security import setup as setup_security
from aiohttp_security import SessionIdentityPolicy

from auth import DBAuthorizationPolicy
import asyncpgsa
from aioredis import create_pool
from urls import setup_routes


async def init():
    app = web.Application()

    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('templates'))

    app['database'] = await asyncpgsa.create_pool(user='postgres',
                                                  database='aiohttp',
                                                  host='127.0.0.1',
                                                  password='password')

    redis_pool = await create_pool(('localhost', 6379))
    setup_session(app, RedisStorage(redis_pool))
    setup_security(app, SessionIdentityPolicy(), DBAuthorizationPolicy(app['database']))

    setup_routes(app)

    return app


if __name__ == '__main__':
    web.run_app(init(), host='127.0.0.1', port=8000)
