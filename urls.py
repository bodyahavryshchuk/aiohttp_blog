from aiohttp import web
import views


def setup_routes(app):
    app.add_routes([web.static('/static', 'static'),
                    web.get('/login', views.login, name='login'),
                    web.post('/login', views.login, name='login'),
                    web.get('/logout', views.logout, name='logout'),

                    web.get('/registration', views.registration, name='registration'),
                    web.post('/registration', views.registration, name='registration'),

                    web.get('/posts', views.post_list, name='post_list'),
                    web.get('/posts/{category}', views.post_list, name='post_list_by_category'),
                    web.get('/user-posts', views.user_post_list, name='post_list_by_user'),

                    web.get('/post-create', views.post_create, name='post_create'),
                    web.post('/post-create', views.post_create, name='post_create'),

                    web.get('/post/{id}/update', views.post_update, name='post_update'),
                    web.post('/post/{id}/update', views.post_update, name='post_update'),

                    web.get('/post/{id}', views.post_detail, name='post_detail'),

                    web.get('/search', views.search, name='search'),

                    web.get('/', views.index, name='index'),
                    ])
