
from django.urls import path
from blog.views import *

app_name = 'blog'

urlpatterns = [
    path('', blog_view, name='index'),
    path('single/<int:pk>/', blog_single, name='single'),
    path('category/<str:slug>/', category_view, name='category'),
    path('search/', search_view, name='search'),
]