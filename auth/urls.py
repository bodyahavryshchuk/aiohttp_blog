from aiohttp import web
from . import views


def setup_auth_routes(app):
    app.add_routes([web.get('/login', views.login, name='login'),
                    web.post('/login', views.login, name='login'),
                    web.get('/logout', views.logout, name='logout'),

                    web.get('/registration', views.registration, name='registration'),
                    web.post('/registration', views.registration, name='registration'),
                    ])
