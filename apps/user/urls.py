from django.urls import path
from . import views
app_name = 'user'

urlpatterns=[
    path('',views.LoginView.as_view(),name='index'),
    # path('register/',views.register,name='register'),
    # path('register_handle/',views.register_handle,name='register_handle'),
    path('register/',views.RegisterView.as_view(),name='register'),
    path('active/<str:token>',views.ActiveView.as_view(),name='active'),
    path('login/',views.LoginView.as_view(),name='login'),

]