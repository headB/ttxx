from django.urls import path,include,re_path
from . import views 


app_name = 'order'
urlpatterns = [
    path('place',views.OrderPlaceView.as_view(),name='place'),
    path('commit',views.OrderCommitView.as_view(),name='commit'),
    path('pay', views.OrderPayView.as_view(), name='pay'), # 订单支付
    path('check', views.CheckPayView.as_view(), name='check'), # 订单支付
    path('comment/<int:order_id>', views.CommentView.as_view(), name='comment'), # 订单支付
]