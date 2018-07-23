from django.urls import path,include,re_path
from apps.order import views as order_view

import sys
app_name = 'order'
urlpatterns = [
    path('',order_view.index,name='index'),
]