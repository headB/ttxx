from django.urls import path
from . import views

app_name = 'user'

urlpatterns=[
    path('',views.index,name='index'),
    path('register/',views.register,name='register'),
    path('register_handle/',views.register_handle,name='register_handle'),
]