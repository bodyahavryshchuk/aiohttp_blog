from aiohttp import web
from auth.urls import setup_auth_routes
from post.urls import setup_post_routes



def setup_routes(app):
    app.add_routes([web.static('/static', 'static')])
    setup_auth_routes(app)
    setup_post_routes(app)
