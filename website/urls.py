
from django.urls import path
from website.views import *


urlpatterns = [
    path('' ,index_view,name='index'),
    path('about',about_view,name='about'),
    path('blog',blog_view,name='blog-home'),
]