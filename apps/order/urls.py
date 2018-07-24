from django.urls import path,include,re_path
from . import views as order_view


app_name = 'user'
urlpatterns = [
    path('',order_view.index,name='index'),
]