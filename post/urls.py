from aiohttp import web
from . import views


def setup_post_routes(app):
    app.add_routes([web.get('/posts', views.post_list, name='post_list'),
                    web.get('/posts/{category}', views.post_list, name='post_list_by_category'),
                    web.get('/user-posts', views.user_post_list, name='post_list_by_user'),

                    web.get('/post-create', views.post_create, name='post_create'),
                    web.post('/post-create', views.post_create, name='post_create'),

                    web.get('/post/{id}/update', views.post_update, name='post_update'),
                    web.post('/post/{id}/update', views.post_update, name='post_update'),

                    web.get('/post/{id}', views.post_detail, name='post_detail'),

                    web.post('/post/{id}/comment/create', views.comment_create, name='comment_create'),

                    web.get('/search', views.search, name='search'),

                    web.get('/', views.index, name='index'),
                    ])
