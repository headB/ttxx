from django.urls import path
from . import views

app_name = 'cart'
urlpatterns=[
    path('add',views.CartAddView.as_view(),name='add'),#购物车商品添加
    path('',views.CartInfoView.as_view(),name='show'),#购物车页面显示
    path('update',views.CartUpdateView.as_view(),name='update'),#购物车页面显示


]