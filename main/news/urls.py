from django.urls import path

from .views import *

urlpatterns = [
    # path('', index, name='index'),
    path('', IndexView.as_view(), name='index'),
    # path('category/<int:category_id>/', get_category,  name='get_category'),
    path('category/<int:category_id>/', CategoryNews.as_view(),  name='get_category'),
    path('news/<int:news_id>/', view_news, name='view_news'),
    path('news/add-news/', add_news, name='add_news'),
    path('news/add_news_1/', add_news_1, name='add_news_1'),
    path('news/register/', register, name='register'),
    path('news/login/', user_login, name='login'),
    path('news/logout/', user_logout, name='logout'),
]

