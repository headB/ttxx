from django.urls import path
from . import views

app_name = 'goods'

urlpatterns=[
    path('index',views.IndexView.as_view(),name='index'),
    path('',views.IndexView.as_view(),name='index'),
    path('goods/<int:goods_id>',views.DetailView.as_view(),name='detail'),
    path('list/<int:type_id>/<int:page>',views.ListView.as_view(),name='list'),
    

]