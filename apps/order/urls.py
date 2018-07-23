from django.urls import path,include
from apps.order import views as order_view

import sys
app_name = 'xx'
urlpatterns = [
    path('',order_view.index,'name'),
]