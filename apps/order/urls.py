from django.urls import path,include,re_path
from . import views 


app_name = 'order'
urlpatterns = [
    path('place',views.OrderPlaceView.as_view(),name='place'),
    path('commit',views.OrderCommitView.as_view(),name='commit'),
]